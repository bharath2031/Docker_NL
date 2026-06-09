import json
import re
import os
from typing import Dict, Optional
from pathlib import Path

class LLMManager:
    def __init__(self, model: str = "llama-3.3-70b-versatile", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.system_prompt = self._load_system_prompt()
        
        # Try to import groq, fallback if not available
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None
            print("Warning: groq package not installed. Install with: pip install groq")
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        prompt_path = Path("prompts/system_prompt.txt")
        if prompt_path.exists():
            return prompt_path.read_text()
        return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default system prompt for Docker NL commands"""
        return """You are a Docker command translator. Your task is to convert natural language requests into structured JSON actions.

Available actions and their formats:

1. List containers:
{"action": "list_containers", "status": "running|stopped|restarting|all"}

2. Restart container:
{"action": "restart_container", "container": "container_name"}

3. Start container:
{"action": "start_container", "container": "container_name"}

4. Stop container:
{"action": "stop_container", "container": "container_name"}

5. Get container health:
{"action": "get_container_health", "container": "container_name"}

6. Get container logs:
{"action": "get_container_logs", "container": "container_name", "tail": 100}

7. Get container resource usage:
{"action": "get_container_resource_usage", "container": "container_name"}

Examples:
- "show running containers" → {"action": "list_containers", "status": "running"}
- "list all containers" → {"action": "list_containers", "status": "all"}
- "show restarting containers" → {"action": "list_containers", "status": "restarting"}
- "restart nginx" → {"action": "restart_container", "container": "nginx"}
- "start mysql" → {"action": "start_container", "container": "mysql"}
- "stop redis" → {"action": "stop_container", "container": "redis"}
- "check nginx health" → {"action": "get_container_health", "container": "nginx"}
- "show nginx logs" → {"action": "get_container_logs", "container": "nginx", "tail": 100}
- "what crashed in the last hour" → {"action": "list_containers", "status": "exited"}
- "get resource usage for nginx" → {"action": "get_container_resource_usage", "container": "nginx"}

Always respond with ONLY valid JSON. No explanations, no markdown, just the JSON object."""
    
    def translate_to_action(self, user_prompt: str) -> Dict:
        """Translate natural language to structured action"""
        if not self.client or not self.api_key:
            return {
                "action": "error",
                "message": "Groq API key not configured. Please set GROQ_API_KEY environment variable or enter it in Settings page."
            }
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            action = json.loads(content)
            return action
        except json.JSONDecodeError as e:
            return {
                "action": "error",
                "message": f"Failed to parse LLM response: {str(e)}",
                "raw_response": content if 'content' in locals() else ""
            }
        except Exception as e:
            return {
                "action": "error",
                "message": f"Groq API error: {str(e)}"
            }
    
    def generate_summary(self, action: Dict, result: any) -> str:
        """Generate human-readable summary of action result"""
        try:
            action_type = action.get("action", "unknown")
            
            if action_type == "list_containers":
                return self._summarize_list_containers(result, action)
            elif action_type in ["restart_container", "start_container", "stop_container"]:
                return self._summarize_container_action(result, action_type)
            elif action_type == "get_container_health":
                return self._summarize_health(result)
            elif action_type == "get_container_logs":
                return self._summarize_logs(result)
            elif action_type == "get_container_resource_usage":
                return self._summarize_resources(result)
            else:
                return f"Action '{action_type}' completed. Result: {str(result)}"
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def _summarize_list_containers(self, containers: list, action: Dict) -> str:
        """Summarize container list"""
        if not containers:
            status = action.get("status", "all")
            return f"No {status} containers found."
        
        total = len(containers)
        running = sum(1 for c in containers if c.get("status") == "running")
        stopped = sum(1 for c in containers if c.get("status") in ["exited", "stopped"])
        restarting = sum(1 for c in containers if c.get("status") == "restarting")
        
        summary = f"Found {total} container(s). "
        
        if running > 0:
            summary += f"{running} running normally. "
        if stopped > 0:
            summary += f"{stopped} stopped. "
        if restarting > 0:
            summary += f"{restarting} restarting (may indicate issues). "
        
        # Check for unhealthy containers
        unhealthy = [c for c in containers if c.get("status") == "running" 
                    and c.get("cpu_usage", 0) > 90]
        
        if unhealthy:
            summary += f"{len(unhealthy)} container(s) show high CPU usage and may require attention."
        
        return summary.strip()
    
    def _summarize_container_action(self, result: Dict, action_type: str) -> str:
        """Summarize container action (start/stop/restart)"""
        if result.get("success"):
            container = result.get("container", "unknown")
            status = result.get("status", "unknown")
            action_name = action_type.replace("_", " ").replace("container", "").strip()
            return f"Successfully {action_name}ed container '{container}'. Current status: {status}."
        else:
            return f"Failed: {result.get('message', 'Unknown error')}"
    
    def _summarize_health(self, result: Dict) -> str:
        """Summarize health check"""
        if "error" in result:
            return f"Health check failed: {result['error']}"
        
        container = result.get("container", "unknown")
        health = result.get("health", "none")
        status = result.get("status", "unknown")
        
        if health == "healthy":
            return f"Container '{container}' is healthy and running normally."
        elif health == "unhealthy":
            failing = result.get("failing_streak", 0)
            return f"Container '{container}' is unhealthy (failed {failing} consecutive health checks). Immediate attention required."
        elif health == "none":
            return f"Container '{container}' has no health check configured. Status: {status}."
        else:
            return f"Container '{container}' health: {health}. Status: {status}."
    
    def _summarize_logs(self, result: Dict) -> str:
        """Summarize logs"""
        if "error" in result:
            return f"Failed to retrieve logs: {result['error']}"
        
        container = result.get("container", "unknown")
        lines = result.get("lines", 0)
        logs = result.get("logs", "")
        
        # Check for common error patterns
        error_keywords = ["error", "failed", "exception", "fatal", "critical"]
        errors_found = sum(1 for keyword in error_keywords if keyword.lower() in logs.lower())
        
        summary = f"Retrieved {lines} log lines from '{container}'. "
        
        if errors_found > 0:
            summary += f"Found {errors_found} potential error messages. Review recommended."
        else:
            summary += "No obvious errors detected."
        
        return summary
    
    def _summarize_resources(self, result: Dict) -> str:
        """Summarize resource usage"""
        if "error" in result:
            return f"Failed to get resource usage: {result['error']}"
        
        container = result.get("container", "unknown")
        cpu = result.get("cpu_percent", 0)
        memory_mb = result.get("memory_mb", 0)
        memory_percent = result.get("memory_percent", 0)
        
        summary = f"Container '{container}' resource usage: CPU {cpu:.1f}%, Memory {memory_mb:.1f}MB ({memory_percent:.1f}%). "
        
        if cpu > 80:
            summary += "CPU usage is high. "
        if memory_percent > 80:
            summary += "Memory usage is high. "
        
        if cpu <= 80 and memory_percent <= 80:
            summary += "Resource usage is within normal range."
        
        return summary
    
    def test_connection(self) -> Dict:
        """Test Groq connection"""
        if not self.client or not self.api_key:
            return {
                "success": False,
                "error": "API key not configured",
                "message": "Groq API key not set. Please configure it in Settings or set GROQ_API_KEY environment variable."
            }
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                temperature=0,
                max_tokens=10
            )
            return {
                "success": True,
                "model": self.model,
                "message": "Groq API connection successful"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to connect to Groq API"
            }
