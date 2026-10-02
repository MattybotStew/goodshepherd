<?php
/**
 * Elementor performance settings matching the wire build.
 *
 * Enables the stable "Optimized Markup" experiment (smaller DOM output).
 * Verified safe against the page custom CSS (scrollers, footer, submenu).
 * Note: "Optimized CSS Files" is ALPHA and intentionally left off.
 *
 * Run: wp eval-file _tools/optimize_performance.php
 */

$option = 'elementor_experiment-e_optimized_markup';
$current = get_option( $option );

if ( 'active' !== $current ) {
    update_option( $option, 'active' );
    echo "enabled: {$option}\n";
} else {
    echo "already enabled: {$option}\n";
}

\Elementor\Plugin::instance()->files_manager->clear_cache();
wp_cache_flush();
echo "elementor css cache cleared\n";
