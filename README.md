# tbapy

[![PyPI version](https://badge.fury.io/py/tbapy.svg)](https://badge.fury.io/py/tbapy)

Python library to get data from The Blue Alliance. _Uses v3 of the TBA API._

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
You may specify `simple=True` to get only vital data on some models or lists of models, or you may specify `keys=True` to get a list of the keys for a list rather than full data on each model. It is recommended to use these options if you do not need full data.

Some requests support `year` and other optional parameters, which are recommended to use to narrow down your results.
* `tba.status()` - Get TBA's status.
* `tba.teams(page, [year], [simple/keys])` - Get a list of of valid teams, where `page * 500` is the starting team number.
* `tba.team(team, [simple])` - Get a team's data. `team` can be an integer team number of a string-form `'frc####'` identifier.
* `tba.team_events(team, [year], [simple/keys])` - Get a list of events a team has been to.
* `tba.team_awards(team, [event/year])` - Get a list of the team's awards.
* `tba.team_matches(team, [event/year], [simple/keys])` - Get a list of a team's matches at an event.
* `tba.team_years(team)` - Get a list of years the team was active in FRC.
* `tba.team_media(team, [year], [tag])` - Get team media. Specify a year to get media from or a tag or both.
* `tba.team_robots(team)` - Get data about a team's robots.
* `tba.team_districts(team)` - Get the districts that a team has been part of over the years.
* `tba.team_profiles(team)` - Get data on a team's media profiles.
* `tba.team_status(team, event)` - Get a team's status at an event.
* `tba.events([year], [simple/keys])` - Get a list of all events.
* `tba.event(event, [simple])` - Get data about an event.
* `tba.event_rankings(event)` - Gets a list of team rankings at a given event.
* `tba.event_alliances(event)` - Get sophisticated data on alliances at a given event.
* `tba.event_district_points(event)` - Get sophisticated data on district points at a given event.
* `tba.event_insights(event)` - Get insight data on a given event.
* `tba.event_oprs(event)` - Get sophisticated data on alliances at a given event.
* `tba.event_predictions(event)` - Get predicted scores for a given event.
* `tba.event_teams(event, [simple/keys])` - Get a list of teams at an event.
* `tba.event_awards(event)` - Get the awards from an event.
* `tba.event_matches(event, [simple/keys])` - Get a match list of an event.
* `tba.match([key], [year], [event], [type], [number], [round], [simple])` - Get data about a match. You may either pass the match's `key` directly, or pass `year`, `event`, `type`, `match` (the match number), and `round` if applicable (playoffs only). The event year may be specified as part of the event key or specified in the `year` parameter.
* `tba.districts(year)` - Get a list of all districts that exist(ed) in a given year.
* `tba.district_events(district, [simple/keys])` - Get list of events in a district.
* `tba.district_rankings(district)` - Get the rankings in a district.
* `tba.district_teams(district, [simple/keys])` - Get a list of the teams in a district.

See `example.py` for several usage examples.

Documentation for The Blue Alliance's API can be found [here](https://www.thebluealliance.com/apidocs).

## Authors
This software was created and is maintained by [Erik Boesen](https://github.com/ErikBoesen) with [Team 1418](https://github.com/frc1418). Additional contributions made by [Ian Weiss](https://github.com/endreman0) with [Team 4131](https://github.com/FRC4131).

## License
This software is protected under the [MIT License](LICENSE).
