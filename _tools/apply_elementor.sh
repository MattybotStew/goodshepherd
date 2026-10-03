#!/bin/zsh
# Apply an Elementor canvas JSON to a post and make the front end serve it.
#
#   ~/Local\ Sites/goodshepherd/_tools/apply_elementor.sh 2092 /tmp/sgsm.json
#
# Elementor keeps a rendered-markup cache in the `_elementor_element_cache`
# post meta. Updating `_elementor_data` through wp-cli bypasses the normal save
# path, so that cache has to be dropped or the old markup keeps rendering.
# Regenerating the per-post CSS needs the same treatment.

set -euo pipefail

POST_ID="$1"
JSON_FILE="$2"

WP="$HOME/Local Sites/goodshepherd/_tools/wp.sh"

"$WP" post meta update "$POST_ID" _elementor_data "$(cat "$JSON_FILE")"
"$WP" post meta delete "$POST_ID" _elementor_element_cache 2>/dev/null || true
"$WP" post meta delete "$POST_ID" _elementor_css 2>/dev/null || true
rm -f "$HOME/Local Sites/goodshepherd/app/public/wp-content/uploads/elementor/css/post-${POST_ID}.css"

# Deleting the CSS is not enough. Without an explicit regenerate the page keeps
# linking post-<id>.css while the file is missing, so the page silently renders
# with no Elementor CSS at all.
#
# clear_cache() deletes EVERY elementor CSS file, and pages that are not
# regenerated keep a valid `_elementor_css` meta so Elementor never rebuilds
# their file — they silently lose all styling. So clear, then regenerate every
# Elementor document (with its meta dropped to force the rebuild).
CSS_FILE="$HOME/Local Sites/goodshepherd/app/public/wp-content/uploads/elementor/css/post-${POST_ID}.css"
"$WP" eval "
\$ids = get_posts( array( 'post_type' => 'any', 'posts_per_page' => -1, 'meta_key' => '_elementor_edit_mode', 'meta_value' => 'builder', 'fields' => 'ids' ) );
Elementor\\Plugin::instance()->files_manager->clear_cache();
foreach ( \$ids as \$eid ) { delete_post_meta( \$eid, '_elementor_css' ); }
( new Elementor\\Core\\Files\\CSS\\Post( ${POST_ID} ) )->update();
"
[ -f "$CSS_FILE" ] || { echo "ERROR: ${CSS_FILE} was not generated" >&2; exit 1; }

"$WP" cache flush

echo "Applied to post ${POST_ID}. Verify:"
echo "  curl -sk https://goodshepherd.local/\$(wp post get $POST_ID --field=post_name)/ | grep -c data-id"