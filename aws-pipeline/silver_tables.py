# import dlt as dt  # old version of the lakeflow declartive pipeline
from pyspark.sql.functions import *
from pyspark import pipelines as dp

@dp.expect_or_drop(
    "agent_id_not_null",
    "agent_id IS NOT NULL"
)
@dp.expect_or_drop(
    "customer_id_not_null",
    "customer_id IS NOT NULL"
)
@dp.expect_or_drop(
    "delivery_location_id_not_null",
    "delivery_location_id IS NOT NULL"
)
@dp.expect_or_drop(
    "order_id_not_null",
    "order_id IS NOT NULL"
)
@dp.expect_or_drop(
    "order_status_not_null",
    "order_status IS NOT NULL"
)
@dp.expect_or_drop(
    "payment_method_not_null",
    "payment_method IS NOT NULL"
)
@dp.expect_or_drop(
    "restaurant_id_not_null",
    "restaurant_id IS NOT NULL"
)
@dp.expect_or_drop(
    "total_amount_not_null",
    "total_amount IS NOT NULL"
)
@dp.expect_or_drop(
    "timestamp_not_null",
    "timestamp IS NOT NULL"
)
@dp.expect_or_drop(
    "tip_not_null",
    "tip IS NOT NULL"
)
@dp.expect_or_drop(
    "item_id_not_null",
    "items_ordered.item_id IS NOT NULL"
)
@dp.expect_or_drop(
    "item_name_not_null",
    "items_ordered.item_name IS NOT NULL"
)
@dp.expect_or_drop(
    "item_price_not_null",
    "items_ordered.price IS NOT NULL"
)
@dp.expect_or_drop(
    "item_quantity_not_null",
    "items_ordered.quantity IS NOT NULL"
)

@dp.table()
def silver_orders():
  silver=spark.readStream.table('aws.project.bronze_orders')
  return silver

customer_rules={'customer_id_nn':'customer_id is not null','name_nn':'name is not null','email_nn':'email is not null','dob_nn':'dob is not null','signup_date_nn':'signup_date is not null','location_id_nn':'location_id is not null'}

delivery_agent={'agent_id_nn':'agent_id is not null','name_nn':'name is not null','phone_nn':'phone is not null','rating_nn':'rating is not null'}

restaurant={'restaurant_id_nn':'restaurant_id is not null','name_nn':'name is not null','cuisines_nn':'cuisines is not null','location_id_nn':'location_id is not null','rating_nn':'rating is not null','delivery_fee_nn':'delivery_fee is not null'}

locations={'location_id_nn':'location_id is not null','area_nn':'area is not null','city_nn':'city is not null','state_nn':'state is not null','latitude_nn':'latitude is not null','longitude_nn':'longitude is not null'}

menu_item={'item_id_nn':'item_id is not null','restaurant_id_nn':'restaurant_id is not null','item_name_nn':'item_name is not null','price_nn':'price is not null','category_nn':'category is not null'}

@dp.expect_all_or_drop(customer_rules)
@dp.table()
def silver_customers():
    silver=spark.readStream.table('aws.project.bronze_dim_customers').select(col('customer_id'),col('name'),col('email'),col('dob'),col('signup_date'),col('location_id'))
    return silver

@dp.expect_all_or_drop(delivery_agent)
@dp.table()
def silver_delivery_agents():
    silver=spark.readStream.table('aws.project.bronze_dim_delivery_agents').select(col('agent_id'),col('name'),col('phone'),col('rating'))
    return silver

@dp.expect_all_or_drop(locations)
@dp.table()
def silver_locations():
    silver=spark.readStream.table('aws.project.bronze_dim_locations').select(col('location_id'),col('area'),col('city'),col('state'),col('latitude'),col('longitude'))
    return silver
 
@dp.expect_all_or_drop(restaurant)
@dp.table()
def silver_restaurants():
    silver=spark.readStream.table('aws.project.bronze_dim_restaurants').select(col('restaurant_id'),col('name'),col('cuisines'),col('location_id'),col('rating'),col('delivery_fee'))
    return silver
 
@dp.expect_all_or_drop(menu_item)
@dp.table()
def silver_menu_items():
    silver=spark.readStream.table('aws.project.bronze_dim_menu_items').select(col('item_id'),col('restaurant_id'),col('item_name'),col('price'),col('category'))
    return silver
    

