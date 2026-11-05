<?php
/**
 * Fix the single-post template.
 *
 * Posts were inheriting the transparent header (white logo + white nav) while
 * sitting on a white page, so the whole header was invisible, and they used
 * Astra's default blog layout with a right sidebar of Search / Recent Posts /
 * Recent Comments / Archives / Categories widgets. Match the pages: solid
 * header, plain container, no sidebar, date-only meta.
 */
$s = get_option( 'astra-settings' );

$s['transparent-header-disable-posts'] = 1;            // solid header, like pages
$s['single-post-sidebar-layout']       = 'no-sidebar'; // kill the default widget column
$s['single-post-content-layout']       = 'plain-container';
$s['single-post-ast-content-layout']   = 'normal-width-container';
$s['single-post-content-style']        = 'unboxed';
$s['blog-single-meta']                 = [ 'date' ];   // author was rendering as "By /"
$s['ast-dynamic-single-post-metadata'] = [ 'date' ];

update_option( 'astra-settings', $s );
echo "astra-settings updated\n";

// The privacy page carried an internal review note meant for the build team.
$privacy = get_post( 3 );
if ( $privacy && false !== strpos( $privacy->post_content, 'prototype and should be reviewed' ) ) {
    $content = preg_replace(
        '#<p>\s*<em>\s*Note: This policy is a prototype.*?</em>\s*</p>#is',
        '',
        $privacy->post_content
    );
    $content = preg_replace(
        '#<p[^>]*>\s*Note: This policy is a prototype.*?</p>#is',
        '',
        $content
    );
    wp_update_post( [ 'ID' => 3, 'post_content' => $content ] );
    echo "privacy note removed\n";
} else {
    echo "privacy note: not found (already clean?)\n";
}
