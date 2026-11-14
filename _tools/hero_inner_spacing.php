<?php
/**
 * Sub-page hero inner spacing, matched to the wire (src/components/Layout.css).
 *
 *   H1 -> lede   20px   (`.home-hero h1 { margin: 0 auto 20px }`; was 16)
 *   under lede    0     (the lede is the last element; the theme's 1.6em <p>
 *                        margin was adding ~30px of hidden space under it)
 *
 * Only `hero_h1._margin` and `hero_p.paragraph_spacing` are touched, so the
 * other patches on these pages (CTA band, News hub, gradients, hero padding)
 * survive. `_tools/build_pages.py` emits the same values for new builds.
 *
 * The 30px that used to sit under the lede is now real bottom padding in the
 * hero CSS block (`_tools/hero_centering_css.php`), so the copy keeps its
 * optical position.
 *
 * Run:  wp eval-file _tools/hero_inner_spacing.php
 */

$PAGES = array( 316, 317, 2088, 2090, 2091, 2127, 2092, 2093, 2094, 318, 2095, 2096, 319 );

function gsm_hero_spacing_walk( array &$nodes, array &$hits ) {
	foreach ( $nodes as &$n ) {
		if ( ! is_array( $n ) ) {
			continue;
		}
		$id = $n['id'] ?? '';
		if ( 'hero_h1' === $id ) {
			$n['settings']['_margin'] = array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '20', 'left' => '0', 'isLinked' => false );
			$hits[] = 'h1';
		} elseif ( 'hero_p' === $id ) {
			$n['settings']['paragraph_spacing'] = array( 'unit' => 'px', 'size' => 0, 'sizes' => array() );
			$hits[] = 'p';
		}
		if ( ! empty( $n['elements'] ) && is_array( $n['elements'] ) ) {
			gsm_hero_spacing_walk( $n['elements'], $hits );
		}
	}
}

foreach ( $PAGES as $page_id ) {
	$data = json_decode( (string) get_post_meta( $page_id, '_elementor_data', true ), true );
	if ( ! is_array( $data ) ) {
		WP_CLI::warning( "{$page_id}: no Elementor data" );
		continue;
	}
	$hits = array();
	gsm_hero_spacing_walk( $data, $hits );
	if ( count( $hits ) !== 2 ) {
		WP_CLI::warning( "{$page_id}: expected hero_h1 + hero_p, found " . implode( ',', $hits ) );
		continue;
	}
	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $page_id, '_elementor_element_cache' );
	delete_post_meta( $page_id, '_elementor_css' );
	( new Elementor\Core\Files\CSS\Post( $page_id ) )->update();
	WP_CLI::log( "{$page_id}: hero spacing 20 / 0" );
}

WP_CLI::success( 'Sub-page hero inner spacing applied.' );
