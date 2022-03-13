import pandas as pd
import geopy.distance

users_df = pd.read_csv('users.csv')
shops_df = pd.read_csv('shops.csv')
prods_df = pd.read_csv('products.csv')
prods_df = prods_df.rename(columns={'shop_prouct_id': 'shop_product_id'})
orders_df = pd.read_csv('orders.csv')
cats_df = pd.read_csv('categories.csv')


def get_blind_prods(user_lat, user_long):

    # filters

    # filter nearby shops

    shops_lat = shops_df.latitude
    shops_long = shops_df.longitude

    dists = []
    for s_lat, s_long in zip(shops_lat, shops_long):
        dist = geopy.distance.distance((s_lat, s_long), (user_lat, user_long)).km
        dists.append(dist)


    shops = pd.DataFrame()
    shops['shop_id'] = shops_df['shop_id']
    shops['distance'] = dists

    selected_shops_df = shops_df.loc[shops['distance'] < shops_df['service_radius']]
    selected_shops_df = selected_shops_df.loc[selected_shops_df['has_available_products'] == 1]
    selected_shops_df = selected_shops_df.loc[selected_shops_df['is_open'] == 1]
    selected_shops_df = pd.merge(selected_shops_df, shops, on=['shop_id'])

    # get products in those shops

    product_shop_df = pd.merge(prods_df, selected_shops_df[['shop_id', 'rate', 'service_radius', 'distance']], on=['shop_id'])
    product_shop_df = product_shop_df.loc[product_shop_df['moderation_status'] == 'approved']

    product_shop_df = product_shop_df.loc[product_shop_df['remaining_stock'] > 0]

    # blind Score

    # most bought products come first

    orders_prods_df = pd.merge(product_shop_df[['shop_product_id']], orders_df, on=['shop_product_id'])

    top_bought_products = orders_prods_df.groupby(['shop_id', 'shop_product_id']).size().to_frame('n_buy_all').reset_index()

    top_bought_products = top_bought_products.sort_values(by='n_buy_all', ascending=False)

    prod_ids = [tuple(x) for x in top_bought_products[['shop_id', 'shop_product_id']].values]
    return prod_ids[:20]


def get_prods(user_id):

    # filters

    # filter nearby shops

    user_lat = users_df.loc[users_df['id'] == user_id]['latitude'].tolist()[0]
    user_long = users_df.loc[users_df['id'] == user_id]['longitude'].tolist()[0]

    shops_lat = shops_df.latitude
    shops_long = shops_df.longitude

    dists = []
    for s_lat, s_long in zip(shops_lat, shops_long):
        dist = geopy.distance.distance((s_lat, s_long), (user_lat, user_long)).km
        dists.append(dist)


    shops = pd.DataFrame()
    shops['shop_id'] = shops_df['shop_id']
    shops['distance'] = dists

    selected_shops_df = shops_df.loc[shops['distance'] < shops_df['service_radius']]
    selected_shops_df = selected_shops_df.loc[selected_shops_df['has_available_products'] == 1]
    selected_shops_df = selected_shops_df.loc[selected_shops_df['is_open'] == 1]
    selected_shops_df = pd.merge(selected_shops_df, shops, on=['shop_id'])

    # get products in those shops

    product_shop_df = pd.merge(prods_df, selected_shops_df[['shop_id', 'rate', 'service_radius', 'distance']], on=['shop_id'])
    product_shop_df = product_shop_df.loc[product_shop_df['moderation_status'] == 'approved']

    product_shop_df = product_shop_df.loc[product_shop_df['remaining_stock'] > 0]

    # blind Score

    # most bought products come first

    orders_prods_df = pd.merge(product_shop_df[['shop_product_id']], orders_df, on=['shop_product_id'])

    top_bought_products = orders_prods_df.groupby(['shop_id', 'shop_product_id']).size().to_frame('n_buy_all').reset_index()

    top_bought_products = top_bought_products.sort_values(by='n_buy_all', ascending=False)

    # user-specific score

    # top categories that user buys from

    user_orders_df = orders_df.loc[orders_df.user_id == user_id]
    user_orders_cat_df = pd.merge(user_orders_df, prods_df[['shop_product_id', 'category_id']], on=['shop_product_id'])

    user_orders_cat_df

    category_score = user_orders_cat_df.groupby(['category_id']).size().to_frame('cat_score').reset_index()

    user_orders_cat_df = pd.merge(user_orders_cat_df, category_score, on=['category_id'])

	# listing top bought products in those shops
	
    top_bought_products = pd.merge(top_bought_products, prods_df[['shop_id', 'shop_product_id', 'category_id']], on=['shop_id','shop_product_id'])

    top_bought_products_top_cat = pd.merge(top_bought_products, category_score, on=['category_id'])

    top_bought_products_top_cat = top_bought_products_top_cat.sort_values(by='n_buy_all', ascending=False)

    prod_ids = [tuple(x) for x in top_bought_products_top_cat[['shop_id', 'shop_product_id']].values]
    if len(prod_ids) < 20:
        extra_prod_ids = [tuple(x) for x in top_bought_products[['shop_id', 'shop_product_id']].values]
        prod_ids = prod_ids + extra_prod_ids[:20-len(prod_ids)]
    return prod_ids[:20]


prod_ids = get_prods(user_id=462154)
# prod_ids = get_blind_prods(35.67495, 51.3469)
print(prod_ids)
