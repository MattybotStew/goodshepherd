<?php
/**
 * GSM outbound mail (SendGrid SMTP).
 *
 * This install ships no sendmail binary (`sendmail_path` points at a file that
 * does not exist) and nothing listens on 127.0.0.1:25, so PHP's mail() fails
 * below WordPress: wp_mail() returns false, nothing is logged, and password
 * resets / SureForms notifications / new-user mail all disappear silently.
 *
 * Outbound 587 and 465 are open from the host, so route PHPMailer over SMTP
 * instead. Credentials live in wp-config.php — never in this file, never in the
 * database:
 *
 *   define( 'GSM_SMTP_PASS', 'SG.xxxxxxxx' );   // required; plugin is inert without it
 *   define( 'GSM_SMTP_HOST', 'smtp.sendgrid.net' );   // optional
 *   define( 'GSM_SMTP_PORT', 587 );                   // optional
 *   define( 'GSM_SMTP_SECURE', 'tls' );               // optional, 'tls' (587) or 'ssl' (465)
 *   define( 'GSM_SMTP_USER', 'apikey' );              // optional, SendGrid always 'apikey'
 *   define( 'GSM_MAIL_FROM', 'info@goodshepherdmanor.org' );  // optional
 *   define( 'GSM_SMTP_DEBUG', 0 );                    // optional, 2 = verbose (never ship 2)
 *
 * The From address must stay on a domain authenticated in SendGrid. The zone
 * carries SPF `-all` and DMARC `p=quarantine`, so mail from an unaligned sender
 * is quarantined rather than bounced — including the client's own form
 * notifications landing in their own spam folder.
 *
 * Verify the sending domain, not just the API key: SendGrid needs the domain
 * DKIM record published, or Start-to-Finish alignment fails at DMARC.
 */

defined( 'ABSPATH' ) || exit;

/**
 * Read a wp-config constant, falling back to a default when it is undefined.
 *
 * @param string $constant Constant name.
 * @param mixed  $fallback Value to use when the constant is missing or empty.
 * @return mixed
 */
function gsm_mail_config( $constant, $fallback ) {
	return defined( $constant ) && '' !== constant( $constant ) ? constant( $constant ) : $fallback;
}

/**
 * Point PHPMailer at the transactional provider.
 *
 * Inert unless GSM_SMTP_PASS is defined, so Local and any host with a working
 * native transport keep behaving exactly as they do today.
 *
 * @param PHPMailer\PHPMailer\PHPMailer $phpmailer Mailer instance.
 */
add_action(
	'phpmailer_init',
	function ( $phpmailer ) {
		if ( ! defined( 'GSM_SMTP_PASS' ) || '' === GSM_SMTP_PASS ) {
			return;
		}

		$phpmailer->isSMTP();
		$phpmailer->Host        = gsm_mail_config( 'GSM_SMTP_HOST', 'smtp.sendgrid.net' );
		$phpmailer->Port        = (int) gsm_mail_config( 'GSM_SMTP_PORT', 587 );
		$phpmailer->SMTPSecure  = gsm_mail_config( 'GSM_SMTP_SECURE', 'tls' );
		$phpmailer->SMTPAuth    = true;
		$phpmailer->Username    = gsm_mail_config( 'GSM_SMTP_USER', 'apikey' );
		$phpmailer->Password    = GSM_SMTP_PASS;
		$phpmailer->SMTPAutoTLS = true;
		$phpmailer->SMTPDebug   = (int) gsm_mail_config( 'GSM_SMTP_DEBUG', 0 );
	},
	10,
	1
);

/**
 * Keep the envelope sender aligned with the authenticated domain.
 *
 * WordPress otherwise falls back to wordpress@<host>, which fails DMARC
 * alignment. An explicit From header (SureForms sets one) still wins, so this
 * only fills the gap.
 */
add_filter(
	'wp_mail_from',
	function ( $from ) {
		if ( defined( 'GSM_SMTP_PASS' ) && is_string( $from ) && '' !== $from ) {
			return $from;
		}
		return gsm_mail_config( 'GSM_MAIL_FROM', 'info@goodshepherdmanor.org' );
	},
	20
);

add_filter(
	'wp_mail_from_name',
	function ( $name ) {
		if ( is_string( $name ) && '' !== $name ) {
			return $name;
		}
		return gsm_mail_config( 'GSM_MAIL_FROM_NAME', 'Good Shepherd Manor' );
	},
	20
);

/**
 * Log send failures so the next outage is not silent.
 *
 * wp_mail() returns false on transport errors and callers routinely discard the
 * return value, which is how the missing-sendmail problem stayed invisible.
 */
add_action(
	'wp_mail_failed',
	function ( $error ) {
		$data = $error->get_error_data();
		$to   = is_array( $data ) && isset( $data['to'] ) ? implode( ', ', (array) $data['to'] ) : 'unknown';
		error_log( '[gsm-mail] send failed: ' . $error->get_error_message() . ' | to=' . $to );
	}
);
