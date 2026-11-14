<?php
/**
 * Design sweep fixes (2026-11-13). Idempotent; safe to re-run.
 *
 *   wp eval-file _tools/design_sweep_fixes.php [path/to/design_patches.json]
 *
 * 1. Elementor data: merges _tools/design_patches.json into every builder page,
 *    the Newsletter band template (2375) and the "Single Post — News" template.
 *    Also gives any fixed-px-width container an explicit mobile width (Elementor
 *    otherwise forces 100% below 768px — the program icon tiles became bars).
 *    The generators apply the same file (_tools/design_patches.py).
 * 2. Astra Customizer settings:
 *    - Above Header background was #ffffff. Hero pages hide it under the
 *      transparent header; Privacy and every news post showed a blank white
 *      banner (white text on white). Now navy #002A4E.
 *    - Page title (Privacy H1) was 30px, smaller than its 36px H2s: 48/40/34.
 *    - Footer Facebook icon was an 18x18 target: 8px padding -> 34x34.
 * 3. Privacy (page 3): Astra "Narrow" content layout (750px) — lines ran ~160
 *    characters at 1440.
 * 4. Additional CSS block "GSM design sweep" (see $add below), the post_content
 *    flex fix, and removal of stale comment-only lines left by older runs of
 *    build_post_template.php.
 */

$json_path = $args[0] ?? ( ( getenv( 'GSM_REPO' ) ?: getenv( 'HOME' ) . '/Developer/goodshepherd' ) . '/_tools/design_patches.json' );
$patches   = json_decode( (string) file_get_contents( $json_path ), true );
if ( ! is_array( $patches ) ) {
	WP_CLI::error( "Cannot read patch table at {$json_path}" );
}

/* ---------- 1. Elementor data ---------- */

$tpl = get_posts( array( 'post_type' => 'elementor_library', 'title' => 'Single Post — News', 'posts_per_page' => 1, 'fields' => 'ids', 'post_status' => 'any' ) );
$docs = get_posts( array( 'post_type' => 'page', 'posts_per_page' => -1, 'fields' => 'ids', 'post_status' => 'publish', 'meta_key' => '_elementor_edit_mode', 'meta_value' => 'builder' ) );
$docs[] = 2375;
if ( $tpl ) {
	$docs[] = (int) $tpl[0];
}

function gsm_rules_for( array $patches, string $key ): array {
	$rules = array();
	foreach ( array( 'all', $key ) as $scope ) {
		foreach ( $patches[ $scope ] ?? array() as $match => $settings ) {
			$settings = array_filter( $settings, fn( $k ) => 0 !== strpos( $k, '_why' ), ARRAY_FILTER_USE_KEY );
			$rules[]  = array( $match, $settings );
		}
	}
	return $rules;
}

function gsm_rule_matches( string $match, string $id ): bool {
	return 0 === strpos( $match, 're:' ) ? (bool) preg_match( '/' . substr( $match, 3 ) . '/', $id ) : $match === $id;
}

function gsm_patch_walk( array &$nodes, array $rules, int &$changed ) {
	foreach ( $nodes as &$n ) {
		if ( ! is_array( $n ) ) {
			continue;
		}
		$id = (string) ( $n['id'] ?? '' );
		if ( ! isset( $n['settings'] ) || ! is_array( $n['settings'] ) ) {
			$n['settings'] = array();
		}
		$before = $n['settings'];
		foreach ( $rules as $r ) {
			if ( gsm_rule_matches( $r[0], $id ) ) {
				$n['settings'] = array_merge( $n['settings'], $r[1] );
			}
		}
		$w = $n['settings']['width'] ?? null;
		if ( 'container' === ( $n['elType'] ?? '' ) && is_array( $w ) && 'px' === ( $w['unit'] ?? '' ) && ! isset( $n['settings']['width_mobile'] ) ) {
			$n['settings']['width_mobile'] = $w;
		}
		if ( $before !== $n['settings'] ) {
			$changed++;
		}
		if ( ! empty( $n['elements'] ) && is_array( $n['elements'] ) ) {
			gsm_patch_walk( $n['elements'], $rules, $changed );
		}
	}
}

foreach ( $docs as $doc_id ) {
	$data = json_decode( (string) get_post_meta( $doc_id, '_elementor_data', true ), true );
	if ( ! is_array( $data ) ) {
		continue;
	}
	$key     = ( $tpl && (int) $tpl[0] === (int) $doc_id ) ? 'post_template' : (string) $doc_id;
	$changed = 0;
	gsm_patch_walk( $data, gsm_rules_for( $patches, $key ), $changed );
	if ( ! $changed ) {
		continue;
	}
	update_post_meta( $doc_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
	delete_post_meta( $doc_id, '_elementor_element_cache' );
	delete_post_meta( $doc_id, '_elementor_css' );
	( new Elementor\Core\Files\CSS\Post( $doc_id ) )->update();
	WP_CLI::log( "{$doc_id} ({$key}): {$changed} elements patched" );
}

/* ---------- 2. Astra settings ---------- */

$s = get_option( 'astra-settings', array() );
$s['hba-header-bg-obj-responsive']['desktop']['background-color'] = '#002A4E';
$s['font-size-page-title'] = array( 'desktop' => 48, 'tablet' => 40, 'mobile' => 34, 'desktop-unit' => 'px', 'tablet-unit' => 'px', 'mobile-unit' => 'px' );
// The rule that actually renders the Privacy H1 is Customizer > Page > Title
// (`header.entry-header .entry-title`), default 32px.
$s['ast-dynamic-single-page-title-font-size'] = array( 'desktop' => 48, 'tablet' => 40, 'mobile' => 34, 'desktop-unit' => 'px', 'tablet-unit' => 'px', 'mobile-unit' => 'px' );
$s['footer-social-1-bg-space'] = 8;
update_option( 'astra-settings', $s );
WP_CLI::log( 'Astra: above-header navy, page title 48/40/34, footer social padding 8' );

/* ---------- 3. Privacy layout ---------- */

update_post_meta( 3, 'ast-site-content-layout', 'narrow-width-container' );

/* ---------- 4. Additional CSS ---------- */

$css = wp_get_custom_css();

// post_content sits in a COLUMN flex container, so `flex:0 1 904px` set its
// HEIGHT to 904px: every short post had a ~900px empty body.
$css = str_replace( 'flex:0 1 904px!important;', 'flex:0 0 auto!important;', $css );
// post_body_inner now carries the 904px column itself (design_patches.json), so the
// content widget must not re-cap and re-centre it (it sat 20px in from the Back button at 1024).
$css = str_replace( '.elementor-element-post_content{max-width:904px!important;', '.elementor-element-post_content{max-width:100%!important;', $css );

// An older newsletter-band rule pinned the eyebrow at 12px; every other eyebrow is 13px.
$css = preg_replace( '/(\.elementor-element-nl_eyebrow \.elementor-heading-title\{[^}]*font-size:)12px/', '${1}13px', $css );

// Stale comment-only lines from older build_post_template.php runs (33 copies on Local).
foreach ( array(
	"/* full-bleed post template inside Astra's container */",
	'/* hero depth so posts without a featured image still look designed */',
	'/* fallback photo sits behind the element background, so a featured image still wins */',
) as $stale ) {
	$css = str_replace( $stale . "\n", '', $css );
	$css = str_replace( $stale, '', $css );
}
$css = preg_replace( "/\n{3,}/", "\n\n", $css );

$start = '/* GSM design sweep */';
$end   = '/* end GSM design sweep */';
$from  = strpos( $css, $start );
$to    = strrpos( $css, $end );
if ( false !== $from && false !== $to && $to > $from ) {
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

$add = "\n/* GSM design sweep */\n" .
	"/* overlapping card strips: the wire caps them at the 1200 grid (.home-intro__card) */\n" .
	"#home-intro,#ab-cards,#sg-cards,#en-cards,#ev-cards,#cr-cards,.elementor-element-contact_bar{max-width:1200px;}\n" .
	"/* paragraph rhythm: consecutive text widgets were 42px apart (theme p margin + 16px gap)\n" .
	"   vs 26px between paragraphs inside one widget. Match the 26px. */\n" .
	".elementor-widget-text-editor:has(+ .elementor-widget-text-editor) p:last-child{margin-bottom:10px;}\n" .
	"/* line length: program articles ran ~113 characters per line at 1440 (904px column)\n" .
	"   and ~122 at 1024; Events and Careers ~100-113. Cap body text at 720px (~85ch);\n" .
	"   images keep the full column. !important beats Elementor's\n" .
	"   `.elementor.elementor .e-con > .elementor-widget{max-width:100%}`. */\n" .
	".elementor-element-pg_content .elementor-widget-text-editor,\n" .
	".elementor-widget-text-editor[data-id^=\"ev_\"],.elementor-widget-text-editor[data-id^=\"cr_\"]{max-width:720px!important;}\n" .
	"/* end GSM design sweep */\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );
WP_CLI::log( 'Additional CSS: design sweep block written, post_content flex fixed, stale lines removed' );

WP_CLI::success( 'Design sweep fixes applied.' );
