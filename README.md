# SynAI

Offline-first desktop AI assistant and intelligent agent platform.

## Overview

SynAI is a modular desktop application designed to evolve into a multi-agent system. It implements a layered architecture with clear separation of concerns across presentation, orchestration, AI services, automation, memory, and extensibility layers.

## Architecture

```
Presentation Layer
        ↓
Orchestration Layer
        ↓
Intelligence Layer (AI Services)
        ↓
Automation Layer
        ↓
Memory Layer
        ↓
Extension Layer (Plugins)
```

## Requirements

- Python 3.13+
- Ollama (for local LLM)
- SQLite (for persistence)
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SynAI.git
cd SynAI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Getting Started

Run the application:
```bash
python main.py
```

## Project Structure

```
SynAI/
├── main.py                 # Application entry point
├── pyproject.toml          # Project metadata and build config
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
├── README.md               # This file
├── src/
│   ├── config/             # Configuration management
│   │   └── settings.py     # Settings and environment variables
│   ├── core/               # Core application logic
│   │   ├── app.py          # Application bootstrap
│   │   ├── container.py    # Dependency injection container
│   │   ├── orchestrator.py # Central orchestration logic
│   │   ├── executor.py     # Task execution
│   │   └── planner.py      # Task planning
│   ├── utils/              # Shared utilities
│   │   └── logging.py      # Logging configuration
│   ├── agents/             # AI agents
│   ├── services/           # Domain services
│   │   ├── llm/            # LLM integration
│   │   ├── memory/         # Memory management
│   │   ├── browser/        # Browser automation
│   │   ├── desktop/        # Desktop automation
│   │   └── speech/         # Speech processing
│   ├── skills/             # Reusable skills and tools
│   ├── plugins/            # Plugin system
│   └── ui/                 # User interface
├── config/                 # Configuration files
├── data/                   # Runtime data
├── docs/                   # Documentation
├── logs/                   # Application logs
├── test/                   # Tests
└── assests/                # Non-code resources
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

Run checks:
```bash
black src/
isort src/
ruff check src/
mypy src/
```

## Code Standards

- Python 3.13+ with full type hints
- SOLID principles and composition over inheritance
- Dependency injection for all services
- Rich logging with structured output
- Comprehensive docstrings for all public APIs
- No placeholders or unfinished code
- Production-quality implementations only

## Configuration

Configuration is managed through:
1. `.env` file (local environment variables)
2. `src/config/settings.py` (typed settings with Pydantic)

Environment variables are loaded automatically on application start.

## Logging

The application uses Python's logging module with Rich console formatting. Logs are written to:
- Console (formatted output)
- Files in `logs/` directory

Log level can be configured via `APP_LOG_LEVEL` environment variable.

## Contributing

1. Follow the code standards outlined in `docs/coding_standards.md`
2. Maintain the architecture specified in `docs/project_spec.md`
3. Add tests for new functionality
4. Ensure all tests pass and code quality checks succeed

## License

MIT

## Roadmap

See `docs/roadmap.md` for planned features and milestones.