from etl import artists

# full load
# artists.load_data_to_mongo(1)

# incremental load
incr = artists.ArtistIncr(500)
incr.update_playcounts()
incr.update_ratings()
