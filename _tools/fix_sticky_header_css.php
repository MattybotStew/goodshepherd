<?php
/**
 * Give the sticky header the solid-white treatment once it pins.
 *
 * Enabling the sticky-header addon exposed the next gap: the fixed header
 * inherits the transparent styling, so it pinned as a transparent bar with a
 * white logo and white nav — invisible over page content. Match the solid
 * inner-page header: white bar, colour logo, navy links. Same background-image
 * logo technique as the open mobile menu (content:url() was WebKit-only).
 */
$post = wp_get_custom_css_post();
$css  = $post ? $post->post_content : '';

if ( false === strpos( $css, '#ast-fixed-header' ) ) {
    $chunks = array();

    $chunks[] = '/* Sticky header: solid white bar, colour logo, navy nav. */'
        . '#ast-fixed-header .main-header-bar{background:#FFFFFF!important;'
        . 'box-shadow:0 2px 10px rgba(0,42,78,.08);}'
        . '#ast-fixed-header .transparent-custom-logo{'
        . 'background:url("https://goodshepherd.local/wp-content/uploads/2026/10/gsm-logo-color.svg") center / contain no-repeat;}'
        . '#ast-fixed-header .transparent-custom-logo .custom-logo{opacity:0;}'
        . '#ast-fixed-header .main-header-menu > .menu-item > .menu-link{color:#002A4E!important;}'
        . '#ast-fixed-header .main-header-menu > .menu-item > .ast-menu-toggle{color:#002A4E!important;}'
        . '#ast-fixed-header .main-header-menu > .menu-item > .menu-link:hover,'
        . '#ast-fixed-header .main-header-menu > .current-menu-item > .menu-link,'
        . '#ast-fixed-header .main-header-menu > .current_page_item > .menu-link,'
        . '#ast-fixed-header .main-header-menu > .current-menu-parent > .menu-link{color:#006BB3!important;}'
        . '#ast-fixed-header .menu-toggle,'
        . '#ast-fixed-header .ast-mobile-svg,'
        . '#ast-fixed-header .ast-mobile-svg path{color:#002A4E!important;fill:#002A4E!important;}';

    $css .= "\n\n" . implode( "\n", $chunks ) . "\n";
    wp_update_custom_css_post( $css );
    echo "sticky header CSS added\n";
} else {
    echo "sticky header CSS already present\n";
}

// The jump bar must sit under the pinned header (100px at desktop/tablet).
$css = wp_get_custom_css_post()->post_content;
$css = str_replace(
    array( '#support-tabs.elementor-sticky--active{top:92px!important;}',
           '#support-tabs.elementor-sticky--active{top:70px!important;}' ),
    array( '#support-tabs.elementor-sticky--active{top:100px!important;}',
           '#support-tabs.elementor-sticky--active{top:80px!important;}' ),
    $css
);
wp_update_custom_css_post( $css );
echo "jump-bar offset aligned to the sticky header\n";
