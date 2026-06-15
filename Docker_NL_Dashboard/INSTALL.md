# Installation Guide - AI Docker NL Dashboard

## Prerequisites

Before installing, ensure you have:

1. **Docker** - Running and accessible
2. **Python 3.11+** - For running the application
3. **Groq API Key** - For AI/LLM capabilities

---

## Installation Methods

### Method 1: Docker Compose (Easiest)

This method runs the dashboard container.

```bash
# 1. Navigate to project directory
cd docker-nl-dashboard

# 2. Configure GROQ_API_KEY in Docker_NL_Dashboard/.env
# Update the GROQ_API_KEY with your active key from console.groq.com

# 3. Start all services
docker-compose up -d

# 4. Access dashboard
# Open browser: http://localhost:8501
```

**Verify Installation:**
```bash
# Check services are running
docker-compose ps

# Should show:
# - docker-nl-dashboard (healthy)
```

---

### Method 2: Local Python Installation

This method runs the dashboard locally with system Python.

#### Step 1: Configure Groq API Key

Ensure your `GROQ_API_KEY` is configured in `Docker_NL_Dashboard/.env` or exported to your environment. You can obtain a free key from console.groq.com.

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

Run the dashboard in Docker using the Groq API key from environment.

```bash
# 1. Build dashboard image
docker build -t docker-nl-dashboard .

# 2. Run dashboard container (passing Groq API key)
docker run -d \
  --name dashboard \
  -p 8501:8501 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e GROQ_API_KEY=your_groq_api_key_here \
  docker-nl-dashboard

# 3. Access dashboard
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
✅ Groq API Key is configured in settings or environment  
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

### Groq API connection failed

**Error:** `Groq API connection failed`

**Solution:**
- Verify your API key is correct.
- Ensure you have network access to api.groq.com.

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

**Solution:**
- Ensure network latency to Groq is normal. Groq is cloud-hosted and provides very fast responses.

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
```

---

## System Requirements

### Minimum
- CPU: 2 cores
- RAM: 2GB
- Disk: 1GB
- OS: Linux, macOS, Windows 10+

### Recommended
- CPU: 4+ cores
- RAM: 4GB+
- Disk: 5GB SSD

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
- **Groq Docs**: https://console.groq.com/docs
- **Streamlit Docs**: https://docs.streamlit.io

---

**Installation Complete!** 🎉

Access your dashboard at: **http://localhost:8501**
