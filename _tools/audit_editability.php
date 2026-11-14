<?php
/**
 * Read-only: report anything that would make a page non-editable in Elementor.
 *
 * The "Single Post — News" template is resolved by title, not by ID: it is built
 * independently on each host (2491 on stage, 2496 on Local), so a hardcoded ID
 * made this audit print "NO ELEMENTOR DATA" on Local and silently skip the doc.
 */
$ids = array( 315, 316, 317, 2088, 2090, 2091, 2127, 2092, 2093, 2094, 318, 2095, 2096, 319 );
$names = array(
	315 => 'Home', 316 => 'About', 317 => 'Programs', 2088 => 'CDS', 2090 => 'Residential',
	2091 => 'Health', 2127 => 'Engagement', 2092 => 'Support', 2093 => 'Endowment',
	2094 => 'Events', 318 => 'News', 2095 => 'Newsletters', 2096 => 'Careers', 319 => 'Contact',
);

$tpl = get_posts( array( 'post_type' => 'elementor_library', 'title' => 'Single Post — News', 'posts_per_page' => 1, 'fields' => 'ids', 'post_status' => 'any' ) );
if ( $tpl ) {
	$ids[] = (int) $tpl[0];
	$names[ (int) $tpl[0] ] = 'Post template';
}
$band = get_posts( array( 'post_type' => 'elementor_library', 'title' => 'Newsletter band', 'posts_per_page' => 1, 'fields' => 'ids', 'post_status' => 'any' ) );
if ( $band ) {
	$ids[] = (int) $band[0];
	$names[ (int) $band[0] ] = 'Newsletter band';
} else {
	$ids[] = 2375;
	$names[2375] = 'Newsletter band';
}

foreach ( $ids as $id ) {
	$raw = get_post_meta( $id, '_elementor_data', true );
	if ( ! $raw ) {
		echo $id . ' ' . ( $names[ $id ] ?? '' ) . ": NO ELEMENTOR DATA\n";
		continue;
	}
	$data = json_decode( $raw, true );
	if ( ! is_array( $data ) ) {
		echo $id . ' ' . ( $names[ $id ] ?? '' ) . ': JSON DECODE FAILED (' . json_last_error_msg() . ")\n";
		continue;
	}
	$w = array(); $html = 0; $cc = 0; $sty = 0; $sc = 0; $total = 0;

	$walk = function ( $n ) use ( &$walk, &$w, &$html, &$cc, &$sty, &$sc, &$total ) {
		if ( ! is_array( $n ) ) {
			return;
		}
		// a list of nodes
		if ( ! isset( $n['elType'] ) ) {
			foreach ( $n as $child ) {
				$walk( $child );
			}
			return;
		}
		if ( isset( $n['widgetType'] ) ) {
			$t = $n['widgetType'];
			$total++;
			$w[ $t ] = ( $w[ $t ] ?? 0 ) + 1;
			if ( 'html' === $t ) { $html++; }
			if ( 'shortcode' === $t ) { $sc++; }
			$s = $n['settings'] ?? array();
			if ( ! empty( $s['custom_css'] ) ) { $cc++; }
			$ed = (string) ( $s['editor'] ?? '' );
			if ( false !== strpos( $ed, '<style' ) || false !== strpos( $ed, '<script' ) ) { $sty++; }
		}
		foreach ( ( $n['elements'] ?? array() ) as $c ) {
			$walk( $c );
		}
	};

	$walk( $data );

	arsort( $w );
	$top = array();
	foreach ( array_slice( $w, 0, 5, true ) as $k => $v ) { $top[] = $k . ':' . $v; }

	printf( "%-14s sections=%d widgets=%d html=%d shortcode=%d customCss=%d inlineStyle=%d | %s\n", $names[ $id ] ?? $id, count( $data ), $total, $html, $sc, $cc, $sty, implode( ', ', $top ) );
}
