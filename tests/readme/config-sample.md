    $ foursquare-swarm-ical --config-sample
    # Logging verbosity (0 = WARNING, 1 = INFO, 2 = DEBUG)
    verbose: 0
    
    # Sync again or just use local database?
    sync: true
    
    # Perform full sync instead of incremental
    full: false
    
    # Foursquare oauth2 access token
    access_token: TEXT
    
    # SQLite database file
    database: /home/user/.local/share/foursquare_swarm_ical/checkins.sqlite
    
    # Prefix summary with venue category as emoji
    emoji: true
    
    # Output file
    output: '-'
    
    # Maximum size of the output file in bytes (accepts K and M suffixes as well)
    max_size: SIZE
