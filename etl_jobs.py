from etl import artists

# full load
full = artists.ArtistFull(1)
full.load_data()


# incremental load
# incr = artists.ArtistIncr(500)
# incr.update_playcounts()
# incr.update_ratings()
