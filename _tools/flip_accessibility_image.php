<?php
/**
 * Flip the About page Accessibility section so the photo sits on the left.
 *
 * The section is `accessibility_row` with two children: the copy column and the
 * image column. `row-reverse` swaps them visually on desktop while leaving the
 * DOM order (copy first) intact for screen readers and keyboard order.
 *
 * Desktop only: mobile already stacks via flex_direction_mobile = column.
 *
 * Run:  wp eval-file _tools/flip_accessibility_image.php
 */

$PAGE_ID = 316; // About Us

$raw = get_post_meta( $PAGE_ID, '_elementor_data', true );
if ( ! $raw ) {
	WP_CLI::error( 'About page has no _elementor_data' );
}

$data = json_decode( $raw, true );
if ( ! is_array( $data ) ) {
	WP_CLI::error( 'Could not decode _elementor_data' );
}

$found = false;

$walk = function ( array &$nodes, $id ) use ( &$walk, &$found ) {
	foreach ( $nodes as &$node ) {
		if ( ! is_array( $node ) ) {
			continue;
		}
		if ( isset( $node['id'] ) && $id === $node['id'] ) {
			if ( ! isset( $node['settings'] ) || ! is_array( $node['settings'] ) ) {
				$node['settings'] = array();
			}
			$node['settings']['flex_direction'] = 'row-reverse';
			// Keep the tablet/mobile stacks pointing the right way.
			$node['settings']['flex_direction_tablet'] = 'row-reverse';
			$node['settings']['flex_direction_mobile']  = 'column';
			$found = true;
			return true;
		}
		if ( ! empty( $node['elements'] ) && $walk( $node['elements'], $id ) ) {
			return true;
		}
	}
	return false;
};

$walk( $data, 'accessibility_row' );

if ( ! $found ) {
	WP_CLI::error( 'accessibility_row container not found' );
}

update_post_meta( $PAGE_ID, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
delete_post_meta( $PAGE_ID, '_elementor_css' );
delete_post_meta( $PAGE_ID, '_elementor_element_cache' );
delete_post_meta( $PAGE_ID, '_elementor_page_assets' );

WP_CLI::success( 'Accessibility section flipped: image now on the left.' );
