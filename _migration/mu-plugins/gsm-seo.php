<?php
/**
 * GSM SEO tweaks.
 *
 * SureForms registers its `sureforms_form` post type as public, so the form
 * URLs (/form/newsletter-signup/, etc.) leak into the Rank Math sitemap. Forms
 * are not content: keep them out of the sitemap and out of search indexes.
 * The URLs still resolve in wp-admin for editing.
 */

add_filter(
	'rank_math/sitemap/exclude_post_type',
	function ( $exclude, $type ) {
		return 'sureforms_form' === $type ? true : $exclude;
	},
	10,
	2
);

$gsm_noindex_forms = function ( $robots ) {
	if ( is_singular( 'sureforms_form' ) || is_post_type_archive( 'sureforms_form' ) ) {
		$robots[] = 'noindex';
		$robots[] = 'nofollow';
	}
	return $robots;
};
add_filter( 'rank_math/frontend/robots', $gsm_noindex_forms );

add_filter(
	'wp_robots',
	function ( $robots ) {
		if ( is_singular( 'sureforms_form' ) || is_post_type_archive( 'sureforms_form' ) ) {
			$robots['noindex']  = true;
			$robots['nofollow'] = true;
		}
		return $robots;
	}
);
