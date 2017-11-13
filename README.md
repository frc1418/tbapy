# tbapy

[![PyPI version](https://badge.fury.io/py/tbapy.svg)](https://badge.fury.io/py/tbapy)

Python library to get data from The Blue Alliance. _Uses v3 of the TBA API._

This library returns JSON data fetched from The Blue Alliance's API.

Compatible with Python 2 and 3.

## Breaking changes between v0.x and v1.x
Version v1.x uses TBA API v3 for data gathering. The API has several major changes which are reflected in this library. Below are a list of potentially breaking changes that were made to this library for compatibility with API v3. If you need to use the old API, simply install and use an older version.
* The library now functions based on objects rather than raw JSON data. Dictionary syntax (ie `team['team_number']`) will work, but object syntax (`team.team_number`) is recommended. If you want to use raw JSON data, append `.json()` to the end of the object variable. So, if you had a `Team` object named `my_team`, `my_team.json()` would give you the team data as a raw dictionary. Otherwise, you'll need to switch to using dot notation for the most part and treating the data appropriately.
* Since API v3 now needs an `X-TBA-Auth-Key` header instead of `X-TBA-App-Id`, thus you will need to pass an auth key when instantiating the library rather than an app ID as previously.
* Team History requests have been renamed to reflect the change in TBA's naming of those requests. `team_history_events()`, `team_history_awards()`, `team_history_robots()`, and `team_history_districts()` have been renamed to `team_events()`, `team_awards()`, `team_robots()`, and `team_districts()`.
* The `year` parameter in `team_media()` is no longer optional.
* `event_stats()` is now `event_insights()`.
* `district_points()` has been removed. Data on rankings at a single event can now be fetched via the `event_district_points()`. `district_rankings()` will continue to be used to return holistic ranking data.
* `event_list()` has been renamed to `events()`.

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
* `tba.teams(page, [year], [keys])` - Get a list of of valid teams, where `page * 500` is the starting team number. _OPTIONAL: specify a year to get teams from and set `keys` to `True` to retrieve only the keys of the team rather than its full data._
* `tba.team(team, [simple])` - Get a team's data. `team` can be an integer team number of a string-form `'frc####'` identifier. _OPTIONAL: Specify `simple` as `True` to get simplified data (recommended unless you need full information)._
* `tba.team_events(team, [year], [keys])` - Get a list of events a team has been to. _OPTIONAL: Specify `keys` as `True` to get only the keys of the events and not their full data._
* `tba.team_awards(team, [event/year])` - Get a list of the team's awards. _OPTIONAL: Specify an event or year that you want awards from. Otherwise all a team's awards will be returned._
* `tba.team_matches(team, [event/year], [keys])` - Get a list of a team's matches at an event. _OPTIONAL: Specify `keys` as `True` to only fetch match keys rather than their full data._
* `tba.team_years(team)` - Get a list of years the team was active in FRC.
* `tba.team_media(team, year)` - Get team media. Specify a year to get media from.
* `tba.team_robots(team)` - Get data about a team's robots.
* `tba.team_districts(team)` - Get the districts that a team has been part of over the years.
* `tba.team_social_media(team)` - Get data on a team's social media profiles.
* `tba.events([year], [keys], [simple])` - Get a list of all events. _OPTIONAL: Include a year to get events from that year. Otherwise the current year's events will be returned. You may also specify `keys` or 'simple' as True to get only the keys or simple model of the events rather than full data, respectively. If both 'keys' and 'simple' are true, then it will return keys._
* `tba.event(event, [simple])` - Get data about an event. _OPTIONAL: Specify `simple` as `True` to get simpler data on an event. Recommended unless you need the extra data._
* `tba.event_rankings(event)` - Gets a list of team rankings at a given event.
* `tba.event_alliances(event)` - Get sophisticated data on alliances at a given event.
* `tba.event_district_points(event)` - Get sophisticated data on district points at a given event.
* `tba.event_insights(event)` - Get insight data on a given event.
* `tba.event_oprs(event)` - Get sophisticated data on alliances at a given event.
* `tba.event_predictions(event)` - Get predicted scores for a given event.
* `tba.event_teams(event)` - Get a list of teams at an event.
* `tba.event_awards(event)` - Get the awards from an event.
* `tba.event_matches(event)` - Get a match list of an event.
* `tba.match([key], [year], [event], [type], [number], [round], [simple])` - Get data about a match. You may either pass the match's `key` directly, or pass `year`, `event`, `type`, `match` (the match number), and `round` if applicable (playoffs only). The event year may be specified as part of the event key or specified in the `year` parameter. _OPTIONAL: Specify `simple` as `True` to get simpler data on the match. Recommended unless you need the extra information._
* `tba.districts(year)` - Get a list of all districts that exist(ed) in a given year.
* `tba.district_events(district, [keys])` - Get list of events in a district. _OPTIONAL: Specify `keys` as `True` to only fetch a list of event keys rather than their full data._
* `tba.district_rankings(district)` - Get the rankings in a district.
* `tba.district_teams(district, [keys])` - Get a list of the teams in a district. _OPTIONAL: Specify `keys` as `True` to only fetch a list of team keys rather than their full data._

See `example.py` for several usage examples.

Documentation for The Blue Alliance's API can be found [here](https://www.thebluealliance.com/apidocs).

## Authors
This software was created and is maintained by [Erik Boesen](https://github.com/ErikBoesen) with [Team 1418](https://github.com/frc1418). Additional contributions made by [Ian Weiss](https://github.com/endreman0) with [Team 4131](https://github.com/FRC4131).

## License
This software is protected under the [MIT License](LICENSE).
