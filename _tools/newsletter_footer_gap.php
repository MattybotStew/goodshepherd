<?php
/**
 * Remove the 10px gap under the newsletter band on tablet and phone. Idempotent.
 *
 *   ./_tools/wp.sh eval-file _tools/newsletter_footer_gap.php
 *   # stage:
 *   wp eval-file /sites/goodshephe3dev/newsletter_footer_gap.php --allow-root
 *
 * The newsletter band (Elementor template 2375) sits in Astra's above-footer
 * slot, inside `.site-footer-above-section-1`. The white strip is NOT that
 * section's own margin: Astra puts a 10px `margin-bottom` on every
 * `.site-footer-section` once the footer stacks (max-width: 921px), and the
 * builder's empty `.site-footer-above-section-2` keeps its margin at 0 height,
 * so the strip survives even when section-1 is zeroed.
 *
 *   measured on Local (/programs/): 360 390 768 921 -> 10px gap, 922 1024 1440 -> 0
 *
 * Desktop is already flush, so the rule is scoped to the same 921px breakpoint
 * rather than shipping a global reset, and scoped to the above-footer wrap so
 * the primary footer's own column spacing is untouched.
 *
 * The gap comes from Astra's stacked-footer rule, not from the band template,
 * so this is Additional CSS and not an Elementor edit.
 */

$start = '/* GSM newsletter band sits on the footer */';
$end   = '/* end GSM newsletter band sits on the footer */';

$css = wp_get_custom_css();

// 1. Drop the block this script owns, wherever it sits.
$from = strpos( $css, $start );
$to   = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

$css = preg_replace( "/\n{3,}/", "\n\n", $css );

$block = "\n" . $start . "\n" .
	"/* Astra stacks the footer at 921px and gives every .site-footer-section a 10px bottom margin; the empty above-footer section-2 keeps it at 0 height, which left a white strip under the band. */\n" .
	"@media (max-width: 921px){.site-above-footer-wrap .site-footer-section{margin-bottom:0!important}.site-above-footer-wrap .site-footer-section:empty{display:none!important}}\n" .
	$end . "\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $block );

$now = wp_get_custom_css();
printf( "Additional CSS: %d bytes; block present: %s; copies: %d\n",
	strlen( $now ),
	strpos( $now, $start ) !== false ? 'yes' : 'NO',
	substr_count( $now, $start ) );
WP_CLI::success( 'Newsletter/footer gap removed at <=921px.' );
