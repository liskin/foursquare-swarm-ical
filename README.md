# foursquare-swarm-ical

[![PyPI Python Version badge](https://img.shields.io/pypi/pyversions/foursquare-swarm-ical)](https://pypi.org/project/foursquare-swarm-ical/)
[![PyPI Version badge](https://img.shields.io/pypi/v/foursquare-swarm-ical)](https://pypi.org/project/foursquare-swarm-ical/)
![License badge](https://img.shields.io/github/license/liskin/foursquare-swarm-ical)

## Overview

**Sync Foursquare Swarm check-ins to local sqlite DB (incrementally) and generate iCalendar.**

![Example screenshot of the output in Google Calendar](https://github.com/liskin/foursquare-swarm-ical/assets/300342/b2c88749-3196-4645-8e2d-8574e19dfaa5)

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install foursquare-swarm-ical
```

To keep a local git clone around:

```
git clone https://github.com/liskin/foursquare-swarm-ical
make -C foursquare-swarm-ical pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install foursquare-swarm-ical
```

[pipx]: https://github.com/pypa/pipx

## Setup and usage

* Obtain a Foursquare API Access Token. The easiest way to obtain one is to
  use their [API Exporer](https://foursquare.com/developers/explore/). Grant
  it permission for your account, open DevTools, let it execute an API call
  and then inspect the request and copy `oauth_token` from the Query String
  Parameters.

  * Chrome: <https://developer.chrome.com/docs/devtools/network/reference#payload-encodings>
  * Firefox: <https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_list>

* Run `foursquare-swarm-ical`:

  ```
  $ foursquare-swarm-ical --access-token TOKENTOKENTOKEN --max-size 1M -o swarm-checkins.ical
  ```

* Import `swarm-checkins.ical` into your calendar app of choice.

  (Note that Google Calendar refreshes iCal URLs once a day and cannot be
  tweaked in any way. Manual refresh isn't possible either.)

## Command line options

<!-- include tests/readme/help.md -->
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
<!-- end include -->

## Configuration file

Access token (and other options) can be set permanently in a config file,
which is located at `~/.config/foursquare_swarm_ical/config.yaml` by default
(on Linux; on other platforms see output of `--help`).

Sample config file can be generated using the `--config-sample` flag:

<!-- include tests/readme/config-sample.md -->
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
<!-- end include -->

## Donations (♥ = €)

If you like this tool and wish to support its development and maintenance,
please consider [a small donation](https://www.paypal.me/lisknisi/5EUR) or
[recurrent support through GitHub Sponsors](https://github.com/sponsors/liskin).

By donating, you'll also support the development of my other projects. You
might like these:

* [strava-offline](https://github.com/liskin/strava-offline) – Keep a local mirror of Strava activities for further analysis/processing
* [strava-ical](https://github.com/liskin/strava-ical) – Generate iCalendar with your Strava activities
