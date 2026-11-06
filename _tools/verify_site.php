<?php
/**
 * Assert the documented state of the Local site.
 *
 *   ~/Local\ Sites/goodshepherd/_tools/wp.sh eval-file _tools/verify_site.php
 *
 * Checks the facts AGENTS.md and HANDOFF.md depend on: page IDs and slugs,
 * Elementor builder mode, form IDs and recipients, the newsletter template and
 * its footer slot, the three mu-plugins, the program section anchors the
 * sidebars jump to, and that every image on a page exists on disk.
 *
 * Exit code is non-zero on any failure, so it can gate a push.
 */

$pass = 0;
$fail = [];
$GLOBALS['gsm_pass'] = 0;
$GLOBALS['gsm_fail'] = [];

function check( $label, $ok, $detail = '' ) {
	if ( $ok ) {
		$GLOBALS['gsm_pass']++;
		echo "PASS  $label\n";
		return;
	}
	$GLOBALS['gsm_fail'][] = $label . ( $detail ? "  [$detail]" : '' );
	echo "FAIL  $label" . ( $detail ? "  [$detail]" : '' ) . "\n";
}

/* ---- pages ---- */
$expected = [
	315  => 'home',
	316  => 'about',
	317  => 'programs',
	2088 => 'community-day-services',
	2127 => 'special-olympics',
	2090 => 'residential-living',
	2091 => 'health-well-being',
	2092 => 'support-gsm',
	2093 => 'shepherd-endowment-society',
	2094 => 'events',
	318  => 'news',
	2095 => 'newsletters',
	2096 => 'careers',
	319  => 'contact',
	3    => 'privacy',
];

foreach ( $expected as $id => $slug ) {
	$p = get_post( $id );
	check( "page $id = /$slug/", $p && $p->post_name === $slug && $p->post_status === 'publish',
		$p ? $p->post_name . '/' . $p->post_status : 'missing' );
}

/* Vocational was folded into Community Day Services (2026-11-06). The page
   stays as a draft so old links keep 301ing. */
$voc = get_post( 2089 );
check( 'page 2089 /vocational/ is a draft', $voc && 'vocational' === $voc->post_name && 'draft' === $voc->post_status,
	$voc ? $voc->post_name . '/' . $voc->post_status : 'missing' );

$builder = 0;
foreach ( array_diff( array_keys( $expected ), [ 3 ] ) as $id ) {
	if ( 'builder' === get_post_meta( $id, '_elementor_edit_mode', true ) ) {
		$builder++;
	}
}
check( '14 content pages use Elementor builder mode', 14 === $builder, "$builder/14" );
check( 'privacy is a plain WordPress page', 'builder' !== get_post_meta( 3, '_elementor_edit_mode', true ) );

/* ---- program menus (no Vocational anywhere) ---- */
foreach ( [ 'primary-menu', 'programs-sidebar' ] as $menu_slug ) {
	$menu = wp_get_nav_menu_object( $menu_slug );
	$items = $menu ? wp_get_nav_menu_items( $menu->term_id ) : [];
	$voc_items = array_filter( $items, fn( $i ) => false !== stripos( $i->url, '/programs/vocational' ) );
	check( "menu $menu_slug has no Vocational item", 0 === count( $voc_items ), count( $voc_items ) . ' found' );
}

/* ---- forms ---- */
$inbox = 'info@goodshepherdmanor.org';
foreach ( [ 2056 => 'Simple Contact Form', 2370 => 'Thank a Staff Member', 2202 => 'Newsletter Signup' ] as $id => $title ) {
	$p = get_post( $id );
	check( "form $id = $title", $p && 'publish' === $p->post_status, $p ? $p->post_title : 'missing' );
	$n  = maybe_unserialize( get_post_meta( $id, '_srfm_email_notification', true ) );
	$to = $n[0]['email_to'] ?? '';
	check( "form $id notifies $inbox", $to === $inbox, $to ?: 'unset' );
}

/* ---- newsletter band ---- */
$t = get_post( 2375 );
check( 'template 2375 = Newsletter band', $t && 'Newsletter band' === $t->post_title, $t ? $t->post_title : 'missing' );
$s = get_option( 'astra-settings' );
check( 'footer-html-1 holds only the template shortcode',
	( $s['footer-html-1'] ?? '' ) === '[elementor-template id="2375"]',
	$s['footer-html-1'] ?? 'empty' );

$types = [];
$walk  = function ( $els ) use ( &$walk, &$types ) {
	foreach ( $els as $e ) {
		if ( ! empty( $e['widgetType'] ) ) {
			$types[ $e['widgetType'] ] = ( $types[ $e['widgetType'] ] ?? 0 ) + 1;
		}
		$walk( $e['elements'] ?? [] );
	}
};
$walk( json_decode( get_post_meta( 2095, '_elementor_data', true ), true ) ?: [] );
check( 'newsletters embeds the SureForms widget', 1 === ( $types['sureforms_form'] ?? 0 ) );
check( 'newsletters has no shortcode widget', 0 === ( $types['shortcode'] ?? 0 ) );

/* ---- must-use plugins ---- */
$mu = glob( WPMU_PLUGIN_DIR . '/*.php' );
check( 'three mu-plugins installed', 3 === count( $mu ), count( $mu ) . ' found' );

/* The repo and the Local install live in unrelated trees, so the mirror is
   located from an explicit env var with a conventional fallback. */
$repo = getenv( 'GSM_REPO' ) ?: ( getenv( 'HOME' ) . '/Developer/goodshepherd' );
$mirror_dir = rtrim( $repo, '/' ) . '/_migration/mu-plugins';
foreach ( [ 'gsm-redirects.php', 'gsm-security.php', 'gsm-seo.php' ] as $file ) {
	$live   = WPMU_PLUGIN_DIR . '/' . $file;
	$mirror = $mirror_dir . '/' . $file;
	check( "$file matches the copy in _migration/mu-plugins/",
		file_exists( $live ) && file_exists( $mirror ) && md5_file( $live ) === md5_file( $mirror ),
		file_exists( $mirror ) ? 'differs' : "no mirror at $mirror_dir" );
}

/* ---- settings ---- */
check( 'blog_public is 0 (Local stays out of search)', '0' === (string) get_option( 'blog_public' ), (string) get_option( 'blog_public' ) );
check( "admin_email is $inbox", get_option( 'admin_email' ) === $inbox, get_option( 'admin_email' ) );
check( 'exactly one user', 1 === count( get_users() ), (string) count( get_users() ) );
check( 'active theme is astra', 'astra' === get_option( 'stylesheet' ), get_option( 'stylesheet' ) );
check( 'comments closed by default', 'closed' === get_option( 'default_comment_status' ), get_option( 'default_comment_status' ) );
$open = (int) $GLOBALS['wpdb']->get_var( "SELECT COUNT(*) FROM {$GLOBALS['wpdb']->posts} WHERE post_status='publish' AND comment_status='open'" );
check( 'no published post has comments open', 0 === $open, "$open open" );

/* ---- program section anchors ---- */
$anchors = [
	2088 => [ 'economics', 'personal-living-skills', 'digital-den', 'civic-engagement', 'physical-fitness', 'vocational-classroom', 'seniors', 'activities' ],
	2090 => [ 'personalized-support', 'leadership', 'our-team', 'comfort-safety', 'staying-connected', 'history', 'making-home-happen' ],
	2091 => [ 'supporting-health', 'mcallister-infirmary', 'nursing', 'voice-in-care', 'consistent-support', 'community-care', 'closing' ],
	2127 => [ 'following-interests', 'special-olympics', 'arts', 'outdoors', 'giving-back', 'gsm-events' ],
];
$total = 0;
$missing = 0;
foreach ( $anchors as $pid => $slugs ) {
	$raw = (string) get_post_meta( $pid, '_elementor_data', true );
	foreach ( $slugs as $slug ) {
		$total++;
		if ( ! str_contains( $raw, '"' . $slug . '"' ) ) {
			$missing++;
		}
	}
}
check( "all $total program section anchors present", 0 === $missing, "$missing missing" );

/* ---- /news hub links ---- */
$raw318 = (string) get_post_meta( 318, '_elementor_data', true );
preg_match_all( '#/news/([a-z0-9-]+)"#', $raw318, $m );
$bad = 0;
foreach ( array_unique( $m[1] ) as $slug ) {
	$post = get_page_by_path( $slug, OBJECT, 'post' );
	if ( ! $post || 'publish' !== $post->post_status ) {
		$bad++;
	}
}
check( 'every /news hub link resolves to a published post', 0 === $bad, "$bad broken" );

/* ---- images on disk ---- */
$missing_files = 0;
foreach ( array_keys( $expected ) as $pid ) {
	$raw = (string) get_post_meta( $pid, '_elementor_data', true );
	if ( preg_match_all( '#"id":"(\d+)"#', $raw, $mm ) ) {
		foreach ( array_unique( $mm[1] ) as $att ) {
			if ( (int) $att < 100 ) {
				continue;
			}
			$file = get_attached_file( (int) $att );
			if ( $file && ! file_exists( $file ) ) {
				$missing_files++;
			}
		}
	}
}
check( 'every image referenced by a page exists on disk', 0 === $missing_files, "$missing_files missing" );

echo "\n----------------------------------------\n";
$pass = $GLOBALS['gsm_pass'];
$fail = $GLOBALS['gsm_fail'];
if ( $fail ) {
	echo 'FAILED (' . count( $fail ) . ' of ' . ( $pass + count( $fail ) ) . "):\n - " . implode( "\n - ", $fail ) . "\n";
	exit( 1 );
}
echo "ALL $pass CHECKS PASSED\n";
