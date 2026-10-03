<?php
/**
 * Self-host DM Sans so no fonts.googleapis.com / fonts.gstatic.com requests
 * are made:
 *   - Astra "Self Hosted Google Fonts" + "Preload Local Fonts" (downloads to
 *     wp-content/astra-local-fonts/ on the next front-end request)
 *   - disable Elementor's Google Fonts output (we self-host the same family)
 *
 * Run: wp eval-file _tools/configure_fonts.php
 */

$admin = get_option( 'astra_admin_settings', array() );
$admin['self_hosted_gfonts'] = true;
$admin['preload_local_fonts'] = true;
update_option( 'astra_admin_settings', $admin );

update_option( 'elementor_google_font', '0' ); // Elementor: "1" = load Google Fonts, "0" = off

// Nudge the loader so wp-content/astra-local-fonts/ is generated now.
$uploads = wp_upload_dir();
if ( function_exists( 'astra_load_preload_local_fonts' ) ) {
    // Astra downloads on the first front-end request; nothing to force here.
}

echo "Fonts self-hosted (Astra) + Elementor Google Fonts disabled.\n";
