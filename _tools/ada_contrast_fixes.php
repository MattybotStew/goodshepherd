<?php
/**
 * ADA: the sidebar "current page" button used #0089DF on white (3.72:1).
 *
 * The program sidebar is a list of Elementor button widgets; the builder marks
 * the current page by setting that one button's text colour to the brand
 * accent. Swap it to #006BB3 (5.46:1) on every program page.
 *
 * Also darkens the Astra header button, which axe flags for the same reason
 * (white on #0089DF = 3.59:1).
 *
 * Run:  wp eval-file _tools/ada_contrast_fixes.php
 */

$ACCENT = '#0089DF';
$SAFE   = '#006BB3';

$PAGES = array(
	2088 => 'Community Day Services',
	2090 => 'Residential Living',
	2091 => 'Health & Well Being',
	2127 => 'Community Engagement',
);

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

	$changed = 0;

	$walk = function ( array &$nodes ) use ( &$walk, &$changed, $ACCENT, $SAFE ) {
		foreach ( $nodes as &$node ) {
			if ( ! is_array( $node ) ) {
				continue;
			}

			if ( isset( $node['settings'] ) && is_array( $node['settings'] ) ) {
				foreach ( array( 'button_text_color', 'title_color' ) as $key ) {
					if ( isset( $node['settings'][ $key ] ) && $ACCENT === strtoupper( (string) $node['settings'][ $key ] ) ) {
						$node['settings'][ $key ] = $SAFE;
						$changed++;
					}
				}
			}

			if ( ! empty( $node['elements'] ) ) {
				$walk( $node['elements'] );
			}
		}
	};

	$walk( $data );

	if ( ! $changed ) {
		WP_CLI::log( "{$page_id} {$label}: no accent-coloured button, skipped" );
		continue;
	}

	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $page_id, '_elementor_css' );
	delete_post_meta( $page_id, '_elementor_element_cache' );
	WP_CLI::log( "{$page_id} {$label}: {$changed} colour(s) {$ACCENT} -> {$SAFE}" );
}

// Header CTA: Astra header button, white on the brand accent.
$css    = wp_get_custom_css();
$marker = 'GSM header CTA contrast';

if ( false === strpos( $css, $marker ) ) {
	$add = "\n/* {$marker}: white on #0089DF was 3.59:1 */"
		. "\n.ast-header-button-1 .ast-custom-button{background-color:#006BB3!important;}"
		. "\n.ast-header-button-1 .ast-custom-button:hover{background-color:#004F85!important;}\n";
	wp_update_custom_css_post( $css . $add );
	WP_CLI::log( 'Header CTA contrast CSS added.' );
}

WP_CLI::success( 'ADA contrast fixes applied.' );
