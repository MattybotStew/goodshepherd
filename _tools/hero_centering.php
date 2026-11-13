<?php
/**
 * Vertically centre the hero content on every inner page.
 *
 * The heroes already used `justify-content: center`, but the padding was
 * asymmetric (140 top / 96 bottom), which pushed the copy ~22px below the true
 * centre — visible as a heavier gap above the headline than below it. Heights
 * also varied (480 / 520 / 560) for no design reason.
 *
 * This sets one rhythm across the 13 sub-pages: min-height 520, symmetric
 * padding (120 / 120 desktop, 110 tablet, 96 mobile), content centred.
 *
 * The single-post hero is handled by _tools/build_post_template.php.
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

$MIN_HEIGHT = 520;

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

		$left  = $s['padding']['left']  ?? '24';
		$right = $s['padding']['right'] ?? '24';

		$s['min_height']          = array( 'unit' => 'px', 'size' => $MIN_HEIGHT, 'sizes' => array() );
		$s['min_height_mobile']   = array( 'unit' => 'px', 'size' => 420, 'sizes' => array() );
		$s['flex_justify_content'] = 'center';
		$s['padding']             = gsm_pad( 120, $right, 120, $left );
		$s['padding_tablet']      = gsm_pad( 110, $right, 110, $left );
		$s['padding_mobile']      = gsm_pad( 96, '20', 96, '20' );

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

	WP_CLI::log( "{$page_id} {$label}: hero centred, min-height {$MIN_HEIGHT}" );
}

WP_CLI::success( 'Sub-page heroes centred.' );
