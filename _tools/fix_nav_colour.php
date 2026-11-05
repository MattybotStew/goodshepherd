<?php
/**
 * Generalise the "no hero behind the header" nav colour fix.
 *
 * Astra's primary menu colour is white (var(--ast-global-color-5)) because
 * every content page opens with a photo hero. Privacy and blog posts have no
 * hero, so the first rule was hard-scoped to .page-id-3 and the posts ended up
 * with a white-on-white nav. Key it off the transparent-header class instead.
 */
$post = wp_get_custom_css_post();
$css  = $post ? $post->post_content : '';

$old = <<<'CSS'
/* Privacy is the only page without a hero behind the header, so the
   white transparent-header nav was invisible on white. Use solid-header colours. */
.page-id-3 .main-header-menu > .menu-item > .menu-link{color:#002A4E!important;}
.page-id-3 .main-header-menu > .menu-item > .menu-link:hover,
.page-id-3 .main-header-menu > .current-menu-item > .menu-link,
.page-id-3 .main-header-menu > .current_page_item > .menu-link{color:#006BB3!important;}
CSS;

$new = <<<'CSS'
/* Pages without a hero behind the header (Privacy, blog posts) need the solid
   header's colours: the global menu colour is white for the transparent hero. */
body:not(.ast-theme-transparent-header) .main-header-menu > .menu-item > .menu-link{color:#002A4E!important;}
body:not(.ast-theme-transparent-header) .main-header-menu > .menu-item > .menu-link:hover,
body:not(.ast-theme-transparent-header) .main-header-menu > .current-menu-item > .menu-link,
body:not(.ast-theme-transparent-header) .main-header-menu > .current_page_item > .menu-link{color:#006BB3!important;}
CSS;

if ( false !== strpos( $css, '.page-id-3 .main-header-menu' ) ) {
    $css = str_replace( $old, $new, $css );
    wp_update_custom_css_post( $css );
    echo "nav colour rule generalised\n";
} elseif ( false !== strpos( $css, 'body:not(.ast-theme-transparent-header) .main-header-menu' ) ) {
    echo "already generalised\n";
} else {
    echo "pattern not found — check the CSS manually\n";
}
