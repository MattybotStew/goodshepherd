<?php
/**
 * Make the program-page "Photo gallery" tiles square. Idempotent; safe to re-run.
 *
 *   ./_tools/wp.sh eval-file _tools/square_gallery_images.php
 *   # stage: upload this file, then
 *   wp eval-file /sites/goodshephe3dev/square_gallery_images.php --allow-root
 *
 * Each tile was an <img> at its photo's natural aspect ratio (`image_size: full`),
 * so a 2-up row mixed 4:3, 3:2 and portrait frames and the grid came out ragged
 * (measured 444x592 next to 444x333 at 1440).
 *
 * The fix is Elementor-native, no CSS: the image widget's own Image Resolution is
 * set to "Custom" with an 800x800 dimension. Elementor then serves a hard-cropped
 * square (bfi_thumb, crop=true), so every tile is square at any column width.
 *
 * 800px covers a 444px tile at ~2x. Generating a custom size writes one file per
 * photo into uploads; both Local and stage generate their own on first render.
 */

$SQUARE = array(
	'image_size'             => 'custom',
	'image_custom_dimension' => array( 'width' => 800, 'height' => 800 ),
);

$docs = get_posts( array(
	'post_type'      => 'page',
	'posts_per_page' => -1,
	'post_status'    => 'any',
	'meta_key'       => '_elementor_edit_mode',
	'meta_value'     => 'builder',
	'fields'         => 'ids',
) );

/**
 * @param array $nodes   Elementor elements, by reference.
 * @param int   $found   Gallery image widgets seen.
 * @param int   $changed Those that actually needed rewriting.
 */
function gsm_square_walk( array &$nodes, array $square, int &$found, int &$changed ) {
	foreach ( $nodes as &$n ) {
		if ( ! is_array( $n ) ) {
			continue;
		}
		$id = (string) ( $n['id'] ?? '' );
		if ( 'widget' === ( $n['elType'] ?? '' ) && 'image' === ( $n['widgetType'] ?? '' ) && preg_match( '/^gal_\d+$/', $id ) ) {
			$found++;
			$s = (array) ( $n['settings'] ?? array() );
			$dim = isset( $s['image_custom_dimension'] ) && is_array( $s['image_custom_dimension'] )
				? $s['image_custom_dimension']
				: array();
			$already = ( 'custom' === ( $s['image_size'] ?? '' ) )
				&& 800 === (int) ( $dim['width'] ?? 0 )
				&& 800 === (int) ( $dim['height'] ?? 0 );
			if ( ! $already ) {
				$n['settings'] = array_merge( $s, $square );
				$changed++;
			}
		}
		if ( ! empty( $n['elements'] ) && is_array( $n['elements'] ) ) {
			gsm_square_walk( $n['elements'], $square, $found, $changed );
		}
	}
}

$docs_written = 0;
$tiles_found  = 0;
$tiles_fixed  = 0;

foreach ( $docs as $doc_id ) {
	$data = json_decode( (string) get_post_meta( $doc_id, '_elementor_data', true ), true );
	if ( ! is_array( $data ) ) {
		continue;
	}
	$found = 0;
	$changed = 0;
	gsm_square_walk( $data, $SQUARE, $found, $changed );
	if ( ! $found ) {
		continue;
	}
	$tiles_found += $found;
	if ( ! $changed ) {
		WP_CLI::log( "{$doc_id}: {$found} gallery tiles already square" );
		continue;
	}
	update_post_meta( $doc_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $doc_id, '_elementor_element_cache' );
	delete_post_meta( $doc_id, '_elementor_css' );
	( new Elementor\Core\Files\CSS\Post( $doc_id ) )->update();
	WP_CLI::log( "{$doc_id}: {$changed} of {$found} gallery tiles set to an 800x800 square crop" );
	$docs_written++;
	$tiles_fixed += $changed;
}

WP_CLI::success( "{$docs_written} documents written, {$tiles_fixed} tiles changed ({$tiles_found} gallery tiles total)." );
