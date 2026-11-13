<?php
/**
 * Remove the wire's "Placeholder photo — …" captions.
 *
 * Three program pages carry a caption widget left over from the prototype:
 * Residential, Health & Well Being and Community Engagement. The photos are
 * self-explanatory, so the captions are deleted rather than reworded — that is
 * what removes the placeholder text from the rendered page.
 *
 * Idempotent: does nothing once the widgets are gone.
 *
 * Run:  wp eval-file _tools/remove_placeholder_captions.php
 */

global $wpdb;

$ids = $wpdb->get_col(
	"SELECT post_id FROM {$wpdb->postmeta}
	 WHERE meta_key = '_elementor_data'
	   AND meta_value LIKE '%Placeholder photo%'"
);

if ( ! $ids ) {
	WP_CLI::success( 'No placeholder captions found.' );
	return;
}

$removed_total = 0;

foreach ( $ids as $post_id ) {
	$raw = get_post_meta( $post_id, '_elementor_data', true );
	if ( ! $raw ) {
		continue;
	}

	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) ) {
		WP_CLI::warning( "{$post_id}: bad JSON" );
		continue;
	}

	$removed = 0;

	$strip = function ( array &$nodes ) use ( &$strip, &$removed ) {
		foreach ( $nodes as $i => &$node ) {
			if ( ! is_array( $node ) ) {
				continue;
			}

			$settings = isset( $node['settings'] ) && is_array( $node['settings'] ) ? $node['settings'] : array();
			$text     = (string) ( $settings['editor'] ?? '' );

			if ( false !== strpos( $text, 'Placeholder photo' ) ) {
				WP_CLI::log( sprintf( '  %s: removed widget %s', $post_id ?? '', $node['id'] ?? '?' ) );
				unset( $nodes[ $i ] );
				$removed++;
				continue;
			}

			if ( ! empty( $node['elements'] ) ) {
				$strip( $node['elements'] );
			}
		}
		$nodes = array_values( $nodes );
	};

	$strip( $data );

	if ( ! $removed ) {
		continue;
	}

	update_post_meta( $post_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $post_id, '_elementor_css' );
	delete_post_meta( $post_id, '_elementor_element_cache' );
	delete_post_meta( $post_id, '_elementor_page_assets' );

	$removed_total += $removed;
	WP_CLI::log( "{$post_id}: {$removed} caption widget(s) removed" );
}

WP_CLI::success( "Removed {$removed_total} placeholder caption(s)." );
