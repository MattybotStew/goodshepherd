<?php
/**
 * Serve the hero / CTA band / News donate backgrounds as WebP. The page
 * containers carry a `gsm-bg-*` class (set in the page data); the plain JPG
 * URL here is rewritten by Converter for Media to its WebP passthru, so the
 * browser receives image/webp (with the JPG as the source fallback).
 *
 * Run: wp eval-file _tools/webp_backgrounds.php
 */
$B = 'https://goodshepherd.local/wp-content/uploads/2026/10/';
$css = wp_get_custom_css();
$add = "/* WebP backgrounds (plugin rewrites these URLs to the WebP passthru) */\n"
     . ".gsm-bg-hero{background-image:url(\"{$B}hero.jpg\")!important;}\n"
     . ".gsm-bg-cta{background-image:url(\"{$B}cta-greenhouse.jpg\")!important;}\n"
     . ".gsm-bg-donate{background-image:url(\"{$B}donate-picnic.jpg\")!important;}\n";
if ( strpos( $css, 'WebP backgrounds (plugin rewrites' ) === false ) {
    wp_update_custom_css_post( $css . "\n" . $add );
    echo "added\n";
} else {
    echo "present\n";
}
