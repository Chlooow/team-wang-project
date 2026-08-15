{% snapshot shopify_orders_scd2 %}

{{
  config(
    target_schema='main',
    unique_key='id',
    strategy='check',
    check_cols=['email', 'financial_status', 'total_price', 'updated_at']
  )
}}

select
  id,
  customer_id,
  email,
  financial_status,
  total_price,
  updated_at
from {{ ref('stg_shopify_orders') }}

{% endsnapshot %}
