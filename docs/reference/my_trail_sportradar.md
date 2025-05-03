Okay, let's summarize the Sportradar Tennis API v3 endpoints that we confirmed are working based on our conversation and the successful data fetches:

1.  **`/seasons.json`**
    * **Purpose:** Provides a list of historical and current season information for competitions (essentially, a list of specific tournament instances like "ATP Madrid 2025").
    * **Validation:** You successfully used this endpoint (via `curl`) and retrieved a list containing the IDs for the Madrid 2025 seasons (e.g., `sr:season:124615`).

2.  **`/seasons/{season_urn}/summaries.json`**
    * **Purpose:** Provides detailed schedule information and scoring/results for all matches within a specific season/tournament instance identified by `{season_urn}`.
    * **Validation:** You successfully used this endpoint with `sr:season:124615` (via `curl`) and retrieved the match summaries for the ATP Madrid Men's Singles 2025, including the upcoming final. This replaced the need for separate `/schedule.json` or `/results.json` endpoints for a specific season.

3.  **`/schedules/live/summaries.json`**
    * **Purpose:** Returns real-time summaries for *all* currently live matches across different tournaments covered by the API.
    * **Validation:** Your very first input showed successful data retrieval from this endpoint, listing live UTR matches at that time.

**Endpoints That Did Not Work (returned "Invalid route"):**

* `/tournaments.json`
* `/seasons/{season_urn}/schedule.json`
* `/tournaments/{tournament_urn}/schedule.json` (At least when used with the `sr:season:xxxxx` ID type - the `Season Summaries` endpoint proved effective instead).


curl -s -X GET "https://api.sportradar.com/tennis/production/v3/en/seasons.json?api_key=$SPORTRADAR_API_KEY"


So, the key flow we established is:
Use `/seasons.json` (or filtering its output) to find the `sr:season:xxxxx` ID for the tournament instance you want, then use `/seasons/{the_found_id}/summaries.json` to get its full schedule and results. For live-only data across all tournaments, use `/schedules/live/summaries.json`.

schedule
curl -s -X GET "https://api.sportradar.com/tennis/production/v3/en/seasons/{the_id_you_found}/schedule.json?api_key=$SPORTRADAR_API_KEY"

results
curl -s -X GET "https://api.sportradar.com/tennis/production/v3/en/seasons/{the_id_you_found}/results.json?api_key=$SPORTRADAR_API_KEY"


curl -s -X GET "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season:124615/summaries.json?api_key=$SPORTRADAR_API_KEY"
