<?php
/**
 * Put posts under /news/%postname%/ to match the wire's /news/:slug routes.
 *
 * The React wire routes news articles at /news/:slug and site.js links
 * /news/<slug>, but WordPress served posts from the root (/%postname%/) and
 * 301-redirected those links. Aligning the permalink structure removes the hop.
 * gsm-redirects.php 301s the old flat post URLs to the new /news/ homes.
 *
 * Run: wp eval-file _tools/configure_permalinks.php
 */

global $wp_rewrite;

update_option( 'permalink_structure', '/news/%postname%/' );
$wp_rewrite->set_permalink_structure( '/news/%postname%/' );
$wp_rewrite->flush_rules( true );

echo "permalink_structure set to /news/%postname%/ and rewrite rules flushed\n";
