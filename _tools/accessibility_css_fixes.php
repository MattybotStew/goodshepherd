<?php
/**
 * AA + tap-target fixes found in the 2026-11-13 stage audit.
 *
 * 1. Program sidebar label ("Programs") and the active/nested links were
 *    #0089DF on white = 3.72:1, below the 4.5:1 needed at 13-15px.
 * 2. Required-field asterisk was #DC2626 = 4.41:1; the token is #B42318 (7:1).
 * 3. Inline CTAs ("Learn more →", "Read More", "View openings →", "Facebook")
 *    render 14-20px tall. The existing 44px overlay only covers
 *    .elementor-button. Padding + negative margin grows the hit box to 44px
 *    without moving anything on screen.
 *
 * Appends once, guarded by a marker comment.
 *
 * Run:  wp eval-file _tools/accessibility_css_fixes.php
 */

$marker = 'GSM audit fixes 2026-11-13';

$css = wp_get_custom_css();

if ( false !== strpos( $css, $marker ) ) {
	WP_CLI::success( 'Audit fixes already present.' );
	return;
}

$add = <<<CSS

/* ===== {$marker} ===== */
/* Program sidebar: label + active/hover links were #0089DF (3.72:1) */
.elementor-element-pg_side_label .elementor-heading-title{color:#006BB3!important;}
.gsm-nav:hover,.gsm-nav.is-active{color:#006BB3!important;}
.gsm-subnav a:hover{color:#006BB3!important;}
/* Required-field asterisk: #DC2626 was 4.41:1 */
.srfm-required{color:#B42318!important;}
/* Inline CTAs: 44px hit area without moving the visual */
main a:not(.elementor-button):not(.ast-menu-toggle):not(.menu-link):not(.skip-link):not(.ast-button){
  display:inline-block;
  padding-top:14px;
  padding-bottom:14px;
  margin-top:-14px;
  margin-bottom:-14px;
}
CSS;

wp_update_custom_css_post( $css . $add );

WP_CLI::success( 'Audit CSS fixes applied.' );
