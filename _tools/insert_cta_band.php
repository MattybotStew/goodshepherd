<?php
/**
 * Insert (or replace) the global `gsm_cta_band` on every content page.
 *
 * The band is the photo-overlay "Support GSM Foundation" section with Donate /
 * Volunteer / Careers cards. It was designed into every content page but is
 * missing in the build, so this applier inserts the fragment when absent and
 * replaces it when the page already carries one. Home is excluded on purpose.
 *
 * The fragment must be host-agnostic (root-relative upload URLs) so the same
 * JSON can be applied to Local and stage.
 *
 * Usage:
 *   wp eval-file _tools/insert_cta_band.php /tmp/cta_band.json
 */

$fragment_path = isset( $args[0] ) ? $args[0] : '/tmp/cta_band.json';

if ( ! file_exists( $fragment_path ) ) {
	WP_CLI::error( "Fragment not found: {$fragment_path}" );
}

$fragment = json_decode( file_get_contents( $fragment_path ), true );
if ( ! is_array( $fragment ) || 'gsm_cta_band' !== ( $fragment['id'] ?? '' ) ) {
	WP_CLI::error( 'Fragment is not a gsm_cta_band container.' );
}

if ( false !== strpos( file_get_contents( $fragment_path ), 'goodshepherd.local' ) ) {
	WP_CLI::error( 'Fragment contains absolute Local URLs — it must stay host-agnostic.' );
}

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
	2095 => 'Newsletters & Family Resources',
	2096 => 'Careers',
	319  => 'Contact Us',
);

foreach ( $PAGES as $page_id => $label ) {
	$raw = get_post_meta( $page_id, '_elementor_data', true );
	if ( ! $raw ) {
		WP_CLI::warning( "{$page_id} {$label}: no _elementor_data" );
		continue;
	}

	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) ) {
		WP_CLI::warning( "{$page_id} {$label}: could not decode JSON" );
		continue;
	}

	$replaced = false;
	foreach ( $data as $i => $node ) {
		if ( isset( $node['id'] ) && 'gsm_cta_band' === $node['id'] ) {
			$data[ $i ] = $fragment;
			$replaced = true;
			break;
		}
	}

	if ( ! $replaced ) {
		$data[] = $fragment;
	}

	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $page_id, '_elementor_css' );
	delete_post_meta( $page_id, '_elementor_element_cache' );
	delete_post_meta( $page_id, '_elementor_page_assets' );

	WP_CLI::log( "{$page_id} {$label}: " . ( $replaced ? 'band replaced' : 'band inserted' ) );
}

WP_CLI::success( 'gsm_cta_band applied.' );
