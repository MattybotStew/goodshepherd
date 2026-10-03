<?php
use WebpConverter\Repository\TokenRepository;
use WebpConverter\Conversion\Format\FormatFactory;
use WebpConverter\Conversion\Method\MethodFactory;
use WebpConverter\Conversion\Directory\DirectoryFactory;
use WebpConverter\PluginData;
use WebpConverter\PluginInfo;
use WebpConverter\Action\ConvertPathsAction;
use WebpConverter\Loader\PassthruLoader;

update_option( 'webpc_settings', array(
    'supported_extensions' => array( 'jpg', 'jpeg', 'png' ),
    'output_formats'       => array( 'webp' ),
    'conversion_method'    => 'gd',
    'auto_conversion'      => 'yes',
    'loader_type'          => 'passthru',
    'images_quality'       => '82',
) );

$token = new TokenRepository();
$ff    = new FormatFactory( $token );
$mf    = new MethodFactory( $token, $ff );
$df    = new DirectoryFactory( $ff );
$pd    = new PluginData( $token, $mf, $ff, $df );
$pi    = new PluginInfo( WP_PLUGIN_DIR . '/webp-converter-for-media/webp-converter-for-media.php', '6.6.5' );

$df->init_hooks(); // registers webpc_dir_name / webpc_dir_path filters

$uploads = wp_upload_dir();
$paths   = array();
$it = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $uploads['basedir'] ) );
foreach ( $it as $f ) {
    if ( $f->isFile() && preg_match( '/\.(jpe?g|png)$/i', $f->getFilename() ) ) { $paths[] = $f->getPathname(); }
}
echo "converting " . count( $paths ) . " files...\n";
( new ConvertPathsAction( $pd, $mf ) )->convert_files_by_paths( $paths, true );

( new PassthruLoader( $pi, $pd, $ff ) )->activate_loader();
$pass = ABSPATH . 'webpc-passthru.php';
echo ( file_exists( $pass ) ? "passthru: " . $pass : "passthru MISSING" ) . "\n";
