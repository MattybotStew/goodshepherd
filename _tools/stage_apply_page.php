<?php
/**
 * Apply a generated Elementor page JSON on a host where apply_elementor.sh is
 * not available (stage/WP Engine).
 *
 *   wp eval-file _tools/stage_apply_page.php <post_id> <json_path>
 *
 * Mirrors apply_elementor.sh: write _elementor_data, drop the element cache,
 * clear Elementor's CSS, then force a rebuild of every builder document's CSS
 * (clearing without regenerating silently strips styling from every other
 * page — see the comment in apply_elementor.sh).
 */

$post_id = isset( $args[0] ) ? (int) $args[0] : 0;
$path    = isset( $args[1] ) ? $args[1] : '';
if ( ! $post_id || ! $path || ! file_exists( $path ) ) {
    fwrite( STDERR, "usage: wp eval-file stage_apply_page.php <post_id> <json_path>\n" );
    exit( 1 );
}

$json = file_get_contents( $path );
if ( false === strpos( $json, '"elType"' ) ) {
    fwrite( STDERR, "refusing to write: not Elementor data\n" );
    exit( 1 );
}
if ( false !== strpos( $json, 'goodshepherd.local' ) ) {
    fwrite( STDERR, "refusing to write: contains the Local host\n" );
    exit( 1 );
}
if ( get_post_meta( $post_id, '_elementor_edit_mode', true ) !== 'builder' ) {
    fwrite( STDERR, "refusing to write: post $post_id is not in Elementor builder mode\n" );
    exit( 1 );
}

update_post_meta( $post_id, '_elementor_data', wp_slash( $json ) );
delete_post_meta( $post_id, '_elementor_element_cache' );

$ids = get_posts( array(
    'post_type'      => 'any',
    'posts_per_page' => -1,
    'meta_key'       => '_elementor_edit_mode',
    'meta_value'     => 'builder',
    'fields'         => 'ids',
) );

\Elementor\Plugin::instance()->files_manager->clear_cache();
foreach ( $ids as $eid ) {
    delete_post_meta( $eid, '_elementor_css' );
}
( new \Elementor\Core\Files\CSS\Post( $post_id ) )->update();

$upload = wp_upload_dir();
$css    = trailingslashit( $upload['basedir'] ) . 'elementor/css/post-' . $post_id . '.css';
if ( ! file_exists( $css ) ) {
    fwrite( STDERR, "ERROR: $css was not generated\n" );
    exit( 1 );
}

wp_cache_flush();
echo "applied page $post_id from $path (css " . filesize( $css ) . " bytes)\n";
