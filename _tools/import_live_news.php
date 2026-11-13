<?php
/**
 * Pull the real news content from the live site into the new build.
 *
 * The four /news posts on stage were placeholder bodies (Lorem ipsum, or a
 * single "Placeholder photo" caption). The client's live WordPress site has the
 * real posts, so this script fetches each one over the REST API, downloads the
 * images into the local media library, and writes clean, editor-friendly HTML.
 *
 * Runs against whichever site the CLI points at, so Local and stage each end up
 * with their own attachment URLs. Idempotent: posts already imported carry
 * `_gsm_live_source` and are skipped.
 *
 * Run:  wp eval-file _tools/import_live_news.php          (skips already imported)
 *       wp eval-file _tools/import_live_news.php force    (re-import everything)
 */

$LIVE = 'https://www.goodshepherdmanor.org/wp-json/wp/v2/posts/';

$MAP = array(
	2145 => array( 'live' => 2648, 'mode' => 'text' ),     // 35th Annual Fall Festival
	2147 => array( 'live' => 2554, 'mode' => 'gallery', 'images' => 3 ), // Digital Den
	2149 => array( 'live' => 2639, 'mode' => 'flyer' ),    // Golf sponsors thank-you
	2151 => array( 'live' => 2627, 'mode' => 'flyer' ),    // Family cookouts
);

$force = in_array( 'force', $args, true ) || in_array( '--force', $args, true );

/** Strip the WebP passthru wrapper so post content stores a plain upload URL. */
function gsm_clean_url( $url ) {
	if ( false !== strpos( $url, 'webpc-passthru.php' ) ) {
		$query = wp_parse_url( $url, PHP_URL_QUERY );
		parse_str( (string) $query, $parts );
		if ( ! empty( $parts['src'] ) ) {
			$url = $parts['src'];
		}
	}
	// Store the path only, so the same content works on Local and stage.
	$path = wp_parse_url( $url, PHP_URL_PATH );
	return $path ? $path : $url;
}

/** Sideload an image and return its URL, or '' on failure. */
function gsm_import_image( $url, $post_id, $alt ) {
	$url = preg_replace( '/-\d+x\d+(\.(?:jpg|jpeg|png|webp))$/i', '$1', $url );

	$existing = get_posts( array(
		'post_type'      => 'attachment',
		'posts_per_page' => 1,
		'meta_key'       => '_gsm_source_url',
		'meta_value'     => $url,
		'fields'         => 'ids',
	) );

	if ( $existing ) {
		return gsm_clean_url( wp_get_attachment_url( $existing[0] ) );
	}

	$tmp = download_url( $url );
	if ( is_wp_error( $tmp ) ) {
		WP_CLI::warning( 'download failed: ' . $url );
		return '';
	}

	$file = array(
		'name'     => basename( parse_url( $url, PHP_URL_PATH ) ),
		'tmp_name' => $tmp,
	);

	$id = media_handle_sideload( $file, $post_id, $alt );
	if ( is_wp_error( $id ) ) {
		@unlink( $tmp );
		WP_CLI::warning( 'sideload failed: ' . $url );
		return '';
	}

	update_post_meta( $id, '_gsm_source_url', $url );
	update_post_meta( $id, '_wp_attachment_image_alt', $alt );

	return gsm_clean_url( wp_get_attachment_url( $id ) );
}

$total = 0;

foreach ( $MAP as $post_id => $cfg ) {
	$post = get_post( $post_id );
	if ( ! $post ) {
		WP_CLI::warning( "{$post_id}: post not found" );
		continue;
	}

	$already = get_post_meta( $post_id, '_gsm_live_source', true );
	if ( $already && ! $force ) {
		WP_CLI::log( "{$post_id} {$post->post_name}: already imported from live #{$already}" );
		continue;
	}

	$res = wp_remote_get( $LIVE . $cfg['live'] . '?_fields=id,slug,title,content,date', array( 'timeout' => 30 ) );
	if ( is_wp_error( $res ) || 200 !== wp_remote_retrieve_response_code( $res ) ) {
		WP_CLI::warning( "{$post_id}: could not fetch live #{$cfg['live']}" );
		continue;
	}

	$live = json_decode( wp_remote_retrieve_body( $res ), true );
	if ( empty( $live['content']['rendered'] ) ) {
		WP_CLI::warning( "{$post_id}: live post has no content" );
		continue;
	}

	$html = $live['content']['rendered'];

	// Paragraphs and headings, in document order, cleaned of inline markup.
	$paragraphs = array();
	$items      = array();

	if ( preg_match_all( '/<(p|h[1-6])[^>]*>(.*?)<\/\1>/s', $html, $m, PREG_SET_ORDER ) ) {
		foreach ( $m as $node ) {
			$text = trim( html_entity_decode( wp_strip_all_tags( $node[2] ), ENT_QUOTES, 'UTF-8' ) );
			$text = trim( preg_replace( '/\s+/', ' ', str_replace( "\xc2\xa0", ' ', $text ) ) );
			if ( '' === $text ) {
				continue;
			}
			// Live posts use h1/h2/h3 for titles and h4-h6 for body copy — treat the
			// small headings as paragraphs so they don't land as giant headings here.
			$is_heading = in_array( $node[1], array( 'h1', 'h2', 'h3' ), true );
			$items[] = array( 'heading' => $is_heading, 'text' => $text );
			if ( ! $is_heading ) {
				$paragraphs[] = $text;
			}
		}
	}

	$blocks = array();
	$title  = get_the_title( $post_id );

	foreach ( $items as $item ) {
		$blocks[] = $item['heading']
			? '<h2>' . esc_html( $item['text'] ) . '</h2>'
			: '<p>' . esc_html( $item['text'] ) . '</p>';
	}

	if ( 'flyer' === $cfg['mode'] ) {
		preg_match( '/<img[^>]+src="([^"]+)"/', $html, $img );
		$src = $img[1] ?? '';
		$url = $src ? gsm_import_image( $src, $post_id, $title ) : '';

		// Flyer first, then any caption text the live post carries.
		if ( $url ) {
			array_unshift( $blocks, '<figure class="wp-block-image size-large"><img src="' . esc_url( $url ) . '" alt="' . esc_attr( $title ) . '" /></figure>' );
		}
	} elseif ( 'gallery' === $cfg['mode'] ) {
		preg_match_all( '/<img[^>]+src="([^"]+)"/', $html, $all );
		$urls = array_values( array_unique( $all[1] ?? array() ) );
		$urls = array_values( array_filter( $urls, function ( $u ) {
			return false === strpos( $u, 'fbcdn.net' ); // skip emoji sprites
		} ) );
		$urls = array_slice( $urls, 0, (int) ( $cfg['images'] ?? 3 ) );

		foreach ( $urls as $i => $src ) {
			$alt = sprintf( '%s — photo %d', $title, $i + 1 );
			$url = gsm_import_image( $src, $post_id, $alt );
			if ( $url ) {
				$blocks[] = '<figure class="wp-block-image size-large"><img src="' . esc_url( $url ) . '" alt="' . esc_attr( $alt ) . '" /></figure>';
			}
		}
	}

	if ( ! $blocks ) {
		WP_CLI::warning( "{$post_id} {$post->post_name}: nothing to import" );
		continue;
	}

	$excerpt = $paragraphs ? wp_trim_words( $paragraphs[0], 28, '…' ) : '';

	$update = array(
		'ID'           => $post_id,
		'post_content' => wp_slash( implode( "\n\n", $blocks ) ),
		'post_excerpt' => wp_slash( $excerpt ),
	);

	if ( ! empty( $live['date'] ) ) {
		$update['post_date']     = $live['date'];
		$update['post_date_gmt'] = get_gmt_from_date( $live['date'] );
	}

	$result = wp_update_post( $update, true );
	if ( is_wp_error( $result ) ) {
		WP_CLI::warning( "{$post_id}: update failed — " . $result->get_error_message() );
		continue;
	}

	update_post_meta( $post_id, '_gsm_live_source', (int) $cfg['live'] );
	$total++;

	WP_CLI::log( sprintf(
		'%d %s: %d block(s), %d paragraph(s), from live #%d (%s)',
		$post_id, $post->post_name, count( $blocks ), count( $paragraphs ), $cfg['live'], $live['date']
	) );
}

WP_CLI::success( "Imported {$total} post(s) from the live site." );
