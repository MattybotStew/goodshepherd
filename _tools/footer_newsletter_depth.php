<?php
/**
 * Footer + newsletter-band depth. Idempotent; safe to re-run.
 *
 *   ./_tools/wp.sh eval-file _tools/footer_newsletter_depth.php
 *   # stage, after a push:
 *   wp eval-file /sites/goodshephe3dev/footer_newsletter_depth.php --allow-root
 *
 * Both rules existed ONLY in stage's Additional CSS — they were never in this
 * repo and never on Local, so the next Local -> stage database push would have
 * silently deleted them (flat footer, newsletter band losing its glow). They
 * live here now so a push carries them, and this script strips the old inline
 * copies so a host that already has them ends up with exactly one copy.
 *
 * The footer gradient is depth, not a new palette: it is three tints of the same
 * navy (#1a3348 / #2c4a63 / #0d1c28) under #C8D4E0 body text, all >= 7:1 against
 * the lightest stop.
 * The band gradient + radial glow sit behind the glass pill; the pill's own
 * contrast is unaffected because it keeps its own #006BB3 fill and white text.
 */

$start = '/* GSM footer + newsletter depth */';
$end   = '/* end GSM footer + newsletter depth */';

$footer = '.site-primary-footer-wrap{background:linear-gradient(135deg,#1a3348 0%,#2c4a63 40%,#0d1c28 100%)!important;border-top:1px solid rgba(255,255,255,.16);}';
$band   = '.elementor-element-nlband{position:relative;overflow:hidden;background:linear-gradient(180deg,#061a2c 0%,#0a2740 55%,#061a2c 100%)!important;}';
$glow   = '.elementor-element-nlband::before{content:"";position:absolute;inset:0;background:radial-gradient(58% 120% at 100% 50%,rgba(0,137,223,.5) 0%,rgba(0,137,223,0) 70%);pointer-events:none;}';

$css = wp_get_custom_css();

// 1. Drop the block this script owns, wherever it sits.
$from = strpos( $css, $start );
$to   = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

// 2. Drop the stage-only inline copies of the same three declarations.
foreach ( array( $footer, $band, $glow ) as $decl ) {
	$css = str_replace( "\n" . $decl, '', $css );
	$css = str_replace( $decl, '', $css );
}

// 3. Drop the leftover probe comment from an old debugging pass, then collapse
//    the blank-line runs earlier passes left behind, so Local and stage end up
//    with byte-identical stylesheets and a future push is a no-op.
$css = str_replace( "/* probe */\n\n", '', $css );
$css = preg_replace( "/\n{3,}/", "\n\n", $css );

$block = "\n" . $start . "\n" .
	"/* Footer: three tints of the same navy, so the footer reads as depth rather than a flat slab. */\n" .
	$footer . "\n" .
	"/* Newsletter band: the band's own navy gradient, plus a blue bloom from the pill side. */\n" .
	$band . "\n" .
	$glow . "\n" .
	$end . "\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $block );

$now = wp_get_custom_css();
printf( "Additional CSS: %d bytes; block present: %s; duplicates of the footer rule: %d\n",
	strlen( $now ),
	strpos( $now, $start ) !== false ? 'yes' : 'NO',
	substr_count( $now, rtrim( $footer, "\n" ) ) );
WP_CLI::success( 'Footer + newsletter-band depth applied.' );
