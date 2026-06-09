import docker
from docker.errors import DockerException, NotFound, APIError
from typing import List, Dict, Optional
import time

class DockerManager:
    def __init__(self):
        try:
            # Try to connect using default method first
            self.client = docker.from_env()
            self.client.ping()
        except DockerException:
            # If that fails, try Windows named pipe
            try:
                self.client = docker.DockerClient(base_url='npipe:////./pipe/docker_engine')
                self.client.ping()
            except DockerException as e:
                raise Exception(f"Failed to connect to Docker daemon: {str(e)}")
    
    def list_containers(self, status_filter: Optional[str] = None) -> List[Dict]:
        """
        List containers with optional status filtering
        Status options: running, stopped, restarting, paused, exited, dead
        """
        try:
            all_containers = status_filter is None
            containers = self.client.containers.list(all=all_containers)
            
            if not all_containers and status_filter:
                containers = [c for c in self.client.containers.list(all=True) 
                             if c.status.lower() == status_filter.lower()]
            
            result = []
            for container in containers:
                try:
                    container.reload()
                    stats = self._get_container_stats_safe(container)
                    
                    result.append({
                        "id": container.short_id,
                        "name": container.name,
                        "status": container.status,
                        "image": container.image.tags[0] if container.image.tags else "unknown",
                        "created": container.attrs.get("Created", ""),
                        "ports": container.ports,
                        "cpu_usage": stats.get("cpu_percent", 0.0),
                        "memory_usage": stats.get("memory_mb", 0.0),
                        "memory_limit": stats.get("memory_limit_mb", 0.0)
                    })
                except Exception as e:
                    result.append({
                        "id": container.short_id,
                        "name": container.name,
                        "status": container.status,
                        "image": "unknown",
                        "created": "",
                        "ports": {},
                        "cpu_usage": 0.0,
                        "memory_usage": 0.0,
                        "memory_limit": 0.0,
                        "error": str(e)
                    })
            
            return result
        except DockerException as e:
            raise Exception(f"Failed to list containers: {str(e)}")
    
    def get_container_by_name(self, name: str):
        """Get container by name or ID"""
        try:
            return self.client.containers.get(name)
        except NotFound:
            raise Exception(f"Container '{name}' not found")
        except DockerException as e:
            raise Exception(f"Failed to get container: {str(e)}")
    
    def restart_container(self, container_name: str) -> Dict:
        """Restart a container by name or ID"""
        try:
            container = self.get_container_by_name(container_name)
            container.restart(timeout=10)
            time.sleep(1)
            container.reload()
            
            return {
                "success": True,
                "container": container.name,
                "status": container.status,
                "message": f"Container '{container.name}' restarted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "container": container_name,
                "message": f"Failed to restart container: {str(e)}"
            }
    
    def start_container(self, container_name: str) -> Dict:
        """Start a stopped container"""
        try:
            container = self.get_container_by_name(container_name)
            container.start()
            time.sleep(1)
            container.reload()
            
            return {
                "success": True,
                "container": container.name,
                "status": container.status,
                "message": f"Container '{container.name}' started successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "container": container_name,
                "message": f"Failed to start container: {str(e)}"
            }
    
    def stop_container(self, container_name: str) -> Dict:
        """Stop a running container"""
        try:
            container = self.get_container_by_name(container_name)
            container.stop(timeout=10)
            time.sleep(1)
            container.reload()
            
            return {
                "success": True,
                "container": container.name,
                "status": container.status,
                "message": f"Container '{container.name}' stopped successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "container": container_name,
                "message": f"Failed to stop container: {str(e)}"
            }
    
    def get_container_health(self, container_name: str) -> Dict:
        """Get health status of a container"""
        try:
            container = self.get_container_by_name(container_name)
            container.reload()
            
            health_status = container.attrs.get("State", {}).get("Health", {})
            
            return {
                "container": container.name,
                "status": container.status,
                "health": health_status.get("Status", "none"),
                "failing_streak": health_status.get("FailingStreak", 0),
                "log": health_status.get("Log", [])
            }
        except Exception as e:
            return {
                "container": container_name,
                "error": str(e)
            }
    
    def get_container_logs(self, container_name: str, tail: int = 100) -> Dict:
        """Get logs from a container"""
        try:
            container = self.get_container_by_name(container_name)
            logs = container.logs(tail=tail, timestamps=True).decode('utf-8', errors='ignore')
            
            return {
                "container": container.name,
                "logs": logs,
                "lines": len(logs.split('\n'))
            }
        except Exception as e:
            return {
                "container": container_name,
                "error": str(e),
                "logs": ""
            }
    
    def get_container_resource_usage(self, container_name: str) -> Dict:
        """Get CPU and memory usage for a container"""
        try:
            container = self.get_container_by_name(container_name)
            container.reload()
            
            if container.status != "running":
                return {
                    "container": container.name,
                    "status": container.status,
                    "cpu_percent": 0.0,
                    "memory_mb": 0.0,
                    "memory_limit_mb": 0.0,
                    "memory_percent": 0.0,
                    "message": "Container is not running"
                }
            
            stats = self._get_container_stats_safe(container)
            
            return {
                "container": container.name,
                "status": container.status,
                "cpu_percent": stats.get("cpu_percent", 0.0),
                "memory_mb": stats.get("memory_mb", 0.0),
                "memory_limit_mb": stats.get("memory_limit_mb", 0.0),
                "memory_percent": stats.get("memory_percent", 0.0)
            }
        except Exception as e:
            return {
                "container": container_name,
                "error": str(e)
            }
    
    def _get_container_stats_safe(self, container) -> Dict:
        """Safely get container stats with timeout"""
        try:
            if container.status != "running":
                return {
                    "cpu_percent": 0.0,
                    "memory_mb": 0.0,
                    "memory_limit_mb": 0.0,
                    "memory_percent": 0.0
                }
            
            stats = container.stats(stream=False)
            
            # Calculate CPU percentage
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                       stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                          stats["precpu_stats"]["system_cpu_usage"]
            cpu_count = stats["cpu_stats"].get("online_cpus", 1)
            
            cpu_percent = 0.0
            if system_delta > 0 and cpu_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * cpu_count * 100.0
            
            # Calculate memory usage
            memory_usage = stats["memory_stats"].get("usage", 0)
            memory_limit = stats["memory_stats"].get("limit", 1)
            memory_mb = memory_usage / (1024 * 1024)
            memory_limit_mb = memory_limit / (1024 * 1024)
            memory_percent = (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0.0
            
            return {
                "cpu_percent": round(cpu_percent, 2),
                "memory_mb": round(memory_mb, 2),
                "memory_limit_mb": round(memory_limit_mb, 2),
                "memory_percent": round(memory_percent, 2)
            }
        except Exception:
            return {
                "cpu_percent": 0.0,
                "memory_mb": 0.0,
                "memory_limit_mb": 0.0,
                "memory_percent": 0.0
            }
    
    def get_system_info(self) -> Dict:
        """Get Docker system information"""
        try:
            info = self.client.info()
            return {
                "containers": info.get("Containers", 0),
                "containers_running": info.get("ContainersRunning", 0),
                "containers_paused": info.get("ContainersPaused", 0),
                "containers_stopped": info.get("ContainersStopped", 0),
                "images": info.get("Images", 0),
                "server_version": info.get("ServerVersion", "unknown"),
                "operating_system": info.get("OperatingSystem", "unknown"),
                "total_memory_gb": round(info.get("MemTotal", 0) / (1024**3), 2)
            }
        except DockerException as e:
            return {"error": str(e)}
