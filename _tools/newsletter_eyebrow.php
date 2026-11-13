<?php
/**
 * Add the missing "STAY CONNECTED" eyebrow above the Newsletter band heading.
 *
 * Template 2375 (Saved Templates → "Newsletter band") sits in Astra's
 * above-footer slot. The design has a small letterspaced eyebrow above the
 * heading; the build shipped without it.
 *
 * Inserts a heading widget (`nl_eyebrow`) as the first child of `nlleft`,
 * styled by rule 2 of this script. Idempotent.
 *
 * Run:  wp eval-file _tools/newsletter_eyebrow.php
 */

$TEMPLATE_ID = 2375;
$EYEBROW_ID  = 'nl_eyebrow';
$TEXT        = 'STAY CONNECTED';

$raw = get_post_meta( $TEMPLATE_ID, '_elementor_data', true );
if ( ! $raw ) {
	WP_CLI::error( 'Newsletter template has no _elementor_data' );
}

$data = json_decode( $raw, true );
if ( ! is_array( $data ) ) {
	WP_CLI::error( 'Could not decode _elementor_data' );
}

$inserted = false;

$walk = function ( array &$nodes ) use ( &$walk, &$inserted, $EYEBROW_ID, $TEXT ) {
	foreach ( $nodes as &$node ) {
		if ( ! is_array( $node ) ) {
			continue;
		}

		if ( isset( $node['id'] ) && 'nlleft' === $node['id'] ) {
			$children = isset( $node['elements'] ) && is_array( $node['elements'] ) ? $node['elements'] : array();

			foreach ( $children as $child ) {
				if ( isset( $child['id'] ) && $EYEBROW_ID === $child['id'] ) {
					return true; // already present
				}
			}

			$eyebrow = array(
				'id'         => $EYEBROW_ID,
				'elType'     => 'widget',
				'widgetType' => 'heading',
				'settings'   => array(
					'title'       => $TEXT,
					'header_size' => 'div',
					'align'       => 'left',
					'_element_class' => 'gsm-nl-eyebrow',
					'title_color' => '#9FD0FF',
					'typography_typography' => 'custom',
					'typography_font_size'  => array( 'unit' => 'px', 'size' => 12, 'sizes' => array() ),
					'typography_font_weight' => '700',
					'typography_letter_spacing' => array( 'unit' => 'px', 'size' => 1.6, 'sizes' => array() ),
					'typography_text_transform' => 'uppercase',
					'_margin' => array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '12', 'left' => '0', 'isLinked' => false ),
				),
				'elements'   => array(),
				'isInner'    => false,
			);

			array_unshift( $children, $eyebrow );
			$node['elements'] = $children;
			$inserted = true;
			return true;
		}

		if ( ! empty( $node['elements'] ) && $walk( $node['elements'] ) ) {
			return true;
		}
	}
	return false;
};

$walk( $data );

if ( ! $inserted ) {
	WP_CLI::log( 'Eyebrow already present — nothing to insert.' );
} else {
	update_post_meta( $TEMPLATE_ID, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $TEMPLATE_ID, '_elementor_css' );
	delete_post_meta( $TEMPLATE_ID, '_elementor_element_cache' );
	WP_CLI::log( 'Eyebrow widget inserted into nlleft.' );
}

// Spacing: the band heading sits tight under the eyebrow.
$css   = wp_get_custom_css();
$marker = 'GSM newsletter eyebrow';

if ( false === strpos( $css, $marker ) ) {
	$add = "\n/* {$marker} */\n.elementor-element-nl_eyebrow .elementor-heading-title{color:#9FD0FF!important;font-size:12px!important;font-weight:700!important;letter-spacing:1.6px!important;text-transform:uppercase;margin:0 0 12px!important;}\n";
	wp_update_custom_css_post( $css . $add );
	WP_CLI::log( 'Eyebrow CSS added.' );
}

WP_CLI::success( 'Newsletter eyebrow in place.' );
