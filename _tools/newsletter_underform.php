<?php
/**
 * Add the under-form line to the Newsletter band (content doc Global!D21):
 * "No spam - just stories worth opening."
 *
 * Template 2375 (Saved Templates → "Newsletter band") sits in Astra's
 * above-footer slot on every page. Its right column `nlright` holds the field
 * label (`nllab`) and the SureForms form (`nlform`); nothing followed the form.
 *
 * Appends a text-editor widget (`nlnote`) to `nlright`, right after `nlform`.
 * All styling is in the widget's own settings, so the line stays editable in
 * Elementor (no CSS, no HTML widget). Idempotent; safe to re-run.
 *
 *   ./_tools/wp.sh eval-file _tools/newsletter_underform.php
 *   # stage, after a push (only if the push did not carry it):
 *   wp eval-file /sites/goodshephe3dev/newsletter_underform.php --allow-root
 */

$TEMPLATE_ID = 2375;
$NOTE_ID     = 'nlnote';
$TEXT        = 'No spam - just stories worth opening.';

$raw = get_post_meta( $TEMPLATE_ID, '_elementor_data', true );
if ( ! $raw ) {
	WP_CLI::error( 'Newsletter template has no _elementor_data' );
}

$data = json_decode( $raw, true );
if ( ! is_array( $data ) ) {
	WP_CLI::error( 'Could not decode _elementor_data' );
}

$state = 'missing'; // missing | present | inserted

$walk = function ( array &$nodes ) use ( &$walk, &$state, $NOTE_ID, $TEXT ) {
	foreach ( $nodes as &$node ) {
		if ( ! is_array( $node ) ) {
			continue;
		}

		if ( isset( $node['id'] ) && 'nlright' === $node['id'] ) {
			$children = isset( $node['elements'] ) && is_array( $node['elements'] ) ? $node['elements'] : array();

			foreach ( $children as $child ) {
				if ( isset( $child['id'] ) && $NOTE_ID === $child['id'] ) {
					$state = 'present';
					return true;
				}
			}

			$note = array(
				'id'         => $NOTE_ID,
				'elType'     => 'widget',
				'widgetType' => 'text-editor',
				'settings'   => array(
					'editor'                    => '<p>' . esc_html( $TEXT ) . '</p>',
					// White at 72% on the band's navy (#061a2c–#0a2740) is ~10:1.
					'text_color'                => 'rgba(255,255,255,0.72)',
					'typography_typography'     => 'custom',
					'typography_font_size'      => array( 'unit' => 'px', 'size' => 14, 'sizes' => array() ),
					'typography_line_height'    => array( 'unit' => 'em', 'size' => 1.5, 'sizes' => array() ),
					'paragraph_spacing'         => array( 'unit' => 'px', 'size' => 0, 'sizes' => array() ),
					'_margin'                   => array( 'unit' => 'px', 'top' => '12', 'right' => '0', 'bottom' => '0', 'left' => '24', 'isLinked' => false ),
				),
				'elements'   => array(),
				'isInner'    => false,
			);

			// Directly after the form; append if the form is not found.
			$out    = array();
			$placed = false;
			foreach ( $children as $child ) {
				$out[] = $child;
				if ( isset( $child['id'] ) && 'nlform' === $child['id'] ) {
					$out[]  = $note;
					$placed = true;
				}
			}
			if ( ! $placed ) {
				$out[] = $note;
			}

			$node['elements'] = $out;
			$state            = 'inserted';
			return true;
		}

		if ( ! empty( $node['elements'] ) && $walk( $node['elements'] ) ) {
			return true;
		}
	}
	return false;
};

$walk( $data );

if ( 'missing' === $state ) {
	WP_CLI::error( 'nlright not found in template 2375 — nothing changed.' );
}

if ( 'present' === $state ) {
	WP_CLI::success( 'Under-form line already present — nothing to insert.' );
	return;
}

update_post_meta( $TEMPLATE_ID, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
delete_post_meta( $TEMPLATE_ID, '_elementor_css' );
delete_post_meta( $TEMPLATE_ID, '_elementor_element_cache' );
if ( class_exists( '\Elementor\Plugin' ) ) {
	\Elementor\Plugin::$instance->files_manager->clear_cache();
}

WP_CLI::success( 'Under-form line inserted into nlright after nlform.' );
