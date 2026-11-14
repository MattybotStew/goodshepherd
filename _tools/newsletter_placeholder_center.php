<?php
/**
 * Centre the newsletter field placeholder ("EMAIL ADDRESS") inside the pill.
 * Idempotent; safe to re-run.
 *
 *   ./_tools/wp.sh eval-file _tools/newsletter_placeholder_center.php
 *   # stage, after a push:
 *   wp eval-file /sites/goodshephe3dev/newsletter_placeholder_center.php --allow-root
 *
 * Only the placeholder is centred; typed text keeps its left alignment. The
 * block lives in this script so a Local -> stage database push carries it.
 */

$start = '/* GSM newsletter placeholder centring */';
$end   = '/* end GSM newsletter placeholder centring */';

$rule = '.elementor-element-nlright .srfm-input-email::placeholder{text-align:center!important;line-height:54px!important;}';

$css = wp_get_custom_css();

// 1. Drop the block this script owns, wherever it sits.
$from = strpos( $css, $start );
$to   = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

// 2. Collapse blank-line runs so repeated runs are a no-op.
$css = preg_replace( "/\n{3,}/", "\n\n", $css );

$block = "\n" . $start . "\n" . $rule . "\n" . $end . "\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $block );

$now = wp_get_custom_css();
printf( "Additional CSS: %d bytes; block present: %s\n",
	strlen( $now ),
	strpos( $now, $start ) !== false ? 'yes' : 'NO' );
WP_CLI::success( 'Newsletter placeholder centred.' );
