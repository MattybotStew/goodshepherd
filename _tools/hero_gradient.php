<?php
/**
 * Replace the photo hero on News and Events with a gradient.
 *
 * The two pages were reusing the same shared hero.jpg, which made them look
 * identical to Home and put white type over a busy photograph. A brand gradient
 * is calmer, loads instantly and keeps the hero type readable by construction.
 *
 * Only the `hero` container on each page is touched; height, padding and the
 * inner content stay exactly as they are.
 *
 * Run:  wp eval-file _tools/hero_gradient.php
 */

$PAGES = array(
	318  => 'News & Updates',
	2094 => 'Events',
);

foreach ( $PAGES as $page_id => $label ) {
	$raw = get_post_meta( $page_id, '_elementor_data', true );
	if ( ! $raw ) {
		WP_CLI::warning( "{$page_id} {$label}: no _elementor_data" );
		continue;
	}

	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) ) {
		WP_CLI::warning( "{$page_id} {$label}: bad JSON" );
		continue;
	}

	$done = false;

	foreach ( $data as &$node ) {
		if ( ! is_array( $node ) || 'hero' !== ( $node['id'] ?? '' ) ) {
			continue;
		}

		$s = isset( $node['settings'] ) && is_array( $node['settings'] ) ? $node['settings'] : array();

		// drop the photo + the dark overlay that existed to tame it
		unset( $s['background_image'], $s['background_overlay_color'], $s['background_overlay_opacity'], $s['background_overlay_background'], $s['background_position'], $s['background_repeat'], $s['background_size'] );

		$s['background_background']          = 'gradient';
		$s['background_color']               = '#002A4E';
		$s['background_color_b']             = '#0C4E86';
		$s['background_color_stop']          = array( 'unit' => '%', 'size' => 0, 'sizes' => array() );
		$s['background_color_b_stop']        = array( 'unit' => '%', 'size' => 100, 'sizes' => array() );
		$s['background_gradient_type']       = 'linear';
		$s['background_gradient_angle']      = array( 'unit' => 'deg', 'size' => 160, 'sizes' => array() );
		$s['background_gradient_position']   = 'center center';

		$node['settings'] = $s;
		$done = true;
	}

	if ( ! $done ) {
		WP_CLI::warning( "{$page_id} {$label}: hero container not found" );
		continue;
	}

	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $page_id, '_elementor_css' );
	delete_post_meta( $page_id, '_elementor_element_cache' );
	delete_post_meta( $page_id, '_elementor_page_assets' );

	WP_CLI::log( "{$page_id} {$label}: hero switched to gradient" );
}

WP_CLI::success( 'Hero gradients applied.' );
