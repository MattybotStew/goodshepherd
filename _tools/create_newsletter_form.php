<?php
/**
 * Create a SureForms "Newsletter Signup" form (email field + Sign Up) that
 * emails the monitored admin address, so the footer band and Newsletters page
 * forms have a real destination instead of action="/newsletters/".
 *
 * Run: wp eval-file _tools/create_newsletter_form.php
 */

$existing = get_posts( array(
    'post_type'   => 'sureforms_form',
    'title'       => 'Newsletter Signup',
    'post_status' => 'any',
    'numberposts' => 1,
) );
if ( $existing ) {
    $id = $existing[0]->ID;
} else {
    $id = wp_insert_post( array(
        'post_type'   => 'sureforms_form',
        'post_status' => 'publish',
        'post_title'  => 'Newsletter Signup',
    ) );
}

$block_id = substr( md5( 'gsm-newsletter' ), 0, 8 );
$content  = sprintf(
    '<!-- wp:srfm/email {"block_id":"%s","required":true,"formId":%d,"slug":"email"} /-->',
    $block_id,
    $id
);
wp_update_post( array( 'ID' => $id, 'post_content' => $content ) );

update_post_meta( $id, '_srfm_submit_button_text', 'Sign Up' );
update_post_meta( $id, '_srfm_email_notification', array(
    array(
        'id'              => 1,
        'status'          => true,
        'is_raw_format'   => false,
        'name'            => 'Admin Notification Email',
        'email_to'        => '{admin_email}',
        'email_reply_to'  => '{form:email}',
        'from_name'       => '{site_title}',
        'from_email'      => '{admin_email}',
        'email_cc'        => '',
        'email_bcc'       => '',
        'subject'         => 'New Newsletter Signup',
        'email_body'      => '{all_data}',
    ),
) );
update_post_meta( $id, '_srfm_form_confirmation', array(
    array(
        'id'                => 1,
        'confirmation_type' => 'same page',
        'page_url'          => '',
        'custom_url'        => '',
        'message'           => '<p>Thanks for subscribing to Good Shepherd Manor updates.</p>',
        'submission_action' => 'hide form',
        'enable_query_params' => false,
        'query_params'      => array(),
    ),
) );
update_post_meta( $id, '_srfm_form_restriction', '{"status":false,"maxEntries":0,"date":"","hours":"12","minutes":"00","meridiem":"AM","message":"","schedulingStatus":false}' );
update_post_meta( $id, '_srfm_compliance', array(
    array( 'id' => 'gdpr', 'gdpr' => false, 'do_not_store_entries' => false, 'auto_delete_entries' => false, 'auto_delete_days' => '' ),
) );

echo "newsletter form id: {$id}\n";
