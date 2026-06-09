import time
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path
import json

from llm import LLMManager
from docker_manager import DockerManager
from database import Database

class AgentStep:
    def __init__(self, step_number: int, name: str, description: str):
        self.step_number = step_number
        self.name = name
        self.description = description
        self.status = "pending"
        self.result = None
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.status = "running"
        self.start_time = time.time()
    
    def complete(self, result):
        self.status = "completed"
        self.result = result
        self.end_time = time.time()
    
    def fail(self, error):
        self.status = "failed"
        self.result = {"error": error}
        self.end_time = time.time()
    
    def get_duration_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

class ReactAgent:
    """
    ReAct-style agent for Docker NL commands
    Steps: Request → Analyze → Select Tool → Execute → Collect → Summarize → Return
    """
    
    def __init__(self):
        self.llm = LLMManager()
        self.docker = DockerManager()
        self.db = Database()
        self.steps: List[AgentStep] = []
        self.log_file = Path("logs/prompt_log.txt")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def execute(self, user_request: str) -> Tuple[List[AgentStep], Dict]:
        """
        Execute the full ReAct loop
        Returns: (steps, final_result)
        """
        self.steps = []
        start_time = time.time()
        
        # Step 1: User Request
        step1 = AgentStep(1, "User Request", "Accept and parse user input")
        step1.start()
        self.steps.append(step1)
        step1.complete({"request": user_request})
        
        # Step 2: AI Analysis
        step2 = AgentStep(2, "AI Analysis", "Analyze intent using Ollama LLM")
        step2.start()
        self.steps.append(step2)
        
        try:
            action = self.llm.translate_to_action(user_request)
            step2.complete(action)
        except Exception as e:
            step2.fail(str(e))
            return self.steps, {"error": "AI analysis failed", "details": str(e)}
        
        # Check for error in action
        if action.get("action") == "error":
            return self.steps, action
        
        # Step 3: Tool Selection
        step3 = AgentStep(3, "Tool Selection", "Determine which Docker operation to execute")
        step3.start()
        self.steps.append(step3)
        tool_name = action.get("action", "unknown")
        step3.complete({"tool": tool_name, "parameters": action})
        
        # Step 4: Tool Execution
        step4 = AgentStep(4, "Tool Execution", f"Execute Docker operation: {tool_name}")
        step4.start()
        self.steps.append(step4)
        
        try:
            result = self._execute_tool(action)
            step4.complete(result)
        except Exception as e:
            step4.fail(str(e))
            return self.steps, {"error": "Tool execution failed", "details": str(e)}
        
        # Step 5: Result Collection
        step5 = AgentStep(5, "Result Collection", "Gather and structure execution output")
        step5.start()
        self.steps.append(step5)
        
        collected_data = {
            "action": action,
            "result": result,
            "execution_time_ms": step4.get_duration_ms()
        }
        step5.complete(collected_data)
        
        # Step 6: Summary Generation
        step6 = AgentStep(6, "Summary Generation", "Create human-readable response")
        step6.start()
        self.steps.append(step6)
        
        try:
            summary = self.llm.generate_summary(action, result)
            step6.complete({"summary": summary})
        except Exception as e:
            summary = f"Operation completed but summary generation failed: {str(e)}"
            step6.complete({"summary": summary})
        
        # Step 7: Response Return
        step7 = AgentStep(7, "Response Return", "Deliver final result to user")
        step7.start()
        self.steps.append(step7)
        
        final_result = {
            "summary": summary,
            "action": action,
            "result": result,
            "success": True
        }
        step7.complete(final_result)
        
        # Log everything
        total_time = (time.time() - start_time) * 1000
        self._log_execution(user_request, action, result, summary, total_time)
        
        return self.steps, final_result
    
    def _execute_tool(self, action: Dict) -> any:
        """Execute the selected Docker tool"""
        action_type = action.get("action")
        
        if action_type == "list_containers":
            status = action.get("status", "all")
            status = None if status == "all" else status
            containers = self.docker.list_containers(status_filter=status)
            
            # Log to container history
            for container in containers:
                self.db.log_container_history(
                    container_id=container.get("id", ""),
                    container_name=container.get("name", ""),
                    status=container.get("status", ""),
                    cpu_usage=container.get("cpu_usage", 0.0),
                    memory_usage=container.get("memory_usage", 0.0)
                )
            
            return containers
        
        elif action_type == "restart_container":
            container_name = action.get("container")
            result = self.docker.restart_container(container_name)
            self.db.log_audit("restart_container", 
                            "success" if result.get("success") else "failed",
                            json.dumps(result))
            return result
        
        elif action_type == "start_container":
            container_name = action.get("container")
            result = self.docker.start_container(container_name)
            self.db.log_audit("start_container",
                            "success" if result.get("success") else "failed",
                            json.dumps(result))
            return result
        
        elif action_type == "stop_container":
            container_name = action.get("container")
            result = self.docker.stop_container(container_name)
            self.db.log_audit("stop_container",
                            "success" if result.get("success") else "failed",
                            json.dumps(result))
            return result
        
        elif action_type == "get_container_health":
            container_name = action.get("container")
            return self.docker.get_container_health(container_name)
        
        elif action_type == "get_container_logs":
            container_name = action.get("container")
            tail = action.get("tail", 100)
            return self.docker.get_container_logs(container_name, tail)
        
        elif action_type == "get_container_resource_usage":
            container_name = action.get("container")
            return self.docker.get_container_resource_usage(container_name)
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    def _log_execution(self, user_prompt: str, action: Dict, result: any, 
                      summary: str, execution_time_ms: float):
        """Log execution to database and file"""
        # Log to database
        self.db.log_prompt(
            user_prompt=user_prompt,
            generated_action=json.dumps(action),
            execution_result=summary,
            execution_time_ms=execution_time_ms
        )
        
        # Log to file
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"""
{'='*80}
Timestamp: {timestamp}
User Prompt: {user_prompt}
Generated Action: {json.dumps(action, indent=2)}
Execution Result: {summary}
Execution Time: {execution_time_ms:.2f}ms
{'='*80}

"""
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def get_steps(self) -> List[AgentStep]:
        """Get the current execution steps"""
        return self.steps
