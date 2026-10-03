<?php
/**
 * Wire the newsletter signup forms to a real destination: embed the SureForms
 * "Newsletter Signup" form (created by create_newsletter_form.php) in the dark
 * footer band and style it like the wire's glass pill. The Newsletters page
 * widget is swapped to the same shortcode in the page data.
 *
 * Run: wp eval-file _tools/configure... then _tools/wire_forms.php
 */

$FORM_ID = 2202;

// Footer band: replace the placeholder <form action="/newsletters/"> with the shortcode.
$s = get_option( 'astra-settings' );
$s['footer-html-1'] = '<div class="gsm-signup"><div class="gsm-signup__inner">'
    . '<div class="gsm-signup__copy"><p class="gsm-signup__eyebrow">Stay Connected</p>'
    . '<h2>Newsletter</h2>'
    . '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>'
    . '</div>'
    . '<div class="gsm-signup__form">'
    . '[sureforms id="' . $FORM_ID . '" show_title="false"]'
    . '</div></div></div>';
update_option( 'astra-settings', $s );

// Styling: glass pill in the dark band + GSM-blue button everywhere.
$css = wp_get_custom_css();
$add = <<<CSS

/* SureForms: hide duplicate form title, use the GSM primary button */
.srfm-form-title{display:none!important;}
.srfm-submit-button{background:#0089DF!important;border-radius:8px!important;color:#fff!important;}
.srfm-submit-button:hover{background:#006BB3!important;}
/* Newsletter inside the dark "Stay Connected" band */
.gsm-signup .srfm-form-container{background:transparent!important;padding:0!important;max-width:none!important;}
.gsm-signup .srfm-block-label{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}
.gsm-signup .srfm-common-error-message{display:none!important;}
.gsm-signup .srfm-block-wrap,.gsm-signup .srfm-email-block-wrap{margin:0!important;}
.gsm-signup .srfm-form{display:flex;align-items:center;gap:8px;padding:8px;border:1px solid rgba(255,255,255,.18);border-radius:999px;background:rgba(255,255,255,.08);flex-wrap:nowrap!important;}
.gsm-signup .srfm-block-single{flex:1 1 0!important;min-width:0!important;width:auto!important;}
.gsm-signup .srfm-submit-container{flex:0 0 auto!important;margin:0!important;}
.gsm-signup .srfm-input-email{flex:1;width:100%;min-width:0;font-family:inherit;font-size:16px;padding:14px 22px;border:0!important;border-radius:999px;background:transparent!important;color:#fff!important;box-shadow:none!important;}
.gsm-signup .srfm-input-email::placeholder{color:rgba(255,255,255,.45);}
.gsm-signup .srfm-submit-button{flex-shrink:0;font-family:inherit;font-size:16px;font-weight:700;line-height:1;padding:18px 32px;border:0;border-radius:999px;background:#0089DF!important;color:#fff!important;cursor:pointer;}
.gsm-signup .srfm-submit-button:hover{background:#006BB3!important;}
.gsm-signup .srfm-success-box,.gsm-signup .srfm-success-box-description{color:#fff!important;background:transparent!important;}
CSS;

if ( strpos( $css, 'Newsletter inside the dark' ) === false ) {
    wp_update_custom_css_post( $css . $add );
}

echo "Forms wired.\n";
