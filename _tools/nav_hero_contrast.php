<?php
/**
 * Active nav parent was unreadable over the hero.
 *
 * On any page that sits under a dropdown (Events under Support GSM, every
 * program page under Programs & Services), Astra marks the parent
 * `current-menu-parent` / `current-menu-ancestor`. The AA rule that darkens
 * current items to #006BB3 has higher specificity than the transparent-header
 * "make it white" rule, which only listed `current-menu-item` and
 * `current_page_item` — so the parent rendered #006BB3 on the navy hero
 * (≈2.4:1).
 *
 * Add the two missing states to the hero (white) rule. Solid-header pages keep
 * the AA navy.
 *
 * Run:  wp eval-file _tools/nav_hero_contrast.php
 */

$css    = wp_get_custom_css();
$marker = 'GSM nav hero contrast';

if ( false !== strpos( $css, $marker ) ) {
	WP_CLI::success( 'Nav hero rule already present.' );
	return;
}

$add = "\n/* {$marker} */\n" .
	"@media (min-width:922px){\n" .
	"  .ast-theme-transparent-header:not(.page-id-3) .main-header-menu > .current-menu-parent > .menu-link,\n" .
	"  .ast-theme-transparent-header:not(.page-id-3) .main-header-menu > .current-menu-ancestor > .menu-link,\n" .
	"  .ast-theme-transparent-header:not(.page-id-3) .main-header-menu > .current_page_parent > .menu-link,\n" .
	"  .ast-theme-transparent-header:not(.page-id-3) .main-header-menu > .current_page_ancestor > .menu-link{color:#fff!important;}\n" .
	"}\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );

WP_CLI::success( 'Active nav parent now white over the hero.' );
