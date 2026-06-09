# Installation Guide - AI Docker NL Dashboard

## Prerequisites

Before installing, ensure you have:

1. **Docker** - Running and accessible
2. **Python 3.11+** - For running the application
3. **Ollama** - For AI/LLM capabilities
4. **4GB+ RAM** - Recommended for smooth operation

---

## Installation Methods

### Method 1: Docker Compose (Easiest)

This method runs everything in containers including Ollama.

```bash
# 1. Navigate to project directory
cd docker-nl-dashboard

# 2. Start all services
docker-compose up -d

# 3. Wait for services to start (30-60 seconds)
docker-compose logs -f

# 4. Pull llama3 model (first time only, ~4GB download)
docker exec -it ollama-service ollama pull llama3

# 5. Access dashboard
# Open browser: http://localhost:8501
```

**Verify Installation:**
```bash
# Check services are running
docker-compose ps

# Should show:
# - ollama-service (healthy)
# - docker-nl-dashboard (healthy)
```

---

### Method 2: Local Python Installation

This method runs the dashboard locally with system Python.

#### Step 1: Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
- Download from https://ollama.ai/download
- Run the installer

#### Step 2: Start Ollama and Pull Model

```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull llama3

# Verify
curl http://localhost:11434/api/tags
```

#### Step 3: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Run the Dashboard

```bash
# Linux/Mac:
chmod +x start.sh
./start.sh

# Windows:
start.bat

# Or directly:
streamlit run app.py
```

#### Step 5: Access Dashboard

Open browser: http://localhost:8501

---

### Method 3: Standalone Docker

Run just the dashboard in Docker, with Ollama on host.

```bash
# 1. Ensure Ollama is running on host
ollama serve
ollama pull llama3

# 2. Build dashboard image
docker build -t docker-nl-dashboard .

# 3. Run dashboard container
docker run -d \
  --name dashboard \
  --network host \
  -p 8501:8501 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e OLLAMA_HOST=http://localhost:11434 \
  docker-nl-dashboard

# 4. Access dashboard
# Open browser: http://localhost:8501
```

---

## Post-Installation

### 1. Create Test Containers

```bash
docker run -d --name nginx-test nginx
docker run -d --name redis-test redis
docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=test mysql
```

### 2. Test the Dashboard

1. Open http://localhost:8501
2. Navigate to "AI Agent" page
3. Enter command: "show running containers"
4. Verify you see the test containers

### 3. Run Demo Script

```bash
python test_demo.py
```

---

## Verification Checklist

✅ Docker is running: `docker info`  
✅ Ollama is running: `curl http://localhost:11434/api/tags`  
✅ llama3 model available: `ollama list | grep llama3`  
✅ Dashboard accessible: Open http://localhost:8501  
✅ Can list containers: Try "show running containers" in AI Agent  

---

## Troubleshooting

### Dashboard won't start

**Error:** `Cannot connect to Docker daemon`

**Solution:**
```bash
# Verify Docker is running
docker info

# Check Docker socket permissions (Linux)
sudo chmod 666 /var/run/docker.sock

# Or add user to docker group
sudo usermod -aG docker $USER
# Then logout and login
```

---

### Ollama connection failed

**Error:** `Failed to connect to Ollama`

**Solution:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# Verify model is downloaded
ollama list
ollama pull llama3
```

---

### Port 8501 already in use

**Solution:**
```bash
# Find and kill process using port
# Linux/Mac:
lsof -ti:8501 | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or use different port
streamlit run app.py --server.port 8502
```

---

### Slow AI responses

**Causes:**
- First run downloads model (~4GB)
- Low RAM (need 4GB+)
- CPU-only inference (GPU recommended)

**Solution:**
```bash
# Check system resources
docker stats

# Use smaller model if needed
ollama pull llama3:8b  # smaller variant
```

---

### Permission denied on Docker socket

**Linux Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker

# Or temporary fix
sudo chmod 666 /var/run/docker.sock
```

---

## Uninstallation

### Docker Compose Installation

```bash
# Stop and remove services
docker-compose down -v

# Remove images
docker rmi ollama/ollama:latest
docker rmi docker-nl-dashboard_dashboard

# Remove project directory
cd ..
rm -rf docker-nl-dashboard
```

### Local Installation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf docker-nl-dashboard

# Uninstall Ollama (optional)
# Linux:
sudo rm $(which ollama)
sudo rm -rf /usr/share/ollama

# macOS:
brew uninstall ollama
```

---

## System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB (5GB for llama3 model)
- OS: Linux, macOS, Windows 10+

### Recommended
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 20GB SSD
- GPU: Optional (faster inference)

---

## Next Steps

After successful installation:

1. **Read the README**: Full feature documentation
2. **Explore Pages**: Navigate through all 7 dashboard pages
3. **Try Commands**: Test various natural language commands
4. **View Logs**: Check execution logs and audit trail
5. **Customize**: Modify settings in Settings page

---

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: README.md for full usage guide
- **Ollama Docs**: https://ollama.ai/docs
- **Streamlit Docs**: https://docs.streamlit.io

---

**Installation Complete!** 🎉

Access your dashboard at: **http://localhost:8501**
