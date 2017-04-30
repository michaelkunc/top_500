from etl import artists

artists.load_data_to_mongo(1, 'top_500', 'artists')
