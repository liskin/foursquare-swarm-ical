    $ foursquare-swarm-ical --help
    Usage: foursquare-swarm-ical [OPTIONS]
    
      Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar
    
    Options:
      -v, --verbose             Be more verbose
      --sync / --no-sync        Sync again or just use local database?  [default:
                                sync]
      --access-token TEXT       Foursquare oauth2 access token  [env var:
                                FOURSQUARE_TOKEN]
      --database PATH           SQLite database file  [default: /home/user/.local/
                                share/foursquare_swarm_ical/checkins.sqlite]
      -e, --emoji / --no-emoji  Prefix summary with venue category as emoji
                                [default: no-emoji]
      -o, --output FILENAME     Output file
      --config FILE             Read configuration from FILE.  [default: /home/use
                                r/.config/foursquare_swarm_ical/config.yaml]
      --config-sample           Show sample configuration file
      --help                    Show this message and exit.
