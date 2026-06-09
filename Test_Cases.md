# Test Cases

## Project: AI Docker Natural Language Health Dashboard

---

## Prerequisites

Before running tests, ensure:
- Docker is running: `docker info`
- Ollama is serving: `curl http://localhost:11434/api/tags`
- Dashboard is accessible: `http://localhost:8501`

Create the test containers:
```bash
docker run -d --name nginx-test nginx
docker run -d --name redis-test redis
docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=test mysql
docker ps  # verify all three are running
```

---

## Automated Test Script

Run the provided demo script for automated testing:

```bash
python test_demo.py
```

---

## Manual Test Cases

### TC-01: List Running Containers

**Input:** `show running containers`
**Expected Action:** `{"action": "list_containers", "status": "running"}`
**Expected Output:**
```
Found 3 container(s). 3 running normally.
```
**Expected UI:** Container table shows nginx-test, redis-test, mysql-test with `running` status.

---

### TC-02: List All Containers

**Input:** `list all containers`
**Expected Action:** `{"action": "list_containers", "status": "all"}`
**Expected Output:** All containers listed regardless of status.

---

### TC-03: Restart a Container

**Input:** `restart nginx-test`
**Expected Action:** `{"action": "restart_container", "name": "nginx-test"}`
**Expected Output:** `nginx-test restarted successfully.`
**Verify:** `docker ps` — nginx-test shows a recent start time.

---

### TC-04: Stop a Container

**Input:** `stop redis-test`
**Expected Action:** `{"action": "stop_container", "name": "redis-test"}`
**Expected Output:** `redis-test stopped successfully.`
**Verify:** Dashboard KPIs update to Running: 2, Stopped: 1.

---

### TC-05: Start a Stopped Container

**Input:** `start redis-test`
**Expected Action:** `{"action": "start_container", "name": "redis-test"}`
**Expected Output:** `redis-test started successfully.`

---

### TC-06: Check Container Health

**Input:** `check nginx health`
**Expected Action:** `{"action": "get_container_health", "name": "nginx-test"}`
**Expected Output:** Health status and state of nginx-test container.

---

### TC-07: View Container Logs

**Input:** `show nginx-test logs`
**Expected Action:** `{"action": "get_container_logs", "name": "nginx-test"}`
**Expected Output:** Last N lines of nginx-test container logs.

---

### TC-08: Resource Usage

**Input:** `get resource usage for mysql-test`
**Expected Action:** `{"action": "get_container_resource_usage", "name": "mysql-test"}`
**Expected Output:** CPU % and Memory MB for mysql-test.
**Sample Result:**
```
mysql-test — CPU: 2.3% | Memory: 380.5 MB
```

---

### TC-09: Find Crashed Containers

**Input:** `what crashed in the last hour?`
**Expected Action:** `{"action": "list_containers", "status": "exited"}`
**Expected Output:** List of exited containers, or "No crashed containers found."

---

### TC-10: Show Restarting Containers

**Input:** `show restarting containers`
**Expected Action:** `{"action": "list_containers", "status": "restarting"}`
**Expected Output:** Containers in restarting state, or "No restarting containers found."

---

## UI Page Tests

### Dashboard Page
- [ ] KPI cards load (Total, Running, Stopped, Restarting, Unhealthy)
- [ ] Counts match actual Docker state
- [ ] Quick action buttons are visible

### Containers Page
- [ ] Table shows all containers with correct columns (Name, Status, Image, CPU%, Memory)
- [ ] Status filter works
- [ ] Start / Stop / Restart buttons are clickable

### AI Agent Page
- [ ] Text input box is present
- [ ] Submitting a command triggers the 7-step ReAct loop
- [ ] Each step shows status indicator (✅ / ❌ / ⏳)
- [ ] Summary is displayed after completion
- [ ] Example commands are listed

### Logs Page
- [ ] Prompt Logs tab shows recent entries
- [ ] Audit Logs tab shows action history
- [ ] Container History tab shows snapshots
- [ ] Entries are expandable

### Analytics Page
- [ ] Bar chart renders (container count by status)
- [ ] Pie chart renders (status distribution)
- [ ] CPU graph renders
- [ ] Memory graph renders
- [ ] Timeline renders

### GitHub API Page
- [ ] GitHub status is displayed
- [ ] Public events list loads
- [ ] Rate limit info is shown
- [ ] Refresh button works

### Settings Page
- [ ] Docker connection can be tested
- [ ] Ollama host and model fields are editable
- [ ] Database path is configurable

---

## Database Verification

After running test commands, verify records exist:

```python
import sqlite3
conn = sqlite3.connect("data/dashboard.db")
cur = conn.cursor()

# Check prompt_logs
cur.execute("SELECT COUNT(*) FROM prompt_logs")
print("Prompt logs:", cur.fetchone()[0])

# Check audit_logs
cur.execute("SELECT COUNT(*) FROM audit_logs")
print("Audit logs:", cur.fetchone()[0])

# Check container_history
cur.execute("SELECT COUNT(*) FROM container_history")
print("Container history:", cur.fetchone()[0])

conn.close()
```

Expected: All counts > 0 after running test cases.

---

## Docker Connection Tests

```bash
# Verify Docker is accessible
docker info

# Check socket permissions (Linux)
ls -la /var/run/docker.sock

# Test from inside Docker container
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker docker ps
```

---

## Ollama Connection Tests

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Verify llama3 model is available
ollama list

# Quick translation test
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"llama3","prompt":"Translate to JSON: show running containers"}'
```

---

## Cleanup After Testing

```bash
# Stop and remove test containers
docker stop nginx-test redis-test mysql-test
docker rm nginx-test redis-test mysql-test

# Verify cleanup
docker ps -a | grep -E "nginx-test|redis-test|mysql-test"
```

---

## Known Limitations

| Limitation | Notes |
|------------|-------|
| No authentication | Add a reverse proxy with auth for production |
| No container creation/deletion via NL | Scope limited to management operations |
| Single Docker host | Multi-host support not included in v1.0 |
| Ollama required locally | No fallback LLM |
