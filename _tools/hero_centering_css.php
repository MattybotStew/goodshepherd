<?php
/**
 * Hero centring that accounts for the transparent header, plus the nav wrap
 * band that breaks the header between 1230 and 1269px.
 *
 * The header floats over the hero, so the copy has to be centred in what is
 * visible BELOW the nav. Elementor only has three breakpoints, but the header
 * is four different heights:
 *
 *   >=1230        176px
 *   922-1229      151px
 *   768-921       190px
 *   <=767         177px
 *
 * So the top padding is set per band (header + 120 / 110 / 96) while the
 * bottom keeps the base value; any extra hero height then splits evenly and the
 * offset stays correct.
 *
 * The 1230-1269 band also wrapped the six nav items onto a second row (header
 * grew to 251px), so the menu spacing is tightened there.
 *
 * Run:  wp eval-file _tools/hero_centering_css.php
 */

$css   = wp_get_custom_css();
$start = '/* GSM hero vertical centring */';
$end   = '/* end GSM hero vertical centring */';

$from = strpos( $css, $start );
$to   = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

$add = "\n/* GSM hero vertical centring */\n" .
	"/* keep the flex centring even if a per-post CSS file is stale */\n" .
	".elementor-element-hero{justify-content:center!important;}\n" .
	".elementor-element-post_hero{justify-content:center!important;}\n" .
	"/* top padding = transparent header height + base rhythm.\n" .
	"   Header: >=1230 176px, 922-1229 151px, 768-921 190px, <=767 177px. */\n" .
	"/* post template hero: header + base, bottom base */\n" .
	"@media (min-width:1230px){.elementor-element-post_hero{padding-top:296px!important;}}\n" .
	"@media (min-width:922px) and (max-width:1229px){.elementor-element-post_hero{padding-top:271px!important;padding-bottom:120px!important;}}\n" .
	"@media (min-width:768px) and (max-width:921px){.elementor-element-post_hero{padding-top:300px!important;}}\n" .
	"@media (max-width:767px){.elementor-element-post_hero{padding-top:273px!important;}}\n" .
	"/* page heroes: base 120/110/96, then 14px moved from top to bottom. The lede is\n" .
	"   the last element and carries no margin (hero_inner_spacing.php), so equal\n" .
	"   boxes read ~28px low; this puts the copy back at the optical position Home\n" .
	"   uses (5-17px above centre, measured header ink -> H1 cap, baseline -> edge). */\n" .
	"@media (min-width:1230px){.elementor-element-hero{padding-top:282px!important;padding-bottom:134px!important;}}\n" .
	"@media (min-width:922px) and (max-width:1229px){.elementor-element-hero{padding-top:257px!important;padding-bottom:134px!important;}}\n" .
	"@media (min-width:768px) and (max-width:921px){.elementor-element-hero{padding-top:286px!important;padding-bottom:124px!important;}}\n" .
	"@media (max-width:767px){.elementor-element-hero{padding-top:259px!important;padding-bottom:110px!important;}}\n" .
	"/* bottom padding on pages with a card strip pulled up over the hero = the\n" .
	"   page-hero bottom above + the overlap, so the copy centres between the header\n" .
	"   and the cards. Overlaps follow Elementor breakpoints (>=1025 / tablet / <=767):\n" .
	"   home intro 160/96/64, cards_strip 120/80/56, contact bar 56. */\n" .
	"@media (min-width:1025px){\n" .
	"  .page-id-2092 .elementor-element-hero,.page-id-2093 .elementor-element-hero,.page-id-2094 .elementor-element-hero{padding-bottom:254px!important;}\n" .
	"  .page-id-319 .elementor-element-hero{padding-bottom:190px!important;}\n" .
	"}\n" .
	"@media (min-width:922px) and (max-width:1024px){\n" .
	"  .page-id-2092 .elementor-element-hero,.page-id-2093 .elementor-element-hero,.page-id-2094 .elementor-element-hero{padding-bottom:214px!important;}\n" .
	"  .page-id-319 .elementor-element-hero{padding-bottom:190px!important;}\n" .
	"}\n" .
	"@media (min-width:768px) and (max-width:921px){\n" .
	"  .page-id-2092 .elementor-element-hero,.page-id-2093 .elementor-element-hero,.page-id-2094 .elementor-element-hero{padding-bottom:204px!important;}\n" .
	"  .page-id-319 .elementor-element-hero{padding-bottom:180px!important;}\n" .
	"}\n" .
	"@media (max-width:767px){\n" .
	"  .page-id-2092 .elementor-element-hero,.page-id-2093 .elementor-element-hero,.page-id-2094 .elementor-element-hero{padding-bottom:166px!important;}\n" .
	"  .page-id-319 .elementor-element-hero{padding-bottom:166px!important;}\n" .
	"}\n" .
	"/* Home ends on a hard-edged button (no trailing text box), so it takes its\n" .
	"   own top/bottom: intro overlap + base, 20px moved from top to bottom. */\n" .
	"@media (min-width:1230px){.page-id-315 .elementor-element-hero{padding-top:276px!important;}}\n" .
	"@media (min-width:922px) and (max-width:1229px){.page-id-315 .elementor-element-hero{padding-top:251px!important;}}\n" .
	"@media (min-width:768px) and (max-width:921px){.page-id-315 .elementor-element-hero{padding-top:280px!important;}}\n" .
	"@media (max-width:767px){.page-id-315 .elementor-element-hero{padding-top:253px!important;}}\n" .
	"@media (min-width:1025px){.page-id-315 .elementor-element-hero{padding-bottom:300px!important;}}\n" .
	"@media (min-width:922px) and (max-width:1024px){.page-id-315 .elementor-element-hero{padding-bottom:236px!important;}}\n" .
	"@media (min-width:768px) and (max-width:921px){.page-id-315 .elementor-element-hero{padding-bottom:226px!important;}}\n" .
	"@media (max-width:767px){.page-id-315 .elementor-element-hero{padding-bottom:180px!important;}}\n" .
	"/* header nav wrapped onto a second row in this band (masthead 251px) */\n" .
	"@media (min-width:1230px) and (max-width:1269px){\n" .
	"  .main-header-menu > .menu-item > .menu-link{padding-left:5px!important;padding-right:5px!important;font-size:15px!important;}\n" .
	"  .ast-header-button-1{display:none!important;}\n" .
	"}\n" .
	"/* end GSM hero vertical centring */\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );

WP_CLI::success( 'Hero centring + nav band CSS written.' );
