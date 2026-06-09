# Project Structure - AI Docker NL Dashboard

## Complete File Tree

```
docker-nl-dashboard/
│
├── app.py                          # Main Streamlit application (7 pages with routing)
├── agent.py                        # ReAct agent loop (7-step execution)
├── docker_manager.py               # Docker SDK wrapper (all operations)
├── llm.py                          # Ollama integration (NL translation)
├── database.py                     # SQLite management (3 tables)
├── github_api.py                   # GitHub API integration
├── test_demo.py                    # Testing and demo script
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Production container image
├── docker-compose.yml              # Multi-service orchestration
│
├── start.sh                        # Linux/Mac startup script
├── start.bat                       # Windows startup script
│
├── README.md                       # Complete documentation
├── INSTALL.md                      # Installation guide
├── QUICKSTART.md                   # 5-minute setup guide
├── API.md                          # API documentation
├── PROJECT_STRUCTURE.md            # This file
│
├── .gitignore                      # Git ignore rules
├── .env.example                    # Environment variables template
│
├── prompts/
│   └── system_prompt.txt           # LLM system prompt for translation
│
├── data/                           # Data directory (auto-created)
│   └── dashboard.db                # SQLite database (auto-created)
│
└── logs/                           # Logs directory (auto-created)
    └── prompt_log.txt              # Execution logs (auto-created)
```

---

## File Descriptions

### Core Application Files

#### `app.py` (442 lines)
Main Streamlit application with 7 pages:
1. Dashboard - KPI cards and system overview
2. Containers - Table view with management controls
3. AI Agent - Natural language interface with ReAct loop visualization
4. Logs - Prompt logs, audit logs, container history
5. Analytics - Plotly visualizations (bar, pie, timeline charts)
6. GitHub API - GitHub status and events monitoring
7. Settings - Configuration management

**Features:**
- Dark theme with custom CSS
- Sidebar navigation
- Session state management
- Real-time data display
- Interactive controls
- Error handling

#### `agent.py` (234 lines)
ReAct-style agent implementation with 7-step execution:
1. User Request - Accept input
2. AI Analysis - Ollama translation
3. Tool Selection - Determine action
4. Tool Execution - Execute Docker operation
5. Result Collection - Gather data
6. Summary Generation - Human-readable response
7. Response Return - Deliver result

**Features:**
- Step-by-step tracking
- Execution timing
- Database logging
- File logging
- Error handling

#### `docker_manager.py` (272 lines)
Docker SDK wrapper providing:
- `list_containers()` - List with status filtering
- `restart_container()` - Restart containers
- `start_container()` - Start stopped containers
- `stop_container()` - Stop running containers
- `get_container_health()` - Health check status
- `get_container_logs()` - Retrieve logs
- `get_container_resource_usage()` - CPU/memory stats
- `get_system_info()` - Docker system information

**Features:**
- Safe stats collection
- Timeout handling
- Error recovery
- Resource calculation

#### `llm.py` (263 lines)
Ollama LLM integration:
- Natural language to JSON translation
- Human-readable summary generation
- System prompt management
- Connection testing

**Features:**
- Temperature control
- JSON extraction from responses
- Action-specific summarization
- Error detection in logs

#### `database.py` (213 lines)
SQLite database management:
- Schema initialization (3 tables)
- Prompt logging
- Container history tracking
- Audit trail logging
- Query methods for all tables
- Statistics aggregation

**Tables:**
- `prompt_logs` - NL command execution
- `container_history` - Container state tracking
- `audit_logs` - Action audit trail

#### `github_api.py` (105 lines)
GitHub API integration:
- `get_status()` - GitHub system status
- `get_public_events()` - Recent public events
- `get_rate_limit()` - API rate limits
- `search_repositories()` - Repo search

**Features:**
- Proper headers
- Timeout handling
- Error recovery
- Response parsing

---

### Configuration Files

#### `requirements.txt`
Python dependencies:
- streamlit>=1.28.0
- docker>=6.1.0
- pandas>=2.0.0
- plotly>=5.17.0
- requests>=2.31.0
- ollama>=0.1.0

#### `Dockerfile`
Multi-stage production container:
- Python 3.11 slim base
- System dependencies (curl, ca-certificates)
- Python dependencies installation
- Directory creation
- Health check
- Streamlit configuration
- Port exposure (8501)

#### `docker-compose.yml`
Multi-service orchestration:
- **ollama** service: LLM backend
- **dashboard** service: Application
- Volume mounts: Docker socket, data, logs
- Health checks
- Network configuration
- Auto-restart policies

#### `.env.example`
Environment variables template:
- Docker configuration
- Ollama settings
- Database paths
- Streamlit options
- Logging configuration

---

### Scripts

#### `start.sh` (Linux/Mac)
Startup script that:
- Checks Docker is running
- Checks Ollama is running
- Offers to pull llama3 model
- Creates directories
- Installs dependencies if needed
- Starts Streamlit

#### `start.bat` (Windows)
Windows equivalent of start.sh

#### `test_demo.py`
Automated testing script:
- Creates test containers (nginx, redis, mysql)
- Tests natural language commands
- Generates expected output
- Offers cleanup

---

### Documentation Files

#### `README.md` (495 lines)
Complete documentation:
- Features overview
- Requirements
- Quick start guides
- Project structure
- Example commands
- Testing instructions
- Database schema
- Configuration
- Troubleshooting
- Performance notes
- Security notes
- Deployment guides

#### `INSTALL.md` (410 lines)
Detailed installation guide:
- Prerequisites
- 3 installation methods
- Post-installation steps
- Verification checklist
- Troubleshooting section
- Uninstallation guide
- System requirements

#### `QUICKSTART.md` (245 lines)
5-minute setup guide:
- Fastest installation method
- Quick test instructions
- Command reference table
- Common tasks
- Expected results
- Troubleshooting quick fixes

#### `API.md` (580 lines)
API documentation:
- All classes and methods
- Parameters and return values
- Code examples
- Action schema
- Error handling
- Database schema
- Integration examples
- Extension points
- Performance tips

#### `PROJECT_STRUCTURE.md` (This file)
Project organization and file descriptions

---

### Prompt Files

#### `prompts/system_prompt.txt`
System prompt for Ollama:
- Action definitions
- JSON format specifications
- Example translations
- Rules and constraints

**Used by:** `llm.py` to translate natural language to actions

---

### Data Files (Auto-created)

#### `data/dashboard.db`
SQLite database with 3 tables:
- prompt_logs (execution history)
- container_history (state tracking)
- audit_logs (action trail)

**Created by:** `database.py` on first run

#### `logs/prompt_log.txt`
Text file with timestamped execution logs:
- User prompts
- Generated actions
- Execution results
- Timing information

**Created by:** `agent.py` during execution

---

## Component Dependencies

```
app.py
├── agent.py
│   ├── llm.py
│   ├── docker_manager.py
│   └── database.py
├── docker_manager.py
├── database.py
├── github_api.py
└── llm.py

docker-compose.yml
├── Dockerfile
└── requirements.txt

start.sh / start.bat
└── requirements.txt

test_demo.py
└── agent.py
    └── (all dependencies)
```

---

## Execution Flow

### User Command Flow

```
User Input (app.py - AI Agent page)
    ↓
ReactAgent.execute() (agent.py)
    ↓
Step 1: Accept Request
    ↓
Step 2: LLMManager.translate_to_action() (llm.py)
    ↓ Ollama API call
    ↓ JSON action returned
    ↓
Step 3: Tool Selection
    ↓
Step 4: DockerManager.{operation}() (docker_manager.py)
    ↓ Docker SDK call
    ↓ Result returned
    ↓
Step 5: Collect Results
    ↓
Step 6: LLMManager.generate_summary() (llm.py)
    ↓ Human-readable summary
    ↓
Step 7: Response Return
    ↓
Database.log_prompt() (database.py)
    ↓
Display in Streamlit (app.py)
```

---

## Data Flow

### Database Writes

```
Agent Execution → database.py
    ├── prompt_logs (every command)
    ├── container_history (list operations)
    └── audit_logs (state changes)

File System → logs/prompt_log.txt
    └── Timestamped execution logs
```

### Database Reads

```
Streamlit Pages → database.py
    ├── Logs Page → get_prompt_logs()
    ├── Logs Page → get_audit_logs()
    ├── Logs Page → get_container_history()
    └── Analytics → get_container_stats_summary()
```

---

## External Integrations

### Docker
- **Connection:** Unix socket (`/var/run/docker.sock`)
- **Library:** Docker SDK for Python
- **Operations:** List, start, stop, restart, logs, stats, health

### Ollama
- **Connection:** HTTP (default: `localhost:11434`)
- **Library:** ollama-python
- **Model:** llama3
- **Operations:** Chat completions for NL translation

### GitHub
- **Connection:** HTTPS (api.github.com)
- **Library:** requests
- **Authentication:** None (public endpoints)
- **Operations:** Status, events, rate limits

---

## Security Boundaries

### Docker Socket Access
- Mounted read-only in production
- Full control in development
- User must be in docker group (Linux)

### Database
- Local SQLite file
- File permissions control access
- No network exposure

### Ollama
- Local HTTP endpoint
- No authentication required
- Model runs locally (no external API)

### GitHub API
- Public endpoints only
- Rate limited (60 requests/hour unauthenticated)
- No secrets required

---

## Configuration Points

### Environment Variables
- `DOCKER_HOST` - Docker connection
- `OLLAMA_HOST` - Ollama endpoint
- `OLLAMA_MODEL` - Model name
- `DATABASE_PATH` - Database location
- `LOG_FILE_PATH` - Log file location
- `STREAMLIT_SERVER_PORT` - Web port

### Code Configuration
- `database.py` - Database schema
- `prompts/system_prompt.txt` - LLM behavior
- `app.py` - UI layout and styling
- `docker_manager.py` - Docker operations

---

## Extending the Application

### Add New Docker Operation

1. Add method to `docker_manager.py`
2. Update `agent.py` `_execute_tool()`
3. Add action to `prompts/system_prompt.txt`
4. Add summary logic to `llm.py`

### Add New Page

1. Add page option to sidebar in `app.py`
2. Create page section with `if page == "New Page":`
3. Import required modules
4. Implement page logic

### Add New Database Table

1. Add schema in `database.py` `init_database()`
2. Add insert method
3. Add query method
4. Use in relevant components

---

## Lines of Code Summary

| File | Lines | Purpose |
|------|-------|---------|
| app.py | 442 | Main UI application |
| agent.py | 234 | ReAct agent loop |
| docker_manager.py | 272 | Docker operations |
| llm.py | 263 | LLM integration |
| database.py | 213 | Database management |
| github_api.py | 105 | GitHub API |
| test_demo.py | 180 | Testing script |
| **Total Core** | **1,709** | **Production code** |

---

## Disk Space Requirements

- **Application Code:** <1 MB
- **Python Dependencies:** ~500 MB
- **Ollama llama3 Model:** ~4.7 GB
- **Database (typical):** <10 MB
- **Logs (typical):** <5 MB
- **Total:** ~5.2 GB

---

## Runtime Memory Usage

- **Streamlit App:** ~150 MB
- **Ollama (llama3):** ~4-8 GB
- **Docker SDK:** ~50 MB
- **Total:** ~4.5-8.5 GB

**Recommendation:** 8GB+ RAM for smooth operation

---

**Project Status:** Production Ready ✅  
**Completeness:** 100% - Zero Placeholders  
**Documentation:** Complete  
**Version:** 1.0.0
