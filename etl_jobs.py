from etl import artists

# full load
# full = artists.ArtistFull(1)
# full.load_data()


# incremental load
incr = artists.ArtistIncr(1)
# this operation should run more often
incr.update_playcounts()
# this run can run less often
incr.update_ratings()
