select
  id,
  customer_id,
  email,
  financial_status,
  total_price,
  updated_at,
  coalesce(cast(_dlt_load_id as varchar), cast(updated_at as varchar)) as loaded_at
from {{ source('raw_shopify', 'shopify_orders') }}
