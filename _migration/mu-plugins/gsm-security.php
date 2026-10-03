<?php
/**
 * GSM security hardening.
 *
 * Host-level WAF/DDoS is WP Engine's job; this covers the WordPress-level
 * basics: disable XML-RPC/pingbacks, block anonymous user enumeration, add
 * security response headers, strip version fingerprints, and rate-limit
 * wp-login.php. Kept in a mu-plugin so it ships with the site and survives
 * plugin updates without a new dependency.
 */

/* ---- XML-RPC / pingbacks off ---- */
add_filter( 'xmlrpc_enabled', '__return_false' );

add_filter(
	'wp_headers',
	function ( $headers ) {
		unset( $headers['X-Pingback'] );
		return $headers;
	}
);

add_filter(
	'xmlrpc_methods',
	function ( $methods ) {
		unset( $methods['pingback.ping'], $methods['pingback.extensions.getPingbacks'] );
		return $methods;
	}
);

/* ---- Security response headers ---- */
add_action(
	'send_headers',
	function () {
		header( 'X-Content-Type-Options: nosniff' );
		header( 'X-Frame-Options: SAMEORIGIN' );
		header( 'Referrer-Policy: strict-origin-when-cross-origin' );
		header( 'Permissions-Policy: geolocation=(), microphone=(), camera=()' );
		if ( is_ssl() ) {
			header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains' );
		}
	}
);

/* ---- Strip version fingerprints ---- */
remove_action( 'wp_head', 'wp_generator' );
add_filter( 'the_generator', '__return_empty_string' );
if ( ! headers_sent() ) {
	header_remove( 'X-Powered-By' );
}

/* ---- Block anonymous user enumeration via the REST API ---- */
add_filter(
	'rest_endpoints',
	function ( $endpoints ) {
		if ( is_user_logged_in() ) {
			return $endpoints;
		}
		unset( $endpoints['/wp/v2/users'], $endpoints['/wp/v2/users/(?P<id>[\d]+)'] );
		return $endpoints;
	}
);

/* ---- Rate-limit wp-login.php: 5 failures / 15 min per IP ---- */
const GSM_LOGIN_MAX    = 5;
const GSM_LOGIN_WINDOW = 900;

function gsm_client_ip() {
	foreach ( array( 'HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'REMOTE_ADDR' ) as $key ) {
		if ( ! empty( $_SERVER[ $key ] ) ) {
			$ip = trim( explode( ',', $_SERVER[ $key ] )[0] );
			if ( filter_var( $ip, FILTER_VALIDATE_IP ) ) {
				return $ip;
			}
		}
	}
	return '';
}

function gsm_login_key() {
	$ip = gsm_client_ip();
	return $ip ? 'gsm_login_fail_' . md5( $ip ) : '';
}

add_action(
	'wp_login_failed',
	function () {
		$key = gsm_login_key();
		if ( $key ) {
			set_transient( $key, (int) get_transient( $key ) + 1, GSM_LOGIN_WINDOW );
		}
	}
);

add_filter(
	'authenticate',
	function ( $user, $username, $password ) {
		if ( '' === $username || '' === $password ) {
			return $user;
		}
		$key = gsm_login_key();
		if ( $key && (int) get_transient( $key ) >= GSM_LOGIN_MAX ) {
			return new WP_Error(
				'gsm_too_many_attempts',
				__( '<strong>Error:</strong> Too many failed login attempts. Please try again in 15 minutes.' )
			);
		}
		return $user;
	},
	5,
	3
);

add_action(
	'wp_login',
	function () {
		$key = gsm_login_key();
		if ( $key ) {
			delete_transient( $key );
		}
	}
);
