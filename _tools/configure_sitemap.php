<?php
/**
 * Keep non-content post types out of the Rank Math XML sitemap.
 *
 * SureForms forms, Elementor Floating Buttons, Astra Advanced Hooks and a stale
 * WooCommerce `product` type are public and were being emitted as sitemaps
 * (/form/*, etc.). They are not indexable content.
 *
 * Run: wp eval-file _tools/configure_sitemap.php
 */

$opt  = get_option( 'rank-math-options-sitemap', array() );
$off  = array(
    'pt_sureforms_form_sitemap',
    'pt_e-floating-buttons_sitemap',
    'pt_astra-advanced-hook_sitemap',
    'pt_product_sitemap',
    'pt_web-story_sitemap',
);
$changed = array();
foreach ( $off as $key ) {
    if ( ( $opt[ $key ] ?? '' ) !== 'off' ) {
        $opt[ $key ]  = 'off';
        $changed[]    = $key;
    }
}
update_option( 'rank-math-options-sitemap', $opt );

// Drop Rank Math's cached sitemap files so the change is immediate.
delete_option( 'rank_math_sitemap_cache_files' );

echo 'sitemap post types disabled: ' . implode( ', ', $changed ?: array( 'already off' ) ) . "\n";
