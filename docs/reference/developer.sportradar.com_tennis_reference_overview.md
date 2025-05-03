# Content from: https://developer.sportradar.com/tennis/reference/overview

Source URL: `https://developer.sportradar.com/tennis/reference/overview`
Fetched on: 2025-05-03 12:56:51 CST

---

Introduction
The Tennis API provides real-time scoring, point-by-point match scoring (when available), and an array of supplementary data.
Over 4,000 competitions are covered and available in one package. Select the Tennis package in our Coverage Matrix for competitions and data offered.
The API is consistent in structure, format, and behavior with the other General Sport APIs. Primary feeds will return seasons, competitions, player data, and real-time scores.
Additional feeds provide a host of complementary stats, including:
- World and race rankings
- Win probabilities for each match
- Player profiles
- Historical results
- Post-match corrections
- In-depth match statistics
Real-time customers are also offered two delivery Push Feeds to enhance speed.
An extended Probabilities package is also offered. This add-on includes live match probability updates and season outrights.
Authentication is required for all API calls.
API Map
To best utilize the Tennis API, you will need several parameters to create your API calls. The map below illustrates how you can obtain the parameters you need.
The primary feeds require only a date or human-readable parameters to call the endpoints. Those feeds provide Sport Event Ids, Competitor Ids, or Season Ids which can be used to generate the match, team, and season feeds.
Endpoint Descriptions
Competition Info – Provides the name, id, and parent id for a given competition.
Competition Seasons – Provides historical season information for a given competition. Competitions will return a maximum of three seasons of data, including current or newly created seasons.
Competitions – Provides a list of all available tennis competitions.
Competitions by Category – Provides a list of all available tennis competitions for a given category (ex. ATP, ITF, or WTA).
Competitor Merge Mappings - Provides the valid Sportradar Id in cases when two competitors have been merged into one. Mapping entries will remain in the feed for 7 days.
Competitor Profile – Provides biographical information for a given player, including current rank, historical statistics, and competition participation.
Competitor Summaries – Provides previous and upcoming match information for a given competitor, including statistics for past matches and scheduling info for upcoming matches.
Competitor vs Competitor – Provides previous and upcoming matches between two teams including scoring information and match statistics.
Complexes – Provides all complexes with venue information.
Daily Summaries – Provides match information for a given day including scoring and match statistics.
Doubles Competitions Played – Returns doubles competitions played and the partners a competitor played with.
Doubles Competitor Rankings – Provides the top 500 doubles competitor rankings for the ATP and WTA.
Doubles Race Rankings – Rankings for the ATP/WTA finals.
Doubles Rankings – Provides rankings in ascending order for doubles teams.
Live Summaries – Returns real-time updates for all currently live matches, including scoring and statistics.
Live Timelines – Provides a real-time play-by-play event timeline for currently live games.
Live Timelines Delta – Provides a 10 second live delta of game information, including scoring and a play-by-play event timeline.
Race Rankings – Returns a list in ascending order for the race to the ATP/WTA finals.
Rankings – Returns a rankings list in ascending order for singles competitors.
Season Competitors – Provides a list of competitors for a given season.
Season Info – Provides detailed information for a given season/tournament, including competitors and structure.
Season Links – Provides information about linked cup rounds for a given season/tournament. Use this feed to compile full advancement brackets for relevant seasons/tournaments. Links between all matches and rounds are available when competitors (TBD vs. TBD) are not yet known.
Season Probabilities – Provides 2-way win probabilities (home team win, away team win) for all matches for a given season.
Season Summaries – Provides schedule information and scoring for all matches from a given season.
Seasons – Provides a list of historical season information for all competitions. Competitions will return a maximum of three seasons of data, including current or newly created seasons.
Sport Event Summary – Provides scheduling information, scoring, and statistics for a given match.
Sport Events Created – Provides ids for sport events that have been created in the last 24 hours.
Sport Event Timeline – Provides scheduling information, scoring, statistics and a play-by-play event timeline for a given match.
Sport Events Removed – Provides ids for sport events that have been removed or deleted.
Sport Events Updated – Provides ids for sport events that have been updated in the last 24 hours.
Push Events – Returns detailed, real-time information on every game event
Push Statistics – Returns detailed game stats at the doubles team or player level
Live Probabilities - Provides top-level information for live matches. If probabilities are available for a match, pre-match and live probabilities will be displayed.
Season Outright Probabilities - Provides a list of outright probabilities for each team from a given season.
Sport Event Probabilities - Provides pre-match and live probabilities for a given match.
Sport Event Upcoming Probabilities - Provides a list of IDs for upcoming sport events in the next 24 hours.
Timeline Probabilities - Provides a timeline of pre-match and live probability changes for a given match.
Probabilities Endpoints
Available only with the probabilities plan within the Tennis v3 package. See FAQ for details.
Data Retrieval Sample
To find the win probabilities for a match, given the date:
- Call the Daily Summaries for the day the sport event takes place and find the Season Id for the chosen sport event
- Make note of the Sport Event Id for the given sport event
- Call the Season Probabilities using the Season Id
- Find Sport Event Id within the results and locate the outcome probability
The probability of a win for each participant is displayed.
Failover Info
If our scout feed goes down or becomes unavailable, Sportradar takes over Live Data Entry (LDE) to provide a failover.
In case of a failover, we follow one of the following scenarios:
- Continue point-by-point coverage – but lose service outcomes. During the failover we cannot provide data related to service outcome. The following data will be unavailable: aces, double faults, service faults, and successful service outcome. Those statistics will be verified and updated post-match.
- If point-by-point coverage is not possible – we will update game-by-game, post-match. During the failover we cannot provide point-by-point coverage and service outcomes. The following data will be unavailable: aces, double faults, service faults, and successful service outcome. Missing point-by-point coverage and statistics will be verified and updated post-match. Tie-break score will not be displayed. Game-by-game coverage will continue as each match ends.
Integration Links
OpenAPI Specs
Our Tennis API is available via OpenAPI. Click below to view and/or download the spec.
Tennis v3 Probabilities OpenAPI
Postman Workspace
Our entire Media APIs are available on Postman. Click the link above to be taken directly to our Tennis API collection.
Feel free to follow and/or fork any collections to receive updates.
Schema Download
Open the zip file below to access our entire Tennis API XSD schema.
