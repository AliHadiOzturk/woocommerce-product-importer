

schemaName = "wordpress"

postTypes = {
    0: "product",
    1: "attachment"
}

postmetadataNames = {
    "Image": "_product_image_gallery",
    "Price": "_price",
    "SalePrice": "_sale_price",
    "ManageStock": "_manage_stock",
    "RegularPrice": "_regular_price",
    "SKU": "_sku",
    "Thumbnail": "_thumbnail_id",
    "StockStatus": "_stock_status",
    "Stock": "_stock",
    "TotalSales": "total_sales",
    "ManageStock": "_manage_stock",
    "_wp_attachment_image_alt": "_wp_attachment_image_alt",
    "_wp_attached_file": "_wp_attached_file"
}


wp_postmetadataInsert = "INSERT INTO "+schemaName + \
    ".wp_postmeta (post_id,meta_key,meta_value) VALUES ({post_id},'{meta_key}','{meta_value}')"
wp_postInsert = "INSERT INTO "+schemaName + \
    ".wp_posts (post_author,post_date,post_content,post_title,post_status,comment_status,ping_status,post_name,post_parent,post_type,post_mime_type,comment_count,post_excerpt,to_ping,pinged,post_content_filtered) VALUES ({post_author},'{post_date}','{post_content}','{post_title}','{post_status}','{comment_status}','{ping_status}','{post_name}','{post_parent}','{post_type}','{post_mime_type}',{comment_count},'{post_excerpt}','{to_ping}','{pinged}','{post_content_filtered}')"

# change it to your wp-content folder's path.
fileMovePath = "C:/inetpub/wwwroot/wp-content/uploads/2021/07/"
