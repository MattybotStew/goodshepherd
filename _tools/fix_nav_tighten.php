<?php
/**
 * Keep the primary nav on a single row between 922-1219px (the wire tightens
 * the inline nav in this band). Without it, Astra's menu (flex-wrap: wrap)
 * wraps to two rows because its six items total ~694px while the centre
 * column is narrower.
 *
 * Run: wp eval-file _tools/fix_nav_tighten.php
 */

$css = wp_get_custom_css();
$add = <<<CSS

/* Tighten the inline nav between 922-1219px so it never wraps to two rows */
@media (min-width:922px) and (max-width:1219px){
  .main-header-menu{flex-wrap:nowrap!important;}
  .main-header-menu > .menu-item > .menu-link{padding:0 8px!important;font-size:13px!important;white-space:nowrap;}
  .main-header-menu > .menu-item > .ast-menu-toggle{padding:0 3px!important;}
  .ast-builder-layout-element[data-section="section-header-button"] .ast-custom-button,
  .ast-header-button-1 a.ast-custom-button,
  a.ast-button{padding:14px 16px!important;font-size:14px!important;}
}
CSS;

if ( strpos( $css, 'never wraps to two rows' ) === false ) {
    wp_update_custom_css_post( $css . $add );
    echo "appended\n";
} else {
    echo "already present\n";
}
