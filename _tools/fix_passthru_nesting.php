<?php
/**
 * Repair WebP "Pass Thru" URL nesting in Elementor data.
 *
 * Storing already-wrapped webpc-passthru.php?src=... URLs means the render-time
 * converter wraps them AGAIN on the next save, producing
 *   passthru.php?src=passthru.php?src=passthru.php?src=...jpg&nocache=1&nocache=1
 * which the converter cannot resolve, so it serves the original JPG/PNG.
 *
 * collapse every passthru wrapper back to the clean uploads URL and drop the
 * duplicated &nocache params, so the converter wraps exactly once at render.
 *
 * Run: wp eval-file _tools/fix_passthru_nesting.php
 */

global $wpdb;
$ids = $wpdb->get_col(
    "SELECT DISTINCT post_id FROM {$wpdb->postmeta}
     WHERE meta_key = '_elementor_data' AND meta_value LIKE '%webpc-passthru.php%'"
);

$fix = 0;
foreach ( $ids as $id ) {
    $raw = get_post_meta( $id, '_elementor_data', true );
    if ( ! $raw ) {
        continue;
    }
    $prefix = WP_CONTENT_URL . '/webpc-passthru.php?src=';
    $clean  = str_replace( $prefix, '', $raw );
    $clean  = str_replace( array( '&amp;nocache=1', '&nocache=1' ), '', $clean );
    if ( $clean === $raw ) {
        continue;
    }
    update_post_meta( $id, '_elementor_data', wp_slash( $clean ) );
    delete_post_meta( $id, '_elementor_element_cache' );
    delete_post_meta( $id, '_elementor_css' );
    echo "fixed post {$id}\n";
    $fix++;
}
echo "total fixed: {$fix}\n";
