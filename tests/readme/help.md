    $ foursquare-swarm-ical --help
    Usage: foursquare-swarm-ical [OPTIONS]
    
      Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar
    
    Options:
      -v, --verbose             Logging verbosity (0 = WARNING, 1 = INFO, 2 =
                                DEBUG)
      --sync / --no-sync        Sync again or just use local database?  [default:
                                sync]
      --full / --no-full        Perform full sync instead of incremental
                                [default: no-full]
      --access-token TEXT       Foursquare oauth2 access token  [env var:
                                FOURSQUARE_TOKEN]
      --database PATH           SQLite database file  [default: /home/user/.local/
                                share/foursquare_swarm_ical/checkins.sqlite]
      -e, --emoji / --no-emoji  Prefix summary with venue category as emoji
                                [default: emoji]
      -o, --output FILENAME     Output file
      -m, --max-size SIZE       Maximum size of the output file in bytes (accepts
                                K and M suffixes as well)
      --config FILE             Read configuration from FILE.  [default: /home/use
                                r/.config/foursquare_swarm_ical/config.yaml]
      --config-sample           Show sample configuration file
      --help                    Show this message and exit.
