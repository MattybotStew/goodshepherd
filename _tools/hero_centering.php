<?php
/**
 * Centre the hero content in the VISIBLE hero area.
 *
 * The transparent header sits on top of the hero, so geometric centring puts
 * the copy ~header-height too high (it looked pinned under the nav). The
 * header covers the top of the hero:
 *
 *   desktop 176px (51 banner + 125 nav)
 *   tablet  190px
 *   mobile  177px
 *
 * So the top padding has to be `header + base` while the bottom stays `base`.
 * Any extra height then splits evenly, which preserves that offset, and the
 * copy lands in the middle of what the visitor actually sees below the nav.
 *
 *   desktop  min-height 560, padding 296 / 120
 *   tablet   min-height 520, padding 300 / 110
 *   mobile   min-height 480, padding 273 / 96
 *
 * Run:  wp eval-file _tools/hero_centering.php
 */

$PAGES = array(
	316  => 'About Us',
	317  => 'Programs & Services',
	2088 => 'Community Day Services',
	2090 => 'Residential Living',
	2091 => 'Health & Well Being',
	2127 => 'Community Engagement',
	2092 => 'Support GSM Foundation',
	2093 => 'Shepherd Endowment Society',
	2094 => 'Events',
	318  => 'News & Updates',
	2095 => 'Newsletters',
	2096 => 'Careers',
	319  => 'Contact Us',
);

// header height + breathing room, per breakpoint
$BREAKPOINTS = array(
	''       => array( 'min' => 560, 'top' => 296, 'bottom' => 120, 'side' => '24' ),   // >=1025, header 176
	'_tablet' => array( 'min' => 520, 'top' => 300, 'bottom' => 110, 'side' => '24' ), // 768-1024, header 190
	'_mobile' => array( 'min' => 480, 'top' => 273, 'bottom' => 96,  'side' => '20' ),  // <=767, header 177
);

function gsm_pad( $t, $r, $b, $l ) {
	return array( 'unit' => 'px', 'top' => (string) $t, 'right' => (string) $r, 'bottom' => (string) $b, 'left' => (string) $l, 'isLinked' => false );
}

foreach ( $PAGES as $page_id => $label ) {
	$raw = get_post_meta( $page_id, '_elementor_data', true );
	if ( ! $raw ) {
		WP_CLI::warning( "{$page_id} {$label}: no data" );
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

		foreach ( $BREAKPOINTS as $suffix => $bp ) {
			$s[ 'min_height' . $suffix ] = array( 'unit' => 'px', 'size' => $bp['min'], 'sizes' => array() );
			$s[ 'padding' . $suffix ]    = gsm_pad( $bp['top'], $bp['side'], $bp['bottom'], $bp['side'] );
		}

		$s['flex_justify_content'] = 'center';

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

	WP_CLI::log( "{$page_id} {$label}: hero centred below the header" );
}

WP_CLI::success( 'Sub-page heroes centred in the visible area.' );
