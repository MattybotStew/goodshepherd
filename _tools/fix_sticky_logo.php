<?php
/**
 * Size the colour logo in the pinned header.
 *
 * The sticky bar shrinks the logo to ~90x22, which the background-image
 * replacement then draws as a smudge. Give the link an explicit box so the
 * logo keeps the same proportions as the solid header.
 */
$post = wp_get_custom_css_post();
$css  = $post ? $post->post_content : '';

if ( false === strpos( $css, 'sticky logo box' ) ) {
    $css .= "\n\n/* Sticky header: sticky logo box */"
        . '#ast-fixed-header .transparent-custom-logo{width:132px;height:56px;display:flex;align-items:center;}'
        . '#ast-fixed-header .transparent-custom-logo .custom-logo{opacity:0!important;width:100%!important;height:100%!important;}'
        . '@media (max-width:921px){#ast-fixed-header .transparent-custom-logo{width:112px;height:46px;}}' . "\n";
    wp_update_custom_css_post( $css );
    echo "logo sizing added\n";
} else {
    echo "logo sizing already present\n";
}
