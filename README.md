# foursquare-swarm-ical

## Overview

Sync Foursquare Swarm check-ins to local sqlite DB (incrementally) and generate iCalendar.

## Installation

```
pipx ensurepath
pipx install --spec git+https://github.com/liskin/foursquare-swarm-ical foursquare_swarm_ical
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

```
$ foursquare-swarm-ical --help
usage: foursquare-swarm-ical [-h] [-v] [--no-sync] [--access-token XXX]
                             [--database FILE] [--emoji]

Sync Foursquare Swarm check-ins to local sqlite DB and generate iCalendar

optional arguments:
  -h, --help          show this help message and exit
  -v, --verbose
  --no-sync           skip online sync, print ical from database only
  --access-token XXX  foursquare oauth2 access token (default:
                      getenv('FOURSQUARE_TOKEN'))
  --database FILE     sqlite database file (default: checkins.sqlite)
  --emoji             prefix summary with venue category as emoji
```

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
