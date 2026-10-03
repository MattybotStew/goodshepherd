<?php
/**
 * Configure Rank Math SEO: knowledge graph + LocalBusiness schema, Facebook,
 * trim unused modules, and set per-page titles/descriptions.
 *
 * Run: wp eval-file _tools/configure_seo.php
 */

// ---- Titles & Meta + Local SEO ------------------------------------------
$titles = get_option( 'rank-math-options-titles', array() );
$titles['knowledgegraph_type']  = 'company';
$titles['knowledgegraph_name']  = 'Good Shepherd Manor';
$titles['knowledgegraph_logo']  = wp_get_attachment_image_url( 2168, 'full' );
$titles['local_business_type']  = 'LocalBusiness';
$titles['local_phone']          = '(815) 472-3700';
$titles['local_address']        = array(
    'street_address'   => '4129 N. State Route 1-17',
    'address_locality' => 'Momence',
    'address_region'   => 'IL',
    'postal_code'      => '60954',
    'address_country'  => 'US',
);
$titles['twitter_card_type']    = 'summary_large_image';
$titles['open_graph_image_id']  = 2171; // hero.jpg fallback social image
$titles['open_graph_image']     = wp_get_attachment_image_url( 2171, 'full' );
update_option( 'rank-math-options-titles', $titles );

// Rank Math disables its front end until the site is "connected" or the
// registration step is skipped.
update_option( 'rank_math_registration_skip', 1 );

// ---- General: social ----------------------------------------------------
$general = get_option( 'rank-math-options-general', array() );
$general['social_url_facebook'] = 'https://www.facebook.com/goodshepherdmanor';
update_option( 'rank-math-options-general', $general );

// ---- Trim modules that don't apply --------------------------------------
update_option( 'rank_math_modules', array(
    'link-counter', 'analytics', 'seo-analysis', 'sitemap', 'rich-snippet', 'local-seo', 'role-manager',
) );

// ---- Per-page titles + descriptions -------------------------------------
$pages = array(
    315  => array( 'Good Shepherd Manor | Residential Care in Momence, IL',
        'Good Shepherd Manor is a residential care community in Momence, Illinois, supporting men with intellectual and developmental disabilities since 1971.' ),
    316  => array( 'About Us | Good Shepherd Manor',
        'Learn about Good Shepherd Manor - our history, mission, vision and values, affiliations, and accessibility commitment.' ),
    317  => array( 'Programs & Services | Good Shepherd Manor',
        'Explore Good Shepherd Manor programs: Community Day Services, Vocational, Special Olympics, Residential Living, and Health & Well Being.' ),
    2088 => array( 'Community Day Services | Good Shepherd Manor',
        'Community Day Services help the men of Good Shepherd Manor build skills, friendships, and independence, including the Digital Den.' ),
    2089 => array( 'Vocational Program | Good Shepherd Manor',
        'Good Shepherd Manor Vocational Program offers meaningful work, training, and coaching for the men we serve.' ),
    2127 => array( 'Special Olympics | Good Shepherd Manor',
        'Special Olympics at Good Shepherd Manor - sports, training, and competition for the men we serve.' ),
    2090 => array( 'Residential Living | Good Shepherd Manor',
        'Residential Living at Good Shepherd Manor offers a nurturing home and 24-hour support on our Momence campus.' ),
    2091 => array( 'Health & Well Being | Good Shepherd Manor',
        'Health & Well Being at Good Shepherd Manor: on-site nursing, clinic, and pharmacy, plus community supports and transportation.' ),
    2092 => array( 'Support GSM Foundation | Good Shepherd Manor',
        'Support the Good Shepherd Manor Foundation - ways to give, the Shepherd Endowment Society, events, and memorial or tribute gifts.' ),
    2093 => array( 'Shepherd Endowment Society | Good Shepherd Manor',
        'The Shepherd Endowment Society provides lasting financial support for Good Shepherd Manor through current and deferred gifts.' ),
    2094 => array( 'Events | Good Shepherd Manor',
        'Events at Good Shepherd Manor: the Fall Festival, Brunch Auction, Golf Invitational, and family events.' ),
    318  => array( 'News & Updates | Good Shepherd Manor',
        'News and updates from Good Shepherd Manor.' ),
    2095 => array( 'Newsletters & Family Resources | Good Shepherd Manor',
        'Read and subscribe to Good Shepherd Manor newsletters and family resources.' ),
    2096 => array( 'Careers | Good Shepherd Manor',
        'Careers at Good Shepherd Manor - join our team of Direct Service Providers and make a meaningful difference.' ),
    319  => array( 'Contact Us | Good Shepherd Manor',
        'Contact Good Shepherd Manor in Momence, Illinois - phone, address, staff directory, and contact form.' ),
);
foreach ( $pages as $id => $meta ) {
    update_post_meta( $id, 'rank_math_title', $meta[0] );
    update_post_meta( $id, 'rank_math_description', $meta[1] );
    update_post_meta( $id, 'rank_math_robots', array( 'index', 'follow' ) );
}

flush_rewrite_rules();

echo "Rank Math configured: " . count( $pages ) . " pages\n";
