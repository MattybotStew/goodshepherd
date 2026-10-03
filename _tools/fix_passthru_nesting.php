<?php
/**
 * Repair WebP "Pass Thru" URL nesting in stored content.
 *
 * The converter wraps uploads URLs with webpc-passthru.php?src=... at output
 * time. If a value is STORED already wrapped (e.g. Elementor data, or the
 * Additional CSS written by the background helper), the converter wraps it
 * AGAIN → passthru.php?src=passthru.php?src=...jpg&nocache=1&nocache=1, which
 * it cannot resolve, so the image fails (this broke the Home hero background).
 *
 * collapse every passthru wrapper back to the clean uploads URL and drop the
 * duplicated &nocache params. Stored values are read with $wpdb (unfiltered)
 * so we edit what is actually on disk, not the converter's rendered output.
 *
 * Run: wp eval-file _tools/fix_passthru_nesting.php
 */

global $wpdb;

$prefix = WP_CONTENT_URL . '/webpc-passthru.php?src=';
$clean  = function ( $value ) use ( $prefix ) {
    $value = str_replace( $prefix, '', $value );
    return str_replace( array( '&amp;nocache=1', '&nocache=1' ), '', $value );
};

$count = 0;

// 1) Elementor / postmeta (string meta, no serialization concerns here).
$meta = $wpdb->get_results(
    "SELECT meta_id, post_id, meta_value FROM {$wpdb->postmeta} WHERE meta_value LIKE '%webpc-passthru%'",
    ARRAY_A
);
$touched = array();
foreach ( $meta as $row ) {
    $new = $clean( $row['meta_value'] );
    if ( $new !== $row['meta_value'] ) {
        $wpdb->update( $wpdb->postmeta, array( 'meta_value' => $new ), array( 'meta_id' => $row['meta_id'] ) );
        $touched[ $row['post_id'] ] = true;
        $count++;
    }
}
foreach ( array_keys( $touched ) as $id ) {
    delete_post_meta( $id, '_elementor_element_cache' );
    delete_post_meta( $id, '_elementor_css' );
}

// 2) Post content (pages, posts, custom_css).
$posts = $wpdb->get_results(
    "SELECT ID, post_content FROM {$wpdb->posts} WHERE post_content LIKE '%webpc-passthru%'",
    ARRAY_A
);
foreach ( $posts as $p ) {
    $new = $clean( $p['post_content'] );
    if ( $new !== $p['post_content'] ) {
        $wpdb->update( $wpdb->posts, array( 'post_content' => $new ), array( 'ID' => $p['ID'] ) );
        clean_post_cache( $p['ID'] );
        echo "post {$p['ID']}\n";
        $count++;
    }
}

echo "cleaned {$count} stored value(s)\n";
