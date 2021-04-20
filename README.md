# foursquare-swarm-ical

## Overview

Sync Foursquare Swarm check-ins to local sqlite DB (incrementally) and generate iCalendar.

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install git+https://github.com/liskin/foursquare-swarm-ical
```

To keep a local git clone around:

```
git clone https://github.com/liskin/foursquare-swarm-ical
make -C foursquare-swarm-ical pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install git+https://github.com/liskin/foursquare-swarm-ical
```

[pipx]: https://github.com/pipxproject/pipx

## Preparation

You'll need to obtain a Foursquare API Access Token. The easiest way to obtain
one is to use their [API Exporer](https://foursquare.com/developers/explore/).
Grant it permission for your account, open DevTools, let it execute an API
call and then inspect the request and copy `oauth_token` from the Query String
Parameters.

* Chrome: <https://developers.google.com/web/tools/chrome-devtools/network/reference#query-string>
* Firefox: <https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor/request_list>

## Usage

    $ foursquare-swarm-ical --help
    Usage: foursquare-swarm-ical [OPTIONS]
    
      Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar
    
    Options:
      -v, --verbose             Be more verbose
      --sync / --no-sync        Sync again or just use local database?  [default:
                                True]
    
      --access-token TEXT       Foursquare oauth2 access token
      --database PATH           SQLite database file  [default: /home/user/.local/
                                share/foursquare_swarm_ical/checkins.sqlite]
    
      -e, --emoji / --no-emoji  Prefix summary with venue category as emoji
                                [default: False]
    
      -o, --output FILENAME     Output file
      --config FILE             Read configuration from FILE.  [default: /home/use
                                r/.config/foursquare_swarm_ical/config.yaml]
    
      --help                    Show this message and exit.



Example:

```
$ foursquare-swarm-ical --access-token TOKENTOKENTOKEN
BEGIN:VCALENDAR
VERSION:2.0
PRODID:foursquare-swarm-ical
BEGIN:VEVENT
SUMMARY:@ Venue
DTSTART;VALUE=DATE-TIME:20120304T214456Z
…
```

## Configuration file

Access token (and other options) can be set permanently in a config file,
which is located at `~/.config/foursquare_swarm_ical/config.yaml` by default
(on Linux; on other platforms see output of `--help`).

Example config file:

```
access_token: TOKENTOKENTOKENTOKENTOKENTOKEN
emoji: True
verbose: 1
```
