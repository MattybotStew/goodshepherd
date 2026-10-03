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
			'/sitemap.xml' => '/sitemap_index.xml',
		);

		$path = wp_parse_url( home_url( add_query_arg( array() ) ), PHP_URL_PATH );

		if ( isset( $redirects[ $path ] ) ) {
			wp_safe_redirect( home_url( $redirects[ $path ] ), 301 );
			exit;
		}

		// Posts now live under /news/%postname%/. 301 any old flat post URL
		// (/%postname%/) to its new home so earlier links keep working.
		if ( is_404() ) {
			$slug = trim( $path, '/' );
			if ( '' !== $slug && false === strpos( $slug, '/' ) ) {
				$post = get_page_by_path( $slug, OBJECT, 'post' );
				if ( $post && 'publish' === $post->post_status ) {
					wp_safe_redirect( home_url( '/news/' . $post->post_name . '/' ), 301 );
					exit;
				}
			}
		}
	}
);