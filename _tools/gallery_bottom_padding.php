<?php
/**
 * Add bottom padding to the article column on the program pages so the photo
 * gallery does not run flush into the band below it.
 *
 * The gallery is the last block inside `pg_content` (the article column of the
 * program template). Stage measured 0px from the last gallery image to the end
 * of the article, so the photos butted straight against the newsletter band.
 *
 * Only `pg_content` is touched, so the sidebar and every other section keep
 * their current spacing.
 *
 * Run:  _tools/wp.sh eval-file _tools/gallery_bottom_padding.php
 */

$PADDING = 64; // px, bottom only
$PAGES   = array(
	2088 => 'Community Day Services',
	2090 => 'Residential Living',
	2091 => 'Health & Well Being',
	2127 => 'Community Engagement',
);

/**
 * Walk the tree in place and set padding-bottom on the container whose id (or
 * settings._element_id) matches. Returns true once it has been applied.
 *
 * Mutates $nodes by reference — a value-returning helper would edit a copy and
 * silently save nothing.
 */
function gsm_pad_container( array &$nodes, $element_id, $bottom ) {
	foreach ( $nodes as &$node ) {
		if ( ! is_array( $node ) ) {
			continue;
		}

		$id_match   = isset( $node['id'] ) && $element_id === $node['id'];
		$elem_match = isset( $node['settings']['_element_id'] ) && $element_id === $node['settings']['_element_id'];

		if ( $id_match || $elem_match ) {
			if ( ! isset( $node['settings'] ) || ! is_array( $node['settings'] ) ) {
				$node['settings'] = array();
			}

			$padding = isset( $node['settings']['padding'] ) && is_array( $node['settings']['padding'] )
				? $node['settings']['padding']
				: array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '0', 'left' => '0', 'isLinked' => false );

			$padding['unit']     = 'px';
			$padding['bottom']   = (string) $bottom;
			$padding['isLinked'] = false;

			$node['settings']['padding'] = $padding;
			return true;
		}

		if ( ! empty( $node['elements'] ) && gsm_pad_container( $node['elements'], $element_id, $bottom ) ) {
			return true;
		}
	}
	return false;
}

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

	if ( ! gsm_pad_container( $data, 'pg_content', $PADDING ) ) {
		WP_CLI::warning( "{$page_id} {$label}: pg_content not found" );
		continue;
	}

	update_post_meta( $page_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );

	// Elementor caches per-post CSS and the element cache; drop both.
	delete_post_meta( $page_id, '_elementor_css' );
	delete_post_meta( $page_id, '_elementor_element_cache' );
	delete_post_meta( $page_id, '_elementor_page_assets' );

	WP_CLI::log( "{$page_id} {$label}: pg_content padding-bottom -> {$PADDING}px" );
}

WP_CLI::success( 'Gallery bottom padding applied.' );
