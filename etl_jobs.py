from etl import artists

# full load
# artists.load_data_to_mongo(1)

# incremental load
incr = artists.ArtistIncr(1)
# incr.update_playcounts()
incr.update_ratings()
