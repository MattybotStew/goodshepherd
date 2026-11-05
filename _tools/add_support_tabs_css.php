<?php
/**
 * Additional CSS for the Support GSM jump bar (wire: SectionTabs).
 * Elementor buttons render as filled pills; the bar wants plain text tabs with
 * an underline on hover. Scoped to the jump-bar container so no other button
 * is touched. Same pattern as the program sidebar rules.
 */
$block = <<<CSS

/* Support GSM jump bar: text tabs, not kit buttons */
.elementor-element-sg_tabs .elementor-button {
  background: transparent !important;
  padding: 18px 0 !important;
  border: 0 !important;
  border-bottom: 2px solid transparent !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
.elementor-element-sg_tabs .elementor-button:hover {
  background: transparent !important;
  border-bottom-color: #006BB3 !important;
}
.elementor-element-sg_tabs .elementor-button-content-wrapper {
  justify-content: center;
}
CSS;

$post = wp_get_custom_css_post();
$css  = $post ? $post->post_content : '';

if ( false === strpos( $css, 'elementor-element-sg_tabs' ) ) {
    $css .= $block;
    wp_update_custom_css_post( $css );
    echo "jump-bar CSS added\n";
} else {
    echo "jump-bar CSS already present\n";
}
