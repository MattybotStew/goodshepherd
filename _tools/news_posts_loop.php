<?php
/**
 * /news (page 318): replace the four hand-built cards with an automatic post list.
 *
 *   wp eval-file _tools/news_posts_loop.php [path/to/news_posts_widget.json]
 *
 * Before: nw_grid held four static cards (nw_card0-3) with hard-coded titles,
 * dates and links, in no particular order. A new post never appeared on /news.
 *
 * After: one Elementor Pro Posts widget (Classic skin, _tools/news_posts_widget.json)
 * lists every published post newest first, 8 per page, numbered pagination.
 * Editable in Elementor; no shortcode, no HTML widget.
 *
 * Content: the cards' summaries were the client-approved hub copy, so they are
 * copied onto the posts as excerpts (Posts > Edit > Excerpt) and the page reads
 * the same. New posts use their own excerpt, or the first 30 words.
 *
 * Idempotent: re-running finds nw_posts already in place and only refreshes CSS.
 * Supersedes the card part of _tools/fix_news_hub.php.
 */

$json_path = $args[0] ?? ( ( getenv( 'GSM_REPO' ) ?: getenv( 'HOME' ) . '/Developer/goodshepherd' ) . '/_tools/news_posts_widget.json' );
$widget    = json_decode( (string) file_get_contents( $json_path ), true );
if ( ! is_array( $widget ) || 'posts' !== ( $widget['widgetType'] ?? '' ) ) {
	WP_CLI::error( "Cannot read widget definition at {$json_path}" );
}
unset( $widget['_doc'] );

$page_id = 318;
$data    = json_decode( (string) get_post_meta( $page_id, '_elementor_data', true ), true );
if ( ! is_array( $data ) ) {
	WP_CLI::error( 'Page 318 has no Elementor data' );
}

/* ---------- 1. excerpts from the current cards (only on the first run) ---------- */

$cards = array();
function gsm_news_collect( array $nodes, array &$cards ) {
	foreach ( $nodes as $n ) {
		if ( preg_match( '/^nw_card(\d)$/', $n['id'] ?? '', $m ) ) {
			$c = array();
			foreach ( $n['elements'] ?? array() as $w ) {
				if ( 0 === strpos( $w['id'], 'nw_e' ) ) {
					$c['excerpt'] = trim( wp_strip_all_tags( $w['settings']['editor'] ?? '' ) );
				}
				if ( 0 === strpos( $w['id'], 'nw_l' ) ) {
					$c['url'] = $w['settings']['link']['url'] ?? '';
				}
			}
			$cards[] = $c;
		}
		gsm_news_collect( $n['elements'] ?? array(), $cards );
	}
}
gsm_news_collect( $data, $cards );

foreach ( $cards as $c ) {
	if ( empty( $c['url'] ) || empty( $c['excerpt'] ) ) {
		continue;
	}
	$slug = basename( untrailingslashit( $c['url'] ) );
	$post = get_page_by_path( $slug, OBJECT, 'post' );
	if ( ! $post ) {
		WP_CLI::warning( "No post for card link {$c['url']}" );
		continue;
	}
	if ( $post->post_excerpt !== $c['excerpt'] ) {
		wp_update_post( array( 'ID' => $post->ID, 'post_excerpt' => $c['excerpt'] ) );
		WP_CLI::log( "Excerpt set on {$post->ID} ({$slug})" );
	}
}

/* ---------- 2. swap nw_grid for the Posts widget ---------- */

$swapped = false;
function gsm_news_swap( array &$nodes, array $widget, bool &$swapped ) {
	foreach ( $nodes as $i => &$n ) {
		if ( 'nw_grid' === ( $n['id'] ?? '' ) ) {
			$nodes[ $i ] = $widget;
			$swapped     = true;
			return;
		}
		if ( 'nw_posts' === ( $n['id'] ?? '' ) ) {
			$nodes[ $i ] = $widget; // refresh settings from the JSON
			$swapped     = true;
			return;
		}
		if ( ! empty( $n['elements'] ) ) {
			gsm_news_swap( $n['elements'], $widget, $swapped );
		}
	}
}
gsm_news_swap( $data, $widget, $swapped );
if ( ! $swapped ) {
	WP_CLI::error( 'Neither nw_grid nor nw_posts found on page 318' );
}

update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
delete_post_meta( $page_id, '_elementor_element_cache' );
delete_post_meta( $page_id, '_elementor_css' );
( new Elementor\Core\Files\CSS\Post( $page_id ) )->update();
WP_CLI::log( 'Page 318: nw_grid -> nw_posts (Posts widget)' );

/* ---------- 3. CSS: same card behaviour as before ---------- */

$css   = wp_get_custom_css();
$start = '/* GSM news hub */';
$end   = '/* end GSM news hub */';
$from  = strpos( $css, $start );
$to    = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

// Doubled class: Elementor Pro prints its Posts CSS later in the page
// (`.elementor-post__text{display:block}`), so equal specificity loses.
$p   = '.elementor-element.elementor-element-nw_posts .elementor-posts-container';
$add = "\n/* GSM news hub */\n" .
	"/* cards from the Posts widget (news_posts_loop.php): equal height, date above title,\n" .
	"   Read More pinned to the bottom and stretched over the whole card */\n" .
	"{$p} .elementor-post{position:relative;display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease;}\n" .
	"{$p} .elementor-post__text{display:flex;flex-direction:column;flex:1 1 auto;}\n" .
	"{$p} .elementor-post__meta-data{order:-1;}\n" .
	"{$p} .elementor-post__excerpt{flex-grow:1;}\n" .
	"{$p} .elementor-post__excerpt p{margin:0;}\n" .
	"{$p} .elementor-post__title a,{$p} .elementor-post__read-more{color:inherit;text-decoration:none;}\n" .
	"{$p} .elementor-post:hover .elementor-post__read-more,{$p} .elementor-post:hover .elementor-post__title a{color:#004F85;}\n" .
	"{$p} .elementor-post:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,42,78,.10);}\n" .
	"{$p} .elementor-post:focus-within{outline:2px solid #006BB3;outline-offset:4px;}\n" .
	"{$p} .elementor-post__read-more{position:static;}\n" .
	"{$p} .elementor-post__read-more::after{content:\"\";position:absolute;inset:0;}\n" .
		"/* pagination: 44px number buttons, current page filled */\n" .
	"{$p} ~ .elementor-pagination,.elementor-element-nw_posts .elementor-pagination{display:flex;justify-content:center;gap:8px;margin-top:40px;}\n" .
	".elementor-element-nw_posts .elementor-pagination .page-numbers{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;margin:0!important;padding:0 12px;border:1px solid #C8D4E0;border-radius:8px;background:#FFFFFF;color:#002A4E;font-weight:700;font-size:15px;text-decoration:none;}\n" .
	".elementor-element-nw_posts .elementor-pagination a.page-numbers:hover{border-color:#006BB3;color:#006BB3;}\n" .
	".elementor-element-nw_posts .elementor-pagination .page-numbers.current{background:#002A4E;border-color:#002A4E;color:#FFFFFF;}\n" .
	"/* end GSM news hub */\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );
WP_CLI::success( 'News page now lists posts automatically.' );
