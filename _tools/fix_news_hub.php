<?php
/*
 * SUPERSEDED 2026-11-13 by _tools/news_posts_loop.php: /news now lists posts with an
 * Elementor Pro Posts widget. Do not re-run this script; it targets the old
 * hand-built nw_card0-3 cards, which no longer exist, and its CSS block marker
 * ("GSM news hub") is now owned by news_posts_loop.php.
 */
/**
 * Fix the /news/ hub (page 318).
 *
 * 1. Drop the duplicated "Our Impact" stats block — it belongs on Home and
 *    pushed the actual news below the fold.
 * 2. Drop the navy "Help Make Home Happen / Donate Now" band — it sits right
 *    above the global Support GSM Foundation band, so the page asked twice.
 * 3. Give each card a date + category line above the headline.
 * 4. Make the whole card clickable by stretching the Read More link over it,
 *    with a hover lift.
 *
 * Idempotent: the removals are by node id, the meta widgets are inserted only
 * when missing.
 *
 * Run:  wp eval-file _tools/fix_news_hub.php
 */

$PAGE_ID = 318;

$META = array(
	'nw_card0' => array( 'date' => 'July 20, 2026', 'term' => 'News' ),
	'nw_card1' => array( 'date' => 'September 14, 2025', 'term' => 'News' ),
	'nw_card2' => array( 'date' => 'June 28, 2026', 'term' => 'News' ),
	'nw_card3' => array( 'date' => 'May 21, 2026', 'term' => 'News' ),
);

$raw = get_post_meta( $PAGE_ID, '_elementor_data', true );
if ( ! $raw ) {
	WP_CLI::error( 'News page has no _elementor_data' );
}

$data = json_decode( $raw, true );
if ( ! is_array( $data ) ) {
	WP_CLI::error( 'Could not decode _elementor_data' );
}

// ---------------------------------------------------------------- 1 + 2: remove
$before = count( $data );
$data   = array_values( array_filter( $data, function ( $node ) {
	return ! in_array( $node['id'] ?? '', array( 'nw_impact', 'nw_cta' ), true );
} ) );
$removed = $before - count( $data );

// ---------------------------------------------------------------- 3 + 4: cards
$cards_done = 0;

/**
 * Hero copy: the client wants "What's Happening at GSM" and its lede in the
 * hero rather than duplicated further down the page, so the cards section
 * keeps only its grid.
 */
function gsm_news_hero_copy( array &$nodes ) {
	$hero_text  = "What’s Happening at GSM";
	$hero_lede  = "<p>See how the men of GSM are learning, connecting, and thriving. Explore the new stories, events, and everyday moments your support helps make possible.</p>";
	$found = 0;

	$walk = function ( array &$list ) use ( &$walk, &$found, $hero_text, $hero_lede ) {
		foreach ( $list as &$node ) {
			if ( ! is_array( $node ) ) {
				continue;
			}
			$id = $node['id'] ?? '';

			if ( 'hero_h1' === $id ) {
				$node['settings']['title'] = $hero_text;
				$found++;
			}

			if ( 'hero_p' === $id ) {
				$node['settings']['editor'] = $hero_lede;
				$found++;
			}

			// drop the now-duplicated section heading + lede
			if ( in_array( $id, array( 'nw_cards_h2', 'nw_cards_p' ), true ) ) {
				$node['__remove'] = true;
			}

			if ( ! empty( $node['elements'] ) ) {
				$walk( $node['elements'] );
			}
		}
	};

	$walk( $nodes );

	// strip marked widgets
	$prune = function ( array &$list ) use ( &$prune ) {
		foreach ( $list as $i => &$node ) {
			if ( ! is_array( $node ) ) {
				continue;
			}
			if ( ! empty( $node['__remove'] ) ) {
				unset( $list[ $i ] );
				continue;
			}
			if ( ! empty( $node['elements'] ) ) {
				$prune( $node['elements'] );
			}
		}
		$list = array_values( $list );
	};
	$prune( $nodes );

	return $found;
}

$hero_changed = gsm_news_hero_copy( $data );

$walk = function ( array &$nodes ) use ( &$walk, &$cards_done, $META ) {
	foreach ( $nodes as &$node ) {
		if ( ! is_array( $node ) ) {
			continue;
		}

		$id = $node['id'] ?? '';

		if ( isset( $META[ $id ] ) && 'container' === ( $node['elType'] ?? '' ) ) {
			$children = $node['elements'] ?? array();

			// Containers render their internal id as elementor-element-<id>; the
			// CSS below hooks those, so no custom class is needed.

			$has_meta = false;
			foreach ( $children as $child ) {
				if ( 0 === strpos( $child['id'] ?? '', 'nw_m' ) ) {
					$has_meta = true;
				}
			}

			if ( ! $has_meta ) {
				$widget = array(
					'id'         => 'nw_m' . substr( $id, -1 ),
					'elType'     => 'widget',
					'widgetType' => 'text-editor',
					'settings'   => array(
						'editor' => '<p>' . esc_html( $META[ $id ]['date'] . ' · ' . $META[ $id ]['term'] ) . '</p>',
						'text_color' => '#6B7280',
						'typography_typography'     => 'custom',
						'typography_font_size'      => array( 'unit' => 'px', 'size' => 13, 'sizes' => array() ),
						'typography_font_weight'    => '700',
						'typography_letter_spacing' => array( 'unit' => 'px', 'size' => 0.8, 'sizes' => array() ),
						'typography_text_transform' => 'uppercase',
						'_margin' => array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '8', 'left' => '0', 'isLinked' => false ),
					),
					'elements'   => array(),
					'isInner'    => false,
				);
				$node['elements'] = array_merge( array( $widget ), $children );
			}

			$cards_done++;
		}

		if ( ! empty( $node['elements'] ) ) {
			$walk( $node['elements'] );
		}
	}
};

$walk( $data );

update_post_meta( $PAGE_ID, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
delete_post_meta( $PAGE_ID, '_elementor_css' );
delete_post_meta( $PAGE_ID, '_elementor_element_cache' );
delete_post_meta( $PAGE_ID, '_elementor_page_assets' );

WP_CLI::log( "removed {$removed} section(s); cards updated: {$cards_done}; hero fields updated: {$hero_changed}" );

// ---------------------------------------------------------------- styling
$css   = wp_get_custom_css();
$start = '/* GSM news hub */';
$end   = '/* end GSM news hub */';

// Remove every copy: first start marker through last end marker.
$from = strpos( $css, $start );
$to   = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

$cards = ':is(.elementor-element-nw_card0,.elementor-element-nw_card1,.elementor-element-nw_card2,.elementor-element-nw_card3)';

$add = "\n/* GSM news hub */\n" .
	$cards . "{position:relative;transition:transform .18s ease,box-shadow .18s ease;}\n" .
	"@media (min-width:1025px){" . $cards . "{flex:1 1 0!important;min-width:0;}}\n" .
	$cards . ":hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,42,78,.10);}\n" .
	$cards . ":focus-within{outline:2px solid #006BB3;outline-offset:4px;}\n" .
	$cards . " .elementor-widget-button{position:static!important;}\n" .
	$cards . " .elementor-button-wrapper{position:static!important;}\n" .
	$cards . " .elementor-widget-button .elementor-button{position:static;}\n" .
	"/* stretch the Read More link over the whole card */\n" .
	$cards . " .elementor-widget-button .elementor-button::after{content:\"\";position:absolute;inset:0;height:auto!important;transform:none!important;}\n" .
	"/* end GSM news hub */\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );

WP_CLI::success( 'News hub fixed.' );
