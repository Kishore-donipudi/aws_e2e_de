from pyspark import pipelines as dp
from pyspark.sql.functions import *

@dp.materialized_view(name="gold_orders_mv")
def gold_orders():
    menu_items=spark.read.table('aws.project.silver_menu_items')
    orders=spark.read.table('aws.project.silver_orders')
    gold=orders \
        .join(spark.read.table('aws.project.silver_customers').select(col('customer_id'),col('name').alias('customer_name'),col('email'),col('dob'),col('signup_date'),col('location_id')),'customer_id',how='left') \
        .join(spark.read.table('aws.project.silver_delivery_agents').select(col('agent_id'),col('name').alias('agent_name'),col('phone'),col('rating').alias('agent_rating')),'agent_id',how='left') \
        .join(spark.read.table('aws.project.silver_restaurants').select(col('restaurant_id'),col('name').alias('restaurant_name'),col('cuisines'),col('location_id').alias('restaurant_location_id'),col('rating').alias('restaurant_rating'),col('delivery_fee')),'restaurant_id',how='left') \
        .join(spark.read.table('aws.project.silver_locations'),'location_id',how='left') \
        .withColumn('items_ordered', explode(col('items_ordered'))) \
        .join(menu_items.select(col('item_id'),col('restaurant_id').alias('menu_restaurant_id'),col('item_name'),col('price'),col('category')),col("items_ordered.item_id") == col("item_id"),how='left')

    return gold

@dp.materialized_view()
def total_orders_per_restaurant():
    return (spark.read.table('aws.project.gold_orders_mv').groupBy('restaurant_id') \
        .agg(countDistinct('restaurant_id').alias('total_orders')))

@dp.materialized_view()
def top_selling_items():
    return (spark.read.table('aws.project.gold_orders_mv').groupBy('item_id') \
        .agg(sum('items_ordered.quantity').alias('total_quantity'),first('item_name').alias('item_name')).select(col('item_name'),col('total_quantity')))


@dp.materialized_view()
def avg_fees_by_city():
    gold=spark.read.table('gold_orders_mv').groupBy('city').agg(avg('restaurant_rating').alias('avg_rating'),avg('tip').alias('avg_tips'))\
        .select(col('city'),col('avg_rating'),col('avg_tips'))
    return gold 


@dp.materialized_view()
def agent_performance():
    gold=spark.read.table('gold_orders_mv').groupBy('agent_name') \
        .agg(countDistinct(col('order_id')).alias('orders_handled'),avg(col('agent_rating')).alias('avg_rating')) \
        .orderBy(col('orders_handled').desc()).select(col('agent_name'),col('orders_handled'),col('avg_rating'))
    return gold

@dp.materialized_view()
def daily_revenue_trend():
    gold=spark.read.table('gold_orders_mv').groupBy(to_date('timestamp').alias('date')) \
        .agg(sum('total_amount').alias('revenue')).orderBy(col('date').desc()).select(col('date'),col('revenue'))
    return gold

