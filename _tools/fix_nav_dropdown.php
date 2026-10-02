<?php
/**
 * Style the Astra nav dropdowns (.sub-menu) to match the wire's
 * .header__dropdown (Layout.css): white panel, 1px #e0e4e8 border, 8px radius,
 * navy links that turn GSM blue on hover. Also fixes the white-on-white link
 * colour inherited from the transparent hero header.
 *
 * Run: wp eval-file _tools/fix_nav_dropdown.php
 */

$css = wp_get_custom_css();
$add = <<<CSS

/* GSM nav dropdowns — styled to match the wire (Layout.css .header__dropdown) */
.main-header-menu .sub-menu{background:#fff!important;border:1px solid #e0e4e8!important;border-radius:8px!important;box-shadow:0 12px 28px rgba(0,42,78,.12)!important;padding:8px 0!important;min-width:260px;overflow:hidden;}
.main-header-menu .sub-menu .menu-link{padding:10px 16px!important;font-size:15px!important;font-weight:500!important;line-height:1.35!important;color:#002A4E!important;background:transparent!important;border:0!important;letter-spacing:0;}
.main-header-menu .sub-menu .menu-link:hover,
.main-header-menu .sub-menu .current-menu-item>.menu-link{color:#0089DF!important;background:#FAFCFE!important;}
/* keep dropdown text dark even over the transparent hero header */
.site-header .main-header-menu .sub-menu a.menu-link,
.ast-desktop .main-header-menu .sub-menu .menu-link{color:#002A4E!important;}
CSS;

if ( strpos( $css, 'GSM nav dropdowns' ) === false ) {
    wp_update_custom_css_post( $css . $add );
    echo "appended\n";
} else {
    echo "already present\n";
}
