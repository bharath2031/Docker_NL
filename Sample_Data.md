# Sample Data

## Project: AI Docker Natural Language Health Dashboard

---

## Sample Docker Containers (Test Setup)

Run the following to create sample containers for testing:

```bash
docker run -d --name nginx-test nginx
docker run -d --name redis-test redis
docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=test mysql
```

---

## Sample Dashboard Output

### KPI Cards (Dashboard Page)

| Metric | Value |
|--------|-------|
| Total Containers | 3 |
| Running | 3 |
| Stopped | 0 |
| Restarting | 0 |
| Unhealthy | 0 |

---

### Container Table (Containers Page)

| Name | Status | Image | CPU % | Memory MB | ID |
|------|--------|-------|-------|-----------|----|
| nginx-test | running | nginx | 0.5 | 50.2 | abc123 |
| redis-test | running | redis | 0.2 | 15.8 | def456 |
| mysql-test | running | mysql | 2.3 | 380.5 | ghi789 |

---

## Sample AI Agent Execution

### Input Command
```
show running containers
```

### ReAct Step-by-Step Output

```json
{
  "steps": [
    {"step": 1, "name": "User Request",       "status": "completed"},
    {"step": 2, "name": "AI Analysis",        "status": "completed"},
    {"step": 3, "name": "Tool Selection",     "status": "completed"},
    {"step": 4, "name": "Tool Execution",     "status": "completed"},
    {"step": 5, "name": "Result Collection",  "status": "completed"},
    {"step": 6, "name": "Summary Generation", "status": "completed"},
    {"step": 7, "name": "Response Return",    "status": "completed"}
  ],
  "summary": "Found 3 container(s). 3 running normally. Resource usage is within normal range."
}
```

### LLM-Translated JSON Action
```json
{
  "action": "list_containers",
  "status": "running"
}
```

---

## Sample Database Records

### `prompt_logs` Table

| id | timestamp | user_prompt | generated_action | execution_result | execution_time_ms |
|----|-----------|-------------|-----------------|------------------|-------------------|
| 1 | 2026-06-08T10:00:00 | show running containers | `{"action":"list_containers","status":"running"}` | Found 3 containers | 1200 |
| 2 | 2026-06-08T10:05:00 | restart nginx-test | `{"action":"restart_container","name":"nginx-test"}` | Container restarted | 850 |
| 3 | 2026-06-08T10:10:00 | get resource usage for mysql-test | `{"action":"get_container_resource_usage","name":"mysql-test"}` | CPU: 2.3%, Mem: 380MB | 980 |

---

### `container_history` Table

| id | timestamp | container_id | container_name | status | cpu_usage | memory_usage |
|----|-----------|-------------|----------------|--------|-----------|--------------|
| 1 | 2026-06-08T10:00:00 | abc123 | nginx-test | running | 0.5 | 50.2 |
| 2 | 2026-06-08T10:00:00 | def456 | redis-test | running | 0.2 | 15.8 |
| 3 | 2026-06-08T10:00:00 | ghi789 | mysql-test | running | 2.3 | 380.5 |

---

### `audit_logs` Table

| id | timestamp | action | status | details |
|----|-----------|--------|--------|---------|
| 1 | 2026-06-08T10:05:00 | restart_container | success | nginx-test restarted |
| 2 | 2026-06-08T10:10:00 | get_container_resource_usage | success | mysql-test stats collected |

---

## Sample `prompt_log.txt` Entry

```
=====================================
Timestamp: 2026-06-08T10:00:00
Prompt: show running containers
Action: {"action": "list_containers", "status": "running"}
Result: Found 3 container(s). 3 running normally.
Time:   1200ms
=====================================
```

---

## Sample GitHub API Data

```json
{
  "github_status": "All Systems Operational",
  "recent_events": [
    {"type": "PushEvent", "actor": "user123", "repo": "user123/project"},
    {"type": "PullRequestEvent", "actor": "dev456", "repo": "org/repo"}
  ],
  "rate_limit": {
    "limit": 60,
    "remaining": 58,
    "reset": "2026-06-08T11:00:00"
  }
}
```

---

## Performance Benchmarks

| Operation | Typical Time |
|-----------|-------------|
| LLM Translation (Ollama) | 500–1500 ms |
| Docker Operations | 100–500 ms |
| Database Queries | < 50 ms |
| Total Request | 1–3 seconds |

---

## Resource Usage

| Component | RAM |
|-----------|-----|
| Dashboard Application | ~150 MB |
| Ollama (llama3 model) | ~4–8 GB |
| Total Disk Space | ~5.2 GB |
