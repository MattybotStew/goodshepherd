<?php
/**
 * Rebuild the Astra footer so it matches the React wire (Layout.jsx):
 *   - dark navy 4-column footer (brand / About Us / Ways To Give / Contact Info)
 *   - "Newsletter" signup band above the footer
 *   - updated bottom bar (copyright + Privacy / Accessibility)
 *
 * Run: wp eval-file _tools/fix_footer.php
 */

$logo = wp_get_attachment_image_url( 2169, 'full' ); // GSM Logo White
if ( ! $logo ) {
    $logo = 'https://goodshepherd.local/wp-content/uploads/2026/10/gsm-logo-white.svg';
}

// ---------------------------------------------------------------- widgets ---
$brand = '<!-- wp:image {"id":2169,"sizeSlug":"full","linkDestination":"custom"} -->'
    . '<figure class="wp-block-image size-full"><a href="/"><img src="' . esc_url( $logo )
    . '" alt="Good Shepherd Manor" class="wp-image-2169"/></a></figure>'
    . '<!-- /wp:image -->'
    . '<!-- wp:paragraph {"className":"gsm-footer-tagline"} -->'
    . '<p class="gsm-footer-tagline">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>'
    . '<!-- /wp:paragraph -->';

$about = '<!-- wp:heading {"level":4} --><h4 class="wp-block-heading">About Us</h4><!-- /wp:heading -->'
    . '<!-- wp:list --><ul>'
    . '<!-- wp:list-item --><li><a href="/about/#mission">Mission, Vision &amp; Values</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/about/#history">Our History</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/programs/">Our Programs</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/about/#affiliations">Affiliations</a></li><!-- /wp:list-item -->'
    . '</ul><!-- /wp:list -->';

$give = '<!-- wp:heading {"level":4} --><h4 class="wp-block-heading">Ways To Give</h4><!-- /wp:heading -->'
    . '<!-- wp:list --><ul>'
    . '<!-- wp:list-item --><li><a href="/support-gsm/">GSM Foundation</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/shepherd-endowment-society/">Shepherd Endowment Society</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/events/">Events</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/support-gsm/#memorial-tribute">Memorial or Tribute</a></li><!-- /wp:list-item -->'
    . '</ul><!-- /wp:list -->';

$contact = '<!-- wp:heading {"level":4} --><h4 class="wp-block-heading">Contact Info</h4><!-- /wp:heading -->'
    . '<!-- wp:paragraph --><p>Tel: <a href="tel:+18154723700">(815) 472-3700</a><br>'
    . 'P.O. Box 260<br>4129 N. State Route 1-17<br>Momence, IL 60954</p><!-- /wp:paragraph -->';

$widget_block = get_option( 'widget_block', array() );
$widget_block[12]['content'] = $brand;
$widget_block[14]['content'] = $about;
$widget_block[16]['content'] = $give;
$widget_block[18]['content'] = $contact;
$widget_block[20]['content'] = '';
$widget_block[21]['content'] = '';
update_option( 'widget_block', $widget_block );

$sidebars = get_option( 'sidebars_widgets', array() );
$sidebars['footer-widget-1'] = array( 'block-12' );
$sidebars['footer-widget-2'] = array( 'block-14' );
$sidebars['footer-widget-3'] = array( 'block-16' );
$sidebars['footer-widget-4'] = array( 'block-18' );
update_option( 'sidebars_widgets', $sidebars );

// ------------------------------------------------------- astra settings ---
$settings = get_option( 'astra-settings', array() );

// Newsletter band lives in the "above footer" HTML element.
$newsletter = <<<'HTML'
<div class="gsm-signup">
	<div class="gsm-signup__inner">
		<div class="gsm-signup__copy">
			<p class="gsm-signup__eyebrow">Stay Connected</p>
			<h2>Newsletter</h2>
			<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
		</div>
		<form class="gsm-signup__form" action="/newsletters/" method="post">
			<label for="gsm-newsletter-email">Email address</label>
			<div class="gsm-signup__row">
				<input id="gsm-newsletter-email" type="email" name="email" autocomplete="email" required>
				<button type="submit">Sign Up</button>
			</div>
		</form>
	</div>
</div>
HTML;

$settings['footer-html-1'] = $newsletter;

if ( ! isset( $settings['footer-desktop-items'] ) ) {
    $settings['footer-desktop-items'] = array();
}
$settings['footer-desktop-items']['above']['above_1'] = array( 'html-1' );
$settings['footer-desktop-items']['status']['above'] = true;
// Clean up a malformed key written by an earlier run (layouts belongs at the
// top level of footer-desktop-items, not inside `above`). Leaving it nested
// makes Astra's array_unique() stringify an array and emit a PHP warning.
unset( $settings['footer-desktop-items']['above']['layouts'] );
$settings['footer-desktop-items']['layouts']['above']['layout']['desktop'] = 'full';

// Above-footer section: no padding, the band provides its own.
$settings['section-above-footer-builder-padding'] = array(
    'desktop' => array( 'top' => '', 'right' => '', 'bottom' => '', 'left' => '' ),
    'tablet'  => array( 'top' => '', 'right' => '', 'bottom' => '', 'left' => '' ),
    'mobile'  => array( 'top' => '', 'right' => '', 'bottom' => '', 'left' => '' ),
    'desktop-unit' => 'px', 'tablet-unit' => 'px', 'mobile-unit' => 'px',
);

// Bottom bar: copyright with privacy + accessibility links.
$settings['footer-copyright-editor'] = '[copyright] [current_year] The Good Shepherd Manor. All rights reserved. <a href="/privacy/">Privacy Policy</a> &middot; <a href="/about/#accessibility">Accessibility Statement</a>';

// Dark footer surfaces + light type.
$dark = array(
    'background-color' => '#0D1C28', 'background-image' => '', 'background-repeat' => 'repeat',
    'background-position' => 'center center', 'background-size' => 'auto',
    'background-attachment' => 'scroll', 'background-type' => 'color',
);
$darker = $dark;
$darker['background-color'] = '#0A1725';
$settings['hb-footer-bg-obj-responsive']  = array( 'desktop' => $dark, 'tablet' => array(), 'mobile' => array() );
$settings['hbb-footer-bg-obj-responsive'] = array( 'desktop' => $darker, 'tablet' => array(), 'mobile' => array() );
$settings['hba-footer-bg-obj-responsive'] = array( 'desktop' => $darker, 'tablet' => array(), 'mobile' => array() );

for ( $i = 1; $i <= 4; $i++ ) {
    $settings[ "footer-widget-alignment-{$i}" ] = array( 'desktop' => 'left', 'tablet' => 'left', 'mobile' => 'left' );
}
$settings['footer-copyright-alignment'] = array( 'desktop' => 'left', 'tablet' => 'left', 'mobile' => 'left' );
$settings['footer-color'] = '#C8D4E0';
$settings['footer-link-color'] = '#C8D4E0';
$settings['footer-link-h-color'] = '#FFFFFF';
$settings['footer-copyright-color'] = '#C8D4E0';
$settings['hb-footer-main-sep-color'] = '#22303F';
$settings['hbb-footer-top-border-color'] = '#22303F';

for ( $i = 1; $i <= 4; $i++ ) {
    $settings[ "footer-widget-{$i}-color" ] = '#C8D4E0';
    $settings[ "footer-widget-{$i}-link-color" ] = '#C8D4E0';
    $settings[ "footer-widget-{$i}-link-h-color" ] = '#FFFFFF';
    $settings[ "footer-widget-{$i}-title-color" ] = '#FFFFFF';
}

$settings['footer-social-1-color'] = array( 'desktop' => '#C8D4E0' );
$settings['footer-social-1-h-color'] = array( 'desktop' => '#FFFFFF' );

update_option( 'astra-settings', $settings );

// ----------------------------------------------------------- custom css ---
$css = <<<'CSS'
/* GSM footer — matches the wire (Layout.jsx) */
.site-above-footer-wrap{padding:0!important;background:transparent!important;}
.site-above-footer-wrap .site-above-footer-inner-wrap,
.site-above-footer-wrap .ast-builder-grid-row{display:block!important;max-width:none!important;}
.site-above-footer-wrap .site-footer-above-section-1{width:100%!important;}
.site-above-footer-wrap .ast-footer-html-1,
.site-above-footer-wrap .ast-footer-html-1 .ast-header-html,
.site-above-footer-wrap .ast-footer-html-1 .ast-builder-html-element{width:100%;}
.gsm-signup{position:relative;overflow:hidden;background:linear-gradient(180deg,#061a2c 0%,#0a2740 55%,#061a2c 100%);border-top:1px solid rgba(255,255,255,.16);}
.gsm-signup::before{content:"";position:absolute;inset:0;background:radial-gradient(58% 120% at 100% 50%,rgba(0,137,223,.5) 0%,rgba(0,137,223,0) 70%);pointer-events:none;}
.gsm-signup__inner{position:relative;max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:48px;padding:76px 40px 80px;text-align:left;}
.gsm-signup__eyebrow{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#6cc4ff!important;margin:0 0 12px;}
.gsm-signup h2{font-size:48px;font-weight:600;line-height:1.1;letter-spacing:-1px;color:#fff!important;margin:0 0 12px;}
.gsm-signup__copy p{font-size:17px;line-height:1.6;color:rgba(255,255,255,.72)!important;margin:0;max-width:480px;}
.gsm-signup label{display:block;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.6);margin:0 0 12px;}
.gsm-signup__row{display:flex;gap:8px;padding:8px;border:1px solid rgba(255,255,255,.18);border-radius:999px;background:rgba(255,255,255,.08);}
.gsm-signup input[type=email]{flex:1;min-width:0;font-size:16px;padding:14px 22px;border:0;border-radius:999px;background:transparent;color:#fff;}
.gsm-signup input[type=email]::placeholder{color:rgba(255,255,255,.45);}
.gsm-signup button{flex-shrink:0;font-size:16px;font-weight:700;line-height:1;padding:18px 32px;border:0;border-radius:999px;background:#0089DF;color:#fff;cursor:pointer;}
.gsm-signup button:hover{background:#006BB3;}
@media(max-width:900px){.gsm-signup__inner{grid-template-columns:1fr;gap:28px;padding:56px 24px;}.gsm-signup h2{font-size:36px;}}

.site-primary-footer-wrap{background:linear-gradient(135deg,#1a3348 0%,#2c4a63 40%,#0d1c28 100%)!important;border-top:1px solid rgba(255,255,255,.16);}
.site-primary-footer-wrap h4,.site-primary-footer-wrap .wp-block-heading{color:#fff!important;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin:0 0 22px;}
.site-primary-footer-wrap p,.site-primary-footer-wrap li,.site-primary-footer-wrap a{color:#C8D4E0!important;font-size:15px;line-height:1.6;}
.site-primary-footer-wrap a:hover{color:#fff!important;}
.site-primary-footer-wrap ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px;}
.site-primary-footer-wrap ul li::before{content:none;}
.site-primary-footer-wrap .wp-block-image img{width:auto;height:72px;}
.site-primary-footer-wrap .gsm-footer-tagline{margin-top:18px!important;max-width:30ch;}

.site-below-footer-wrap{background:#0A1725!important;border-top:1px solid rgba(200,212,224,.35);}
.site-below-footer-wrap,.site-below-footer-wrap p,.site-below-footer-wrap a{color:#C8D4E0;}
.site-below-footer-wrap a:hover{color:#fff;}
CSS;

if ( function_exists( 'wp_update_custom_css_post' ) ) {
    wp_update_custom_css_post( $css );
}

wp_cache_flush();

echo "Footer rebuilt.\n";
