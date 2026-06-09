# Quick Start Guide - 5 Minutes Setup

## 🚀 Fastest Way to Run

### Using Docker Compose (Recommended)

```bash
# 1. Start everything
docker-compose up -d

# 2. Pull AI model (first time only, ~4GB)
docker exec -it ollama-service ollama pull llama3

# 3. Open browser
http://localhost:8501
```

**Done! 🎉**

---

## 🧪 Quick Test

### Create Test Containers

```bash
docker run -d --name nginx-test nginx
docker run -d --name redis-test redis
docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=test mysql
```

### Try These Commands in AI Agent Page

1. `show running containers`
2. `restart nginx-test`
3. `get resource usage for mysql-test`
4. `show nginx-test logs`

---

## 📋 Quick Reference

### Natural Language Commands

| Command | Action |
|---------|--------|
| `show running containers` | List all running containers |
| `list all containers` | Show all containers (any status) |
| `show stopped containers` | List stopped containers |
| `restart nginx` | Restart nginx container |
| `start redis` | Start redis container |
| `stop mysql` | Stop mysql container |
| `check nginx health` | Get health status |
| `show nginx logs` | View container logs |
| `what crashed` | List exited containers |
| `get resource usage for nginx` | CPU/memory stats |

---

## 🎯 Key Features

### Dashboard Page
- Total, running, stopped, restarting, unhealthy counts
- System information

### Containers Page
- Table view of all containers
- Start/Stop/Restart buttons
- Filter by status

### AI Agent Page
- Natural language input
- Step-by-step execution display (ReAct loop)
- 7-step reasoning process visible

### Logs Page
- Prompt execution logs
- Audit trail
- Container history

### Analytics Page
- Bar chart: Container count by status
- Pie chart: Status distribution
- CPU usage graph
- Memory usage graph
- Timeline of container status changes

### GitHub API Page
- GitHub status monitoring
- Recent public events
- API rate limit info

### Settings Page
- Docker configuration
- Ollama model settings
- Database options

---

## 🔧 Common Tasks

### View All Containers
```
Dashboard → Containers → Select "all"
```

### Execute Natural Language Command
```
Dashboard → AI Agent → Type command → Execute
```

### View Logs
```
Dashboard → Logs → Select tab (Prompt/Audit/History)
```

### Check Resource Usage
```
Dashboard → Analytics → View charts
```

### Monitor GitHub
```
Dashboard → GitHub API → Refresh Status/Events
```

---

## 🛑 Stop & Cleanup

### Stop Dashboard
```bash
# If using Docker Compose
docker-compose down

# If using local Python
Ctrl+C in terminal
```

### Remove Test Containers
```bash
docker rm -f nginx-test redis-test mysql-test
```

### Complete Cleanup
```bash
docker-compose down -v
docker rmi ollama/ollama:latest
docker rmi docker-nl-dashboard_dashboard
```

---

## ⚡ Troubleshooting Quick Fixes

### Dashboard won't load
```bash
# Check Docker
docker info

# Check Ollama
curl http://localhost:11434/api/tags

# Restart services
docker-compose restart
```

### Slow responses
```bash
# Check if model is downloaded
ollama list

# Download if missing
ollama pull llama3
```

### Port conflict
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## 📊 Expected Results

After running test commands, you should see:

**Dashboard KPIs:**
- Total: 3
- Running: 3
- Stopped: 0
- Restarting: 0
- Unhealthy: 0

**Containers Table:**
```
nginx-test  | running | nginx | 0.5% | 50MB
redis-test  | running | redis | 0.2% | 15MB
mysql-test  | running | mysql | 2.3% | 380MB
```

**AI Agent Response:**
```
✅ Found 3 container(s). 
   3 running normally. 
   Resource usage is within normal range.
```

---

## 🎓 Next Steps

1. ✅ Dashboard running
2. ✅ Test containers created
3. ✅ Tried natural language commands
4. 📖 Read full README.md
5. 🔍 Explore all 7 pages
6. ⚙️ Customize settings
7. 📊 Monitor your real containers

---

## 📚 More Documentation

- **README.md** - Complete feature documentation
- **INSTALL.md** - Detailed installation guide
- **Logs** - Check `logs/prompt_log.txt` for execution history

---

**You're all set!** Start managing Docker with natural language! 🚀
