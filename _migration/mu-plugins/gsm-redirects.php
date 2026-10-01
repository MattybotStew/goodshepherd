<?php
/**
 * GSM redirects.
 *
 * Ways to Give was merged into the Support GSM Foundation page as an anchor
 * section, so the old standalone slug now 301s to that anchor.
 *
 * Local runs nginx, so .htaccess is not an option. This is a mu-plugin rather
 * than a marketplace plugin to keep the redirect table in version control and
 * avoid a new dependency for two lines of logic.
 */

add_action(
	'template_redirect',
	function () {
		$redirects = array(
			'/ways-to-give/' => '/support-gsm/#ways-to-give',
			'/donate/' => '/support-gsm',
		);

		$path = wp_parse_url( home_url( add_query_arg( array() ) ), PHP_URL_PATH );

		if ( isset( $redirects[ $path ] ) ) {
			wp_safe_redirect( home_url( $redirects[ $path ] ), 301 );
			exit;
		}
	}
);