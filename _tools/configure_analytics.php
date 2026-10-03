<?php
/**
 * GA4 via "GA Google Analytics". Ships a clearly-marked placeholder
 * Measurement ID; the client replaces G-XXXXXXXXXX with the real property ID.
 *
 * Run: wp eval-file _tools/configure_analytics.php G-REALID123
 */
$id = isset( $args[0] ) && $args[0] ? $args[0] : 'G-XXXXXXXXXX';
update_option( 'gap_options', array(
    'gap_id'          => $id,
    'gap_location'    => 'header',
    'gap_enable'      => 2,
    'gap_display_ads' => 0,
    'link_attr'       => 0,
    'gap_anonymize'   => 0,
    'gap_force_ssl'   => 0,
    'admin_area'      => 0,
    'disable_admin'   => 0,
    'gap_custom_loc'  => 0,
    'tracker_object'  => '',
    'gap_custom_code' => '',
    'gap_custom'      => '',
    'gap_universal'   => 1,
    'version_alert'   => 0,
    'default_options' => 0,
) );
echo "GA4 tracking id: {$id}\n";
