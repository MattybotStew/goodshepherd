<?php
/**
 * Build the news post template (Elementor Pro Single Post) so a post looks like
 * the rest of the site: photo hero with the title, a 904px article column, and
 * the global CTA band before the newsletter.
 *
 * The hero background uses the post's featured image through a dynamic tag, so
 * editors only have to set an image on the post. Without one it falls back to
 * the navy hero colour.
 *
 * Idempotent: recreates the template if it already exists.
 *
 * Run:  wp eval-file _tools/build_post_template.php
 */

$TITLE = 'Single Post — News';

// ---------------------------------------------------------------- helpers
function gsm_px( $t, $r, $b, $l, $unit = 'px' ) {
	return array( 'unit' => $unit, 'top' => (string) $t, 'right' => (string) $r, 'bottom' => (string) $b, 'left' => (string) $l, 'isLinked' => false );
}

function gsm_el( $id, $type, $settings, $elements = array(), $inner = false ) {
	return array( 'id' => $id, 'elType' => $type, 'settings' => $settings, 'elements' => $elements, 'isInner' => $inner );
}

function gsm_widget( $id, $type, $settings ) {
	return array( 'id' => $id, 'elType' => 'widget', 'widgetType' => $type, 'settings' => $settings, 'elements' => array(), 'isInner' => false );
}

// ------------------------------------------------- reuse the existing CTA band
$band = null;
$donor = get_posts( array(
	'post_type'      => 'page',
	'posts_per_page' => 1,
	'meta_key'       => '_elementor_data',
	'meta_value'     => 'gsm_cta_band',
	'meta_compare'   => 'LIKE',
) );

if ( $donor ) {
	$data = json_decode( get_post_meta( $donor[0]->ID, '_elementor_data', true ), true );
	foreach ( (array) $data as $node ) {
		if ( isset( $node['id'] ) && 'gsm_cta_band' === $node['id'] ) {
			$band = $node;
			break;
		}
	}
}

// ---------------------------------------------------------------- the layout
$hero = gsm_el( 'post_hero', 'container', array(
	'content_width'            => 'full',
	'min_height'               => array( 'unit' => 'px', 'size' => 520, 'sizes' => array() ),
	'min_height_mobile'        => array( 'unit' => 'px', 'size' => 420, 'sizes' => array() ),
	'background_background'    => 'classic',
	'background_color'         => '#002A4E',
	'background_image'         => array( 'url' => '/wp-content/uploads/2026/10/hero.jpg', 'id' => '' ),
	'background_position'      => 'center center',
	'background_repeat'        => 'no-repeat',
	'background_size'          => 'cover',
	'background_overlay_background' => 'classic',
	'background_overlay_color'      => '#001424',
	'background_overlay_opacity'    => array( 'unit' => 'px', 'size' => 0.78, 'sizes' => array() ),
	'padding'                  => gsm_px( 120, 40, 120, 40 ),
	'padding_mobile'           => gsm_px( 96, 20, 96, 20 ),
	'flex_direction'           => 'column',
	'flex_align_items'         => 'flex-start',
	'flex_justify_content'     => 'center',
), array(
	gsm_el( 'post_hero_inner', 'container', array(
		'content_width'    => 'boxed',
		'flex_direction'   => 'column',
		'flex_align_items' => 'flex-start',
		'padding'          => gsm_px( 0, 0, 0, 0 ),
	), array(
		gsm_widget( 'post_eyebrow', 'heading', array(
			'title'     => 'News &amp; Updates',
			'header_size' => 'div',
			'title_color' => '#9FD0FF',
			'typography_typography'     => 'custom',
			'typography_font_size'      => array( 'unit' => 'px', 'size' => 12, 'sizes' => array() ),
			'typography_font_weight'    => '700',
			'typography_letter_spacing' => array( 'unit' => 'px', 'size' => 1.6, 'sizes' => array() ),
			'typography_text_transform' => 'uppercase',
			'_margin'   => gsm_px( 0, 0, 16, 0 ),
		) ),
		gsm_widget( 'post_title', 'heading', array(
			'title'       => 'Post title',
			'header_size' => 'h1',
			'align'       => 'left',
			'title_color' => '#FFFFFF',
			'__dynamic__' => array(
				'title' => '[elementor-tag id="ptitle1" name="post-title" settings="%7B%7D"]',
			),
			'typography_typography'  => 'custom',
			'typography_font_size'   => array( 'unit' => 'px', 'size' => 54, 'sizes' => array() ),
			'typography_font_size_mobile' => array( 'unit' => 'px', 'size' => 36, 'sizes' => array() ),
			'typography_font_weight' => '600',
			'typography_line_height' => array( 'unit' => 'EM', 'size' => 1.12, 'sizes' => array() ),
			'_margin' => gsm_px( 0, 0, 0, 0 ),
		) ),
		gsm_widget( 'post_date', 'text-editor', array(
			'editor' => 'Date',
			'text_color' => '#C8D4E0',
			'typography_typography'  => 'custom',
			'typography_font_size'   => array( 'unit' => 'px', 'size' => 15, 'sizes' => array() ),
			'_margin' => gsm_px( 16, 0, 0, 0 ),
			'__dynamic__' => array(
				'editor' => '[elementor-tag id="pdate1" name="post-date" settings="%7B%7D"]',
			),
		) ),
	) ),
) );

$content = gsm_el( 'post_body', 'container', array(
	'content_width'  => 'full',
	'background_background' => 'classic',
	'background_color'      => '#FFFFFF',
	'padding'        => gsm_px( 72, 40, 72, 40 ),
	'padding_mobile' => gsm_px( 40, 20, 40, 20 ),
	'flex_direction' => 'column',
	'flex_align_items' => 'center',
), array(
	gsm_el( 'post_body_inner', 'container', array(
		'content_width'  => 'boxed',
		'flex_direction' => 'column',
		'padding'        => gsm_px( 0, 0, 0, 0 ),
		'width'          => array( 'unit' => 'px', 'size' => 904, 'sizes' => array() ),
		'width_mobile'   => array( 'unit' => '%', 'size' => 100, 'sizes' => array() ),
	), array(
		gsm_widget( 'post_content', 'theme-post-content', array(
			'_css_classes' => 'gsm-post-content',
		) ),
		gsm_widget( 'post_back', 'button', array(
			'text'  => 'Back to News &amp; Updates',
			'link'  => array( 'url' => '/news/', 'is_external' => false ),
			'size'  => 'sm',
			'background_color' => 'rgba(0,0,0,0)',
			'button_text_color' => '#006BB3',
			'typography_typography'  => 'custom',
			'typography_font_size'   => array( 'unit' => 'px', 'size' => 16, 'sizes' => array() ),
			'typography_font_weight' => '700',
			'_margin' => gsm_px( 48, 0, 0, 0 ),
		) ),
	) ),
) );

$elements = array( $hero, $content );
if ( $band ) {
	$elements[] = $band;
}

$data = $elements;

// ---------------------------------------------------------------- save
$existing = get_page_by_title( $TITLE, OBJECT, 'elementor_library' ); // phpcs:ignore

if ( $existing ) {
	$post_id = $existing->ID;
	wp_update_post( array( 'ID' => $post_id, 'post_status' => 'publish' ) );
} else {
	$post_id = wp_insert_post( array(
		'post_title'  => $TITLE,
		'post_type'   => 'elementor_library',
		'post_status' => 'publish',
	) );
}

if ( is_wp_error( $post_id ) || ! $post_id ) {
	WP_CLI::error( 'Could not create the template post.' );
}

update_post_meta( $post_id, '_elementor_template_type', 'single-post' );
update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
update_post_meta( $post_id, '_elementor_version', ELEMENTOR_VERSION );
update_post_meta( $post_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
update_post_meta( $post_id, '_elementor_conditions', array( 'include/singular/post' ) );

// Elementor Pro resolves templates from this option, not the post meta alone.
$conditions = get_option( 'elementor_pro_theme_builder_conditions', array() );
if ( ! is_array( $conditions ) ) {
	$conditions = array();
}
$conditions['single'] = array( $post_id => array( 'include/singular/post' ) );
update_option( 'elementor_pro_theme_builder_conditions', $conditions );

delete_post_meta( $post_id, '_elementor_css' );
delete_post_meta( $post_id, '_elementor_element_cache' );

WP_CLI::log( sprintf( 'Template %d "%s": %d section(s), CTA band %s', $post_id, $TITLE, count( $elements ), $band ? 'included' : 'MISSING' ) );

// ---------------------------------------------------------------- styling
$css     = wp_get_custom_css();
$start   = '/* GSM post template */';
$end     = '/* end GSM post template */';

$css = wp_get_custom_css();

// Strip every previous copy of the block, then write a single clean one.
$start = '/* GSM post template */';
$end   = '/* end GSM post template */';

while ( false !== strpos( $css, $start ) ) {
	$from = strpos( $css, $start );
	$to   = strpos( $css, $end );
	if ( false === $to ) {
		break;
	}
	$css = substr( $css, 0, $from ) . substr( $css, $to + strlen( $end ) );
}

$add = "\n/* GSM post template */\n" .
	".single-post .site-content > .ast-container{max-width:100%!important;padding-left:0!important;padding-right:0!important;}\n" .
	".elementor-element-post_content{max-width:100%!important;width:100%!important;margin-left:auto!important;margin-right:auto!important;flex:0 0 auto!important;}\n" .
	".gsm-post-content{font-size:17px;line-height:1.65;color:#303336;}\n" .
	".gsm-post-content p{margin:0 0 24px!important;}\n" .
	".gsm-post-content h2{font-size:30px;line-height:1.25;color:#002A4E;font-weight:600;margin:48px 0 16px;}\n" .
	".gsm-post-content h3{font-size:22px;line-height:1.3;color:#002A4E;font-weight:700;margin:36px 0 12px;}\n" .
	".gsm-post-content a{color:#006BB3;text-decoration:underline;text-underline-offset:2px;}\n" .
	".gsm-post-content .wp-block-image{margin:0 0 28px;}\n" .
	".gsm-post-content img{border-radius:16px;height:auto;max-width:100%;}\n" .
	".gsm-post-content figcaption{font-size:14px;color:#6B7280;margin-top:10px;}\n" .
	".gsm-post-content ul,.gsm-post-content ol{padding-left:22px;margin:0 0 24px;}\n" .
	".gsm-post-content li{margin-bottom:8px;}\n" .
	"/* end GSM post template */\n";

wp_update_custom_css_post( rtrim( $css ) . "\n" . $add );
WP_CLI::log( 'Post template CSS written (single block, hero handled by Elementor).' );

WP_CLI::success( 'News post template ready.' );
