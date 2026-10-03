<?php
/**
 * Styling for the program article sidebar + richtext column, matching the
 * wire's ArticleSidebar / `.rte` (starter.css). Widths/order are set in
 * _tools/build_program_article.py; this only supplies the list/link + rte CSS.
 *
 * Run: wp eval-file _tools/fix_article_sidebar.php
 */

$css = wp_get_custom_css();
$add = <<<CSS

/* Program article: sidebar + richtext column (wire ArticleDetailPage) */
.gsm-article-sidebar{position:sticky;top:120px;}
.gsm-nav-list{list-style:none;margin:0;padding:0;border-top:1px solid #C8D4E0;}
.gsm-nav-list > li{border-bottom:1px solid #C8D4E0;}
.gsm-nav{display:block;padding:10px 0;font-size:15px;font-weight:600;color:#002A4E;text-decoration:none;}
.gsm-nav:hover,.gsm-nav.is-active{color:#0089DF;}
.gsm-subnav{list-style:none;margin:0 0 8px;padding:0 0 4px 12px;}
.gsm-subnav a{display:block;padding:6px 0;font-size:14px;font-weight:500;color:#303336;text-decoration:none;}
.gsm-subnav a:hover{color:#0089DF;}
.gsm-rte .elementor-widget-text-editor p,.gsm-rte p{font-size:17px;line-height:1.7;color:#303336;margin:0 0 16px;}
.gsm-rte ul,.gsm-rte ol{margin:0 0 16px;padding-left:22px;}
.gsm-rte li{font-size:17px;line-height:1.6;color:#303336;margin-bottom:8px;}
.gsm-rte blockquote{margin:0 0 20px;padding:4px 0 4px 20px;border-left:3px solid #0089DF;}
.gsm-rte blockquote cite{display:block;margin-top:6px;font-size:14px;color:#6b7280;}
@media(max-width:921px){.gsm-article-sidebar{position:static;}}
CSS;

if ( strpos( $css, 'sidebar + richtext column' ) === false ) {
    wp_update_custom_css_post( $css . $add );
    echo "appended\n";
} else {
    echo "already present\n";
}
