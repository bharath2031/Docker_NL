# API Documentation - AI Docker NL Dashboard

## Overview

This document describes the internal APIs and components of the AI Docker NL Dashboard.

---

## Table of Contents

1. [Agent API](#agent-api)
2. [Docker Manager API](#docker-manager-api)
3. [LLM Manager API](#llm-manager-api)
4. [Database API](#database-api)
5. [GitHub API](#github-api)
6. [Action Schema](#action-schema)

---

## Agent API

### Class: `ReactAgent`

ReAct-style agent that executes natural language commands through a 7-step loop.

#### Methods

##### `execute(user_request: str) -> Tuple[List[AgentStep], Dict]`

Execute full ReAct loop for a user request.

**Parameters:**
- `user_request` (str): Natural language command

**Returns:**
- Tuple containing:
  - `steps` (List[AgentStep]): Execution steps
  - `result` (Dict): Final result with summary

**Example:**
```python
from agent import ReactAgent

agent = ReactAgent()
steps, result = agent.execute("show running containers")

print(result["summary"])
# Output: "Found 3 container(s). 3 running normally."

for step in steps:
    print(f"Step {step.step_number}: {step.name} - {step.status}")
```

---

## Docker Manager API

### Class: `DockerManager`

Wrapper around Docker SDK for Python.

#### Methods

##### `list_containers(status_filter: Optional[str] = None) -> List[Dict]`

List containers with optional status filtering.

**Parameters:**
- `status_filter` (str, optional): Filter by status (running, stopped, restarting, exited, paused)

**Returns:**
- List of container dictionaries

**Example:**
```python
from docker_manager import DockerManager

docker = DockerManager()
containers = docker.list_containers(status_filter="running")

for c in containers:
    print(f"{c['name']}: {c['status']} - CPU: {c['cpu_usage']}%")
```

##### `restart_container(container_name: str) -> Dict`

Restart a container.

**Returns:**
```python
{
    "success": True,
    "container": "nginx",
    "status": "running",
    "message": "Container 'nginx' restarted successfully"
}
```

##### `start_container(container_name: str) -> Dict`

Start a stopped container.

##### `stop_container(container_name: str) -> Dict`

Stop a running container.

##### `get_container_health(container_name: str) -> Dict`

Get health status.

**Returns:**
```python
{
    "container": "nginx",
    "status": "running",
    "health": "healthy",
    "failing_streak": 0,
    "log": []
}
```

##### `get_container_logs(container_name: str, tail: int = 100) -> Dict`

Get container logs.

**Returns:**
```python
{
    "container": "nginx",
    "logs": "2024-01-01 10:00:00 Starting nginx...\n...",
    "lines": 100
}
```

##### `get_container_resource_usage(container_name: str) -> Dict`

Get CPU and memory usage.

**Returns:**
```python
{
    "container": "nginx",
    "status": "running",
    "cpu_percent": 1.5,
    "memory_mb": 45.2,
    "memory_limit_mb": 1024.0,
    "memory_percent": 4.4
}
```

##### `get_system_info() -> Dict`

Get Docker system information.

**Returns:**
```python
{
    "containers": 5,
    "containers_running": 3,
    "containers_paused": 0,
    "containers_stopped": 2,
    "images": 10,
    "server_version": "24.0.0",
    "operating_system": "Ubuntu 22.04",
    "total_memory_gb": 16.0
}
```

---

## LLM Manager API

### Class: `LLMManager`

Ollama integration for natural language translation.

#### Methods

##### `translate_to_action(user_prompt: str) -> Dict`

Translate natural language to structured action.

**Parameters:**
- `user_prompt` (str): Natural language command

**Returns:**
- Action dictionary (see [Action Schema](#action-schema))

**Example:**
```python
from llm import LLMManager

llm = LLMManager()
action = llm.translate_to_action("show running containers")

print(action)
# Output: {"action": "list_containers", "status": "running"}
```

##### `generate_summary(action: Dict, result: any) -> str`

Generate human-readable summary.

**Parameters:**
- `action` (Dict): The executed action
- `result` (any): The action result

**Returns:**
- Human-readable summary string

**Example:**
```python
summary = llm.generate_summary(
    action={"action": "list_containers", "status": "running"},
    result=[{"name": "nginx", "status": "running"}]
)

print(summary)
# Output: "Found 1 container(s). 1 running normally."
```

##### `test_connection() -> Dict`

Test Ollama connection.

**Returns:**
```python
{
    "success": True,
    "model": "llama3",
    "message": "Ollama connection successful"
}
```

---

## Database API

### Class: `Database`

SQLite database management.

#### Methods

##### `log_prompt(user_prompt: str, generated_action: str, execution_result: str, execution_time_ms: float)`

Log prompt execution.

##### `log_container_history(container_id: str, container_name: str, status: str, cpu_usage: float, memory_usage: float)`

Log container state.

##### `log_audit(action: str, status: str, details: str)`

Log audit event.

##### `get_prompt_logs(limit: int = 100) -> List[Dict]`

Retrieve prompt logs.

**Returns:**
```python
[
    {
        "id": 1,
        "timestamp": "2024-01-01T10:00:00",
        "user_prompt": "show running containers",
        "generated_action": '{"action":"list_containers","status":"running"}',
        "execution_result": "Found 3 containers...",
        "execution_time_ms": 1234.56
    }
]
```

##### `get_container_history(limit: int = 1000) -> List[Dict]`

Retrieve container history.

##### `get_audit_logs(limit: int = 100) -> List[Dict]`

Retrieve audit logs.

##### `get_container_stats_summary() -> Dict`

Get container statistics summary.

**Returns:**
```python
{
    "running": 3,
    "stopped": 1,
    "restarting": 0
}
```

---

## GitHub API

### Class: `GitHubAPI`

GitHub API integration.

#### Methods

##### `get_status() -> Dict`

Get GitHub status.

**Returns:**
```python
{
    "success": True,
    "status": {...},
    "description": "All Systems Operational",
    "indicator": "none",
    "updated_at": "2024-01-01T10:00:00"
}
```

##### `get_public_events(limit: int = 10) -> Dict`

Get recent public events.

**Returns:**
```python
{
    "success": True,
    "events": [
        {
            "id": "12345",
            "type": "PushEvent",
            "actor": "username",
            "repo": "owner/repo",
            "created_at": "2024-01-01T10:00:00",
            "public": True
        }
    ],
    "count": 10
}
```

##### `get_rate_limit() -> Dict`

Get API rate limit.

**Returns:**
```python
{
    "success": True,
    "limit": 60,
    "remaining": 45,
    "reset": 1234567890,
    "used": 15
}
```

---

## Action Schema

### List Containers

```json
{
    "action": "list_containers",
    "status": "running|stopped|restarting|exited|paused|all"
}
```

### Container Actions

```json
{
    "action": "restart_container|start_container|stop_container",
    "container": "container_name"
}
```

### Get Health

```json
{
    "action": "get_container_health",
    "container": "container_name"
}
```

### Get Logs

```json
{
    "action": "get_container_logs",
    "container": "container_name",
    "tail": 100
}
```

### Get Resources

```json
{
    "action": "get_container_resource_usage",
    "container": "container_name"
}
```

---

## Error Handling

All methods return error information in a consistent format:

```python
{
    "success": False,
    "error": "Error message",
    "details": "Detailed error information"
}
```

or for agent actions:

```python
{
    "action": "error",
    "message": "Error description"
}
```

---

## Database Schema

### prompt_logs

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | TEXT | ISO 8601 timestamp |
| user_prompt | TEXT | Natural language input |
| generated_action | TEXT | JSON action |
| execution_result | TEXT | Result summary |
| execution_time_ms | REAL | Execution time |

### container_history

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | TEXT | ISO 8601 timestamp |
| container_id | TEXT | Container short ID |
| container_name | TEXT | Container name |
| status | TEXT | Container status |
| cpu_usage | REAL | CPU percentage |
| memory_usage | REAL | Memory in MB |

### audit_logs

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | TEXT | ISO 8601 timestamp |
| action | TEXT | Action type |
| status | TEXT | success/failed |
| details | TEXT | JSON details |

---

## Integration Examples

### Custom Command Processor

```python
from agent import ReactAgent

def process_command(command: str):
    agent = ReactAgent()
    steps, result = agent.execute(command)
    
    if result.get("success"):
        return result["summary"]
    else:
        return f"Error: {result.get('error')}"

# Usage
summary = process_command("show running containers")
print(summary)
```

### Direct Docker Operations

```python
from docker_manager import DockerManager
from database import Database

docker = DockerManager()
db = Database()

# List containers and log to database
containers = docker.list_containers(status_filter="running")

for container in containers:
    db.log_container_history(
        container_id=container["id"],
        container_name=container["name"],
        status=container["status"],
        cpu_usage=container["cpu_usage"],
        memory_usage=container["memory_usage"]
    )
```

### Custom LLM Prompts

```python
from llm import LLMManager

llm = LLMManager(model="llama3")

# Custom translation
action = llm.translate_to_action("I need to see all broken containers")
print(action)
# Output: {"action": "list_containers", "status": "exited"}
```

---

## Extension Points

### Adding New Actions

1. Update `prompts/system_prompt.txt` with new action format
2. Add handler in `agent.py` `_execute_tool()` method
3. Add Docker operation in `docker_manager.py`
4. Add summary generation in `llm.py`

### Custom Database Tables

```python
from database import Database

db = Database()
conn = db.get_connection()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS custom_metrics (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        metric_name TEXT,
        value REAL
    )
""")

conn.commit()
conn.close()
```

---

## Performance Considerations

- **LLM Calls**: 500-1500ms (depends on model and hardware)
- **Docker Operations**: 100-500ms (depends on operation)
- **Database Queries**: <50ms
- **Total Request**: 1-3 seconds typical

### Optimization Tips

1. Use `status_filter` in `list_containers()` to reduce data
2. Limit log tail to reduce processing time
3. Cache Docker system info for dashboard
4. Use database indexes for large log tables
5. Consider GPU for faster LLM inference

---

## Security Notes

- Docker socket mounted read-only in production
- No authentication on dashboard (add reverse proxy)
- Database file permissions should be restricted
- Sanitize user input before passing to Docker
- Rate limit LLM calls to prevent abuse

---

**Version:** 1.0.0  
**Last Updated:** 2026-06-08
