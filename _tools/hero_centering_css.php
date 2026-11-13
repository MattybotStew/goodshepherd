<?php
/**
 * Belt-and-braces vertical centring for the sub-page heroes.
 *
 * The hero containers carry `justify-content: center` with symmetric 120/120
 * padding in their Elementor settings, which measures correctly. This rule
 * makes the centring survive a stale per-post CSS file in the browser, an
 * Elementor editor preview, or anyone later resetting the flex control: the
 * inner container is pushed to the middle with auto margins.
 *
 * Run:  wp eval-file _tools/hero_centering_css.php
 */

$css    = wp_get_custom_css();
$marker = 'GSM hero vertical centring';

if ( false !== strpos( $css, $marker ) ) {
	WP_CLI::success( 'Hero centring CSS already present.' );
	return;
}

$add = "\n/* {$marker} */\n" .
	".elementor-element-hero{justify-content:center!important;}\n" .
	".elementor-element-hero > .e-con-inner{margin-top:auto!important;margin-bottom:auto!important;}\n" .
	"/* keep the post template hero on the same rhythm */\n" .
	".elementor-element-post_hero{justify-content:center!important;}\n" .
	".elementor-element-post_hero > .elementor-element-post_hero_inner{margin-top:auto!important;margin-bottom:auto!important;}\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );

WP_CLI::success( 'Hero centring CSS added.' );
