<?php
/**
 * Normalize internal links to WordPress' trailing-slash canonical form.
 *
 * Menu items and Elementor link fields were authored as relative paths without
 * a trailing slash (/about, /news/<slug>), so every click 301-redirected to
 * /about/ etc. Add the trailing slash to same-origin paths so internal links
 * resolve with a single 200. File URLs, #anchors, ?queries, external and
 * protocol-relative URLs are left alone.
 *
 * Run: wp eval-file _tools/normalize_internal_urls.php
 */

global $wpdb;

$normalize_link = function ( $u ) {
    $u = trim( $u );
    if ( '' === $u || '/' !== $u[0] || 0 === strpos( $u, '//' ) ) {
        return $u; // not a same-origin absolute path
    }
    $suffix = '';
    if ( preg_match( '/(#.*)$/', $u, $m ) ) {
        $suffix = $m[1];
        $u      = substr( $u, 0, -strlen( $m[1] ) );
    }
    if ( preg_match( '/(\?.*)$/', $u, $m ) ) {
        $suffix = $m[1] . $suffix;
        $u      = substr( $u, 0, -strlen( $m[1] ) );
    }
    if ( '' === $u || substr( $u, -1 ) === '/' ) {
        return $u . $suffix;
    }
    if ( preg_match( '/\.[a-z0-9]{2,5}$/i', $u ) ) {
        return $u . $suffix; // file URL
    }
    return $u . '/' . $suffix;
};

// 1) Elementor link fields ("url":"/path").
$ids = $wpdb->get_col( "SELECT DISTINCT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_elementor_data'" );
$n1  = 0;
foreach ( $ids as $id ) {
    $raw = get_post_meta( $id, '_elementor_data', true );
    if ( ! $raw ) {
        continue;
    }
    $new = preg_replace_callback(
        '/"url":"([^"]*)"/',
        function ( $m ) use ( $normalize_link ) {
            return '"url":"' . $normalize_link( $m[1] ) . '"';
        },
        $raw
    );
    if ( $new !== $raw ) {
        update_post_meta( $id, '_elementor_data', wp_slash( $new ) );
        delete_post_meta( $id, '_elementor_element_cache' );
        delete_post_meta( $id, '_elementor_css' );
        $n1++;
        echo "elementor post {$id}\n";
    }
}

// 2) Nav menu item URLs (/path).
$rows = $wpdb->get_results( "SELECT meta_id, meta_value FROM {$wpdb->postmeta} WHERE meta_key = '_menu_item_url'", ARRAY_A );
$n2   = 0;
foreach ( $rows as $r ) {
    $new = $normalize_link( $r['meta_value'] );
    if ( $new !== $r['meta_value'] ) {
        $wpdb->update( $wpdb->postmeta, array( 'meta_value' => $new ), array( 'meta_id' => $r['meta_id'] ) );
        echo "menu {$r['meta_value']} -> {$new}\n";
        $n2++;
    }
}

echo "normalized: elementor={$n1} menu={$n2}\n";
