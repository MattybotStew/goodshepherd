<?php
/**
 * Footer "Get Involved" column (client decisions 2026-11-14).
 *
 * Global!D25 names the column "GET INVOLVED"; Global!D26 lists "Volunteer",
 * which the site did not have (it carried "Memorial or Tribute" instead,
 * client direction 2026-11-04). Keep both: Volunteer -> /support-gsm#events,
 * Memorial or Tribute stays -> /support-gsm#ways-to-give.
 *
 * The live footer column is the `widget_block` entry 16, rendered through
 * sidebars_widgets['footer-widget-3'] = block-16. Block 17 is an unused
 * older paragraph-style copy of the same column; it is updated too so the
 * two cannot drift apart. Do NOT use fix_footer.php for this — it writes a
 * lorem tagline, the retired .gsm-signup band and Astra Pro footer keys.
 *
 * Idempotent. Run on Local and on stage after a push:
 *   wp eval-file _tools/footer_get_involved.php
 */

$content = '<!-- wp:heading --><h2 class="wp-block-heading">Get Involved</h2><!-- /wp:heading -->'
    . '<!-- wp:list --><ul>'
    . '<!-- wp:list-item --><li><a href="/support-gsm/">GSM Foundation</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/shepherd-endowment-society/">Shepherd Endowment Society</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/events/">Events</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/support-gsm/#events">Volunteer</a></li><!-- /wp:list-item -->'
    . '<!-- wp:list-item --><li><a href="/support-gsm/#ways-to-give">Memorial or Tribute</a></li><!-- /wp:list-item -->'
    . '</ul><!-- /wp:list -->';

$wb = get_option( 'widget_block' );
$changed = 0;

foreach ( array( 16, 17 ) as $id ) {
    $current = isset( $wb[ $id ]['content'] ) ? $wb[ $id ]['content'] : null;
    if ( $current === $content ) {
        echo "block $id: already current\n";
        continue;
    }
    if ( ! isset( $wb[ $id ] ) || ! is_array( $wb[ $id ] ) ) {
        $wb[ $id ] = array();
    }
    $wb[ $id ]['content'] = $content;
    $changed++;
    echo "block $id: updated\n";
}

if ( $changed ) {
    update_option( 'widget_block', $wb );
    wp_cache_flush();
    echo "saved widget_block\n";
}

// Confirm the column that actually renders.
$sidebars = get_option( 'sidebars_widgets' );
$live     = isset( $sidebars['footer-widget-3'] ) ? $sidebars['footer-widget-3'] : array();
echo 'renders: ' . implode( ',', (array) $live ) . "\n";
