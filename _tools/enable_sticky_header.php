<?php
/**
 * Turn the Astra sticky header back on.
 *
 * `header-main-stick` is 1 in astra-settings, but the `sticky-header` addon
 * itself is disabled in `_astra_ext_enabled_extensions`, so the markup never
 * gets `ast-primary-sticky-enabled` and the header simply scrolls away —
 * which also means the transparent → white swap never happens.
 */
$ext = get_option( '_astra_ext_enabled_extensions' );
if ( ! is_array( $ext ) ) {
    $ext = array();
}
if ( empty( $ext['sticky-header'] ) ) {
    $ext['sticky-header'] = 'sticky-header';
    update_option( '_astra_ext_enabled_extensions', $ext );
    echo "sticky-header addon enabled\n";
} else {
    echo "sticky-header addon already enabled\n";
}

// Force Astra to regenerate its generated CSS/JS bundles.
delete_option( 'astra_theme_css_key-astra-addon' );
delete_option( 'astra_theme_js_key-astra-addon' );
delete_option( 'astra_partials_config_cache' );
wp_cache_flush();
echo "caches cleared\n";
