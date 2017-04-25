# tbapy

[![PyPI version](https://badge.fury.io/py/tbapy.svg)](https://badge.fury.io/py/tbapy)

Unofficial Python library to get data from The Blue Alliance. Uses v3 of the TBA API.

This library returns JSON-parsed data fetched from The Blue Alliance's API.

Compatible with Python 2 and 3.

## Breaking changes between v0.x and v1.x
Version v1.x uses TBA API v3 for data gathering. The API has several major changes which are reflected in this library. Below are a list of potentially breaking changes that were made to this library for compatibility with API v3. If you need to use the old API, simply install and use an older version.
* Since API v3 now needs an `X-TBA-Auth-Key` header instead of `X-TBA-App-Id`, thus you will need to pass an auth key when instantiating the library rather than an app ID as previously.
* Team History requests have been renamed to reflect the change in TBA's naming of those requests. `team_history_events`, `team_history_awards`, `team_history_robots`, and `team_history_districts` have been renamed to `team_events`, `team_awards`, `team_robots`, and `team_districts`.
* `event_stats` is now `event_insights`.
* `district_points` has been removed. Data on rankings at a single event can now be fetched via the `event` request through its `detail_type` parameter, as aforementioned. `district_rankings` will continue to be used to return holistic ranking data.
* `event_list` has been renamed to `events`.

## Setup
First, install the module:

    pip3 install tbapy

Then, to use these functions, you must import the `tbapy` module:

```py
import tbapy
```

Before using the library, you must instantiate its class, for example:

```py
tba = tbapy.TBA('key')
```

The Blue Alliance's API requires that all applications identify themselves with an auth key when retrieving data. To obtain an auth key, visit TBA's [Account page](https://www.thebluealliance.com/account).


## Retrieval Functions
Replace `tba` with the object name if you changed it above.
* `tba.status()` - Get the status of TBA datafeeds
* `tba.teams(page)` - Get a list of of valid teams, where `page * 500` is the starting team number.
* `tba.team(team)` - Get a team's data. `team` can be an integer team number of a string-form `'frc####'` identifier.
* `tba.team_events(team, year)` - Get a list of events a team has been to.
* `tba.team_awards(team, [event])` - Get a list of the team's awards. _OPTIONAL: Specify an event that you want awards from. Otherwise all a team's awards will be returned._
* `tba.team_matches(team, event)` - Get a list of a team's matches at an event.
* `tba.team_years(team)` - Get a list of years the team was active in FRC.
* `tba.team_media(team, [year])` - Get team media. _OPTIONAL: Specify a year to get media from. Otherwise the current year will be inferred._
* `tba.team_history_events(team)` - Get events that a team has been to.
* `tba.team_history_awards(team)` - Get all awards that a team has received.
* `tba.team_history_robots(team)` - Get all of a team's robots.
* `tba.team_history_districts(team)` - Get the districts that a team has been part of over the years.
* `tba.event_list([year])` - Get a list of all events. _OPTIONAL: Include a year to get events from that year. Otherwise the current year's events will be returned._
* `tba.event(event)` - Get data about an event.
* `tba.event_teams(event)` - Get a list of teams at an event.
* `tba.event_stats(event)` - Get statistics from an event.
* `tba.event_rankings(event)` - Get the rankings at an event.
* `tba.event_awards(event)` - Get the awards from an event.
* `tba.event_matches(event)` - Get a match list of an event.
* `tba.district_points(event)` - Get points from a district.
* `tba.match(match)` - Get data about a match.
* `tba.districts(year)` - Get a list of all districts that exist(ed) in a given year.
* `tba.district_events(district, year)` - Get list of events in a district.
* `tba.district_rankings(district, year)` - Get the rankings in a district.
* `tba.district_teams(district, year)` - Get a list of the teams in a district.

See `example.py` for a usage example.

Documentation for The Blue Alliance's API can be found [here](https://www.thebluealliance.com/apidocs).

## Authors
This software was created and is maintained by [Erik Boesen](https://github.com/ErikBoesen) with [Team 1418](https://github.com/frc1418).

## License
This software is protected under the [MIT License](LICENSE).
