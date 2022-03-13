import pandas as pd
import geopy.distance

users_df = pd.read_csv('users.csv')
shops_df = pd.read_csv('shops.csv')
prods_df = pd.read_csv('products.csv')
prods_df = prods_df.rename(columns={'shop_prouct_id': 'shop_product_id'})
orders_df = pd.read_csv('orders.csv')


def get_blind_shops(user_lat, user_long):

    # filtering

    shops_lat = shops_df.latitude
    shops_long = shops_df.longitude

    dists = []
    for s_lat, s_long in zip(shops_lat, shops_long):
        dist = geopy.distance.distance((s_lat, s_long), (user_lat, user_long)).km
        dists.append(dist)

    shops = pd.DataFrame()
    shops['distance'] = dists

    selected_shops_df = shops_df.loc[shops['distance'] < shops_df['service_radius']]

    selected_shops_df = selected_shops_df.loc[selected_shops_df['has_available_products'] == 1]

    selected_shops_df = selected_shops_df.loc[selected_shops_df['is_open'] == 1]

    # blind score

    top_rated_shops_df = selected_shops_df[['shop_id', 'rate']].sort_values(by='rate', ascending=False).reset_index()
    top_rated_shops_df = top_rated_shops_df.drop('index', 1)

    shop_ids = top_rated_shops_df.shop_id.tolist()

    return shop_ids


def get_shops(user_id):

    # filtering

    user_lat = users_df.loc[users_df['id'] == user_id]['latitude'].tolist()[0]
    user_long = users_df.loc[users_df['id'] == user_id]['longitude'].tolist()[0]

    shops_lat = shops_df.latitude
    shops_long = shops_df.longitude

    dists = []
    for s_lat, s_long in zip(shops_lat, shops_long):
        dist = geopy.distance.distance((s_lat, s_long), (user_lat, user_long)).km
        dists.append(dist)

    shops = pd.DataFrame()
    shops['distance'] = dists

    selected_shops_df = shops_df.loc[shops['distance'] < shops_df['service_radius']]

    selected_shops_df = selected_shops_df.loc[selected_shops_df['has_available_products'] == 1]

    selected_shops_df = selected_shops_df.loc[selected_shops_df['is_open'] == 1]

    # blind score

    top_rated_shops_df = selected_shops_df[['shop_id', 'rate']].sort_values(by='rate', ascending=False).reset_index()
    top_rated_shops_df = top_rated_shops_df.drop('index', 1)


    # user-specific score

    # top rated shops by the user

    user_orders_df = orders_df.loc[orders_df.user_id == user_id]

    user_orders_df = user_orders_df.drop_duplicates(subset='order_id', keep='last')

    top_bought_shops = user_orders_df.groupby(['shop_id']).size().to_frame('n_buy').reset_index()

    top_user_rated_shops = user_orders_df.groupby(['shop_id']).rate.mean().to_frame().reset_index()

    # combine scores

    shop_scores = pd.merge(top_rated_shops_df, top_user_rated_shops, on=['shop_id'], how='outer',
                        suffixes=('_all', '_user'))
    
    shop_scores = pd.merge(shop_scores, top_bought_shops, on=['shop_id'], how='outer')

    average_shop_rate = shop_scores.rate_all.mean()

    shop_scores.rate_user = shop_scores.rate_user.fillna(average_shop_rate)

    shop_scores.n_buy = shop_scores.n_buy.fillna(0)

    shop_scores['total_score'] = shop_scores.rate_user + shop_scores.n_buy

    shop_scores = shop_scores.sort_values(by='total_score', ascending=False).reset_index()

    # output

    shop_ids = shop_scores.shop_id.tolist()
    
    return shop_ids
        

shop_ids = get_shops(user_id=557409)
# shop_ids = get_blind_shops(35.67495, 51.3469)
print(shop_ids)
