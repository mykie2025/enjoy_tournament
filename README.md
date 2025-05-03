# Tennis Tournament Analysis System

A multi-agent AI system designed to help tennis players improve their skills by analyzing professional tournaments and providing personalized recommendations.

## Overview

This system uses three specialized AI agents:

1. **Orchestrator Agent** - Coordinates the analysis workflow and synthesizes insights
2. **Tournament Info Agent** - Analyzes tennis matches and extracts key patterns from multiple data sources
3. **Tennis Skill Coach Agent** - Provides technical and strategic tennis advice

## Features

- Match analysis with point-by-point breakdown
- Technical skill assessment and recommendations
- Strategy analysis and tactical insights
- Interactive web interface for visualization
- Multi-source tournament data integration (SportRadar API, local database, etc.)
- Real-time tournament and match information
- Head-to-head player statistics and analysis

## Documentation

- [Solution Design](/docs/solution_design.md)
- [Project Tracker](/docs/project.md)
- [Initial Ideas](/docs/ideas.md)
- [SportRadar API Reference](/docs/reference/developer.sportradar.com_tennis_reference_overview.md)

## Tech Stack

- Frontend: Next.js, React, Tailwind CSS
- Backend: Python, FastAPI
- Data Sources: SportRadar API, Tennis-Data API, Tennis Tour API, Local Database
- AI: OpenAI-compatible endpoints with Google ADK/A2A Framework

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- SportRadar API key (set in .env file)

### Installation

1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`

### Running the Application

1. Start the backend server: `python run.py --run-server`
2. Start the frontend development server: `node run_frontend.js`
3. Access the application at `http://localhost:9099`

### Configuration

The application uses a central configuration file (`config.yml`) to manage settings for both backend and frontend:

```yaml
# Server Configuration
server:
  api:
    host: localhost
    port: 9000
  frontend:
    host: localhost
    port: 9099
```

You can customize the configuration by editing the `config.yml` file. Key configuration options include:

- Server ports and hosts for API and frontend
- Data source settings (SportRadar API, Tennis-Data API, etc.)
- Agent parameters (model names, temperatures, etc.)
- UI settings (refresh intervals, display limits)

To use a custom configuration file, use the `--config` option:

```bash
python run.py --run-server --config /path/to/custom/config.yml
```

## Features

### Tournament Info Page

The Tournament Info page provides comprehensive information about tennis tournaments, including:

- Live matches with real-time scores and statistics
- Upcoming matches with schedule information
- Player profiles and head-to-head statistics
- Tournament details and historical data

## License

MIT
