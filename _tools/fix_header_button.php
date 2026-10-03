<?php
/**
 * Header CTA button + logo, so the header never breaks between the mobile
 * switch (922px) and full desktop (1220px):
 *   - the button label must not wrap / shrink (it was breaking letter-by-letter)
 *   - the logo shrinks in the tight band so logo+nav+button fit on one row
 *
 * Run: wp eval-file _tools/fix_header_button.php
 */

$css = wp_get_custom_css();
$add = <<<CSS

/* Header CTA button: never shrink or wrap the label */
.ast-builder-layout-element[data-section="section-header-button"],
.ast-header-button-1{flex-shrink:0;}
.ast-builder-layout-element[data-section="section-header-button"] .ast-custom-button,
.ast-header-button-1 .ast-custom-button,
a.ast-custom-button{white-space:nowrap!important;overflow-wrap:normal!important;word-break:keep-all!important;}

/* Tighten band: shrink the logo so logo+nav+CTA fit before the full desktop size */
@media (min-width:922px) and (max-width:1219px){
  .custom-logo, .ast-site-identity img, .site-logo-img, .site-logo img{max-width:112px!important;height:auto!important;}
}
CSS;

if ( strpos( $css, 'never shrink or wrap the label' ) === false ) {
    wp_update_custom_css_post( $css . $add );
    echo "appended\n";
} else {
    echo "already present\n";
}
