# Tennis Tournament Analysis System API Documentation

## Overview

This document provides detailed information about the Tennis Tournament Analysis System API endpoints, request/response formats, and usage examples.

## Base URL

- Development: `http://localhost:8000`
- Production: TBD

## API Endpoints

### Root Endpoints

#### GET /

Returns basic information about the API.

**Response Example:**
```json
{
  "message": "Welcome to the Tennis Tournament Analysis System API",
  "status": "operational",
  "version": "0.1.0"
}
```

#### GET /health

Health check endpoint to verify the API is running.

**Response Example:**
```json
{
  "status": "healthy",
  "api_version": "0.1.0"
}
```

### Tournaments

#### GET /tournaments

Get a list of all tournaments.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip for pagination. Default: 0
- `limit` (integer, optional): Maximum number of records to return. Default: 100

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Wimbledon 2025",
    "location": "London, UK",
    "start_date": "2025-06-28T00:00:00",
    "end_date": "2025-07-11T00:00:00",
    "surface": "grass",
    "category": "Grand Slam"
  },
  {
    "id": 2,
    "name": "French Open 2025",
    "location": "Paris, France",
    "start_date": "2025-05-26T00:00:00",
    "end_date": "2025-06-09T00:00:00",
    "surface": "clay",
    "category": "Grand Slam"
  }
]
```

#### POST /tournaments

Create a new tournament.

**Request Body:**
```json
{
  "name": "Australian Open 2026",
  "location": "Melbourne, Australia",
  "start_date": "2026-01-18T00:00:00",
  "end_date": "2026-01-31T00:00:00",
  "surface": "hard",
  "category": "Grand Slam"
}
```

**Response Example:**
```json
{
  "id": 3,
  "name": "Australian Open 2026",
  "location": "Melbourne, Australia",
  "start_date": "2026-01-18T00:00:00",
  "end_date": "2026-01-31T00:00:00",
  "surface": "hard",
  "category": "Grand Slam"
}
```

#### GET /tournaments/{tournament_id}

Get detailed information about a specific tournament.

**Path Parameters:**
- `tournament_id` (integer, required): ID of the tournament

**Response Example:**
```json
{
  "id": 1,
  "name": "Wimbledon 2025",
  "location": "London, UK",
  "start_date": "2025-06-28T00:00:00",
  "end_date": "2025-07-11T00:00:00",
  "surface": "grass",
  "category": "Grand Slam",
  "matches": [
    {
      "id": 1,
      "tournament_id": 1,
      "round": "Final",
      "player1": "Roger Federer",
      "player2": "Novak Djokovic",
      "score": "6-4, 7-6, 6-3",
      "date": "2025-07-11T14:00:00",
      "duration": 165
    }
  ]
}
```

#### PUT /tournaments/{tournament_id}

Update a tournament's information.

**Path Parameters:**
- `tournament_id` (integer, required): ID of the tournament

**Request Body:**
```json
{
  "name": "Wimbledon Championships 2025",
  "location": "London, UK",
  "start_date": "2025-06-28T00:00:00",
  "end_date": "2025-07-11T00:00:00",
  "surface": "grass",
  "category": "Grand Slam"
}
```

**Response:** Updated tournament object

#### DELETE /tournaments/{tournament_id}

Delete a tournament.

**Path Parameters:**
- `tournament_id` (integer, required): ID of the tournament

**Response:** HTTP 204 No Content

#### GET /tournaments/{tournament_id}/matches

Get all matches for a specific tournament.

**Path Parameters:**
- `tournament_id` (integer, required): ID of the tournament

**Response:** Array of match objects

### Matches

#### GET /matches

Get a list of all matches with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip for pagination. Default: 0
- `limit` (integer, optional): Maximum number of records to return. Default: 100
- `tournament_id` (integer, optional): Filter by tournament ID
- `player` (string, optional): Filter by player name (partial match)

**Response Example:**
```json
[
  {
    "id": 1,
    "tournament_id": 1,
    "round": "Final",
    "player1": "Roger Federer",
    "player2": "Novak Djokovic",
    "score": "6-4, 7-6, 6-3",
    "date": "2025-07-11T14:00:00",
    "duration": 165
  },
  {
    "id": 2,
    "tournament_id": 1,
    "round": "Semi-final",
    "player1": "Roger Federer",
    "player2": "Rafael Nadal",
    "score": "7-6, 1-6, 6-3, 6-4",
    "date": "2025-07-09T14:00:00",
    "duration": 195
  }
]
```

#### POST /matches

Create a new match.

**Request Body:**
```json
{
  "tournament_id": 1,
  "round": "Quarter-final",
  "player1": "Roger Federer",
  "player2": "Andy Murray",
  "score": "6-4, 6-2, 6-4",
  "date": "2025-07-07T14:00:00",
  "duration": 120
}
```

**Response:** Created match object

#### GET /matches/{match_id}

Get detailed information about a specific match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response Example:**
```json
{
  "id": 1,
  "tournament_id": 1,
  "round": "Final",
  "player1": "Roger Federer",
  "player2": "Novak Djokovic",
  "score": "6-4, 7-6, 6-3",
  "date": "2025-07-11T14:00:00",
  "duration": 165,
  "points": [
    {
      "id": 1,
      "match_id": 1,
      "point_number": 1,
      "game_score": "0-0",
      "point_score": "0-0",
      "server": "Roger Federer",
      "winner": "Roger Federer",
      "first_serve_in": true,
      "serve_type": "wide",
      "return_type": null,
      "rally_length": 1,
      "winning_shot": "ace"
    }
  ]
}
```

#### PUT /matches/{match_id}

Update a match's information.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Request Body:**
```json
{
  "tournament_id": 1,
  "round": "Final",
  "player1": "Roger Federer",
  "player2": "Novak Djokovic",
  "score": "6-4, 7-6, 6-3",
  "date": "2025-07-11T15:00:00",
  "duration": 175
}
```

**Response:** Updated match object

#### DELETE /matches/{match_id}

Delete a match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response:** HTTP 204 No Content

#### GET /matches/{match_id}/points

Get all points for a specific match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response:** Array of point objects

#### POST /matches/{match_id}/points

Add a point to a match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Request Body:**
```json
{
  "point_number": 2,
  "game_score": "0-0",
  "point_score": "15-0",
  "server": "Roger Federer",
  "winner": "Roger Federer",
  "first_serve_in": true,
  "serve_type": "body",
  "return_type": "backhand",
  "rally_length": 5,
  "winning_shot": "forehand winner"
}
```

**Response:** Created point object

### Points

#### GET /points/{point_id}

Get detailed information about a specific point.

**Path Parameters:**
- `point_id` (integer, required): ID of the point

**Response:** Point object

#### PUT /points/{point_id}

Update a point's information.

**Path Parameters:**
- `point_id` (integer, required): ID of the point

**Request Body:**
```json
{
  "match_id": 1,
  "point_number": 2,
  "game_score": "0-0",
  "point_score": "15-0",
  "server": "Roger Federer",
  "winner": "Roger Federer",
  "first_serve_in": true,
  "serve_type": "body",
  "return_type": "backhand",
  "rally_length": 6,
  "winning_shot": "forehand winner"
}
```

**Response:** Updated point object

#### DELETE /points/{point_id}

Delete a point.

**Path Parameters:**
- `point_id` (integer, required): ID of the point

**Response:** HTTP 204 No Content

### Analyses

#### GET /analyses

Get a list of all analyses with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip for pagination. Default: 0
- `limit` (integer, optional): Maximum number of records to return. Default: 100
- `user_id` (integer, optional): Filter by user ID
- `match_id` (integer, optional): Filter by match ID

**Response:** Array of analysis objects

#### POST /analyses

Create a new analysis.

**Request Body:**
```json
{
  "user_id": 1,
  "match_id": 1,
  "title": "Federer vs Djokovic Final Analysis",
  "content": "Detailed analysis of the match...",
  "tournament_info": {
    "key_stats": {
      "aces": {"Federer": 12, "Djokovic": 8},
      "double_faults": {"Federer": 2, "Djokovic": 1}
    }
  },
  "skill_coach": {
    "technical_analysis": {
      "serve": "Excellent wide serves on deuce court",
      "forehand": "Aggressive forehand down the line"
    }
  },
  "orchestrator": {
    "summary": "Federer dominated with his serve and forehand",
    "key_moments": [
      {"game": 5, "set": 1, "description": "Break point conversion"}
    ]
  }
}
```

**Response:** Created analysis object

#### GET /analyses/{analysis_id}

Get detailed information about a specific analysis.

**Path Parameters:**
- `analysis_id` (integer, required): ID of the analysis

**Response:** Analysis object with recommendations

#### PUT /analyses/{analysis_id}

Update an analysis.

**Path Parameters:**
- `analysis_id` (integer, required): ID of the analysis

**Request Body:** Analysis object

**Response:** Updated analysis object

#### DELETE /analyses/{analysis_id}

Delete an analysis.

**Path Parameters:**
- `analysis_id` (integer, required): ID of the analysis

**Response:** HTTP 204 No Content

#### GET /analyses/{analysis_id}/recommendations

Get all recommendations for a specific analysis.

**Path Parameters:**
- `analysis_id` (integer, required): ID of the analysis

**Response:** Array of recommendation objects

### Recommendations

#### PUT /recommendations/{recommendation_id}

Update a recommendation.

**Path Parameters:**
- `recommendation_id` (integer, required): ID of the recommendation

**Request Body:**
```json
{
  "title": "Improve second serve",
  "description": "Focus on increasing second serve percentage",
  "category": "Technical",
  "priority": 1,
  "completed": false
}
```

**Response:** Updated recommendation object

#### PUT /recommendations/{recommendation_id}/complete

Mark a recommendation as complete.

**Path Parameters:**
- `recommendation_id` (integer, required): ID of the recommendation

**Response:** Updated recommendation object

### Agents

#### POST /agents/analyze

Trigger a match analysis using the agent system.

**Request Body:**
```json
{
  "match_id": 1,
  "user_id": 1,
  "analysis_type": "full"
}
```

**Analysis Types:**
- `full`: Run all agents (tournament_info, skill_coach, orchestrator)
- `tournament_info`: Run only the tournament info agent
- `skill_coach`: Run only the skill coach agent
- `orchestrator`: Run only the orchestrator agent

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### GET /agents/status/{job_id}

Check the status of an analysis job.

**Path Parameters:**
- `job_id` (string, required): ID of the job

**Response Example:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": 60,
  "result_id": null,
  "error": null
}
```

**Status Values:**
- `pending`: Job is queued but not started
- `in_progress`: Job is running
- `completed`: Job has completed successfully
- `failed`: Job has failed

#### GET /agents/orchestrator/{match_id}

Get orchestrator agent insights for a match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response:** Orchestrator analysis JSON

#### GET /agents/tournament-info/{match_id}

Get tournament info agent insights for a match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response:** Tournament info analysis JSON

#### GET /agents/skill-coach/{match_id}

Get skill coach agent insights for a match.

**Path Parameters:**
- `match_id` (integer, required): ID of the match

**Response:** Skill coach analysis JSON

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request was successful
- `201 Created`: A new resource was created successfully
- `204 No Content`: The request was successful but there is no content to return
- `400 Bad Request`: The request was malformed or invalid
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

Error responses will have the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

- 100 requests per minute per user
- 1000 requests per day per user

## Authentication

Authentication will be implemented in a future version of the API.
