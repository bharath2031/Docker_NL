#!/usr/bin/env python3
"""
Test and Demo Script for AI Docker NL Dashboard
Creates sample containers and tests various commands
"""

import subprocess
import time
import json
from agent import ReactAgent

def run_command(cmd):
    """Execute shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def create_test_containers():
    """Create sample Docker containers for testing"""
    print("=" * 80)
    print("CREATING TEST CONTAINERS")
    print("=" * 80)
    
    containers = [
        ("nginx-test", "docker run -d --name nginx-test nginx"),
        ("redis-test", "docker run -d --name redis-test redis"),
        ("mysql-test", "docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=test mysql")
    ]
    
    created = []
    
    for name, cmd in containers:
        print(f"\nCreating {name}...")
        success, output = run_command(cmd)
        
        if success:
            print(f"✅ {name} created successfully")
            created.append(name)
        else:
            if "already in use" in output.lower():
                print(f"⚠️  {name} already exists")
                created.append(name)
            else:
                print(f"❌ Failed to create {name}: {output}")
    
    time.sleep(5)  # Wait for containers to start
    
    print(f"\n✅ {len(created)} containers ready for testing")
    return created

def test_agent_commands():
    """Test various natural language commands"""
    print("\n" + "=" * 80)
    print("TESTING AI AGENT COMMANDS")
    print("=" * 80)
    
    agent = ReactAgent()
    
    test_commands = [
        "show running containers",
        "list all containers",
        "get resource usage for nginx-test",
        "show nginx-test logs"
    ]
    
    results = []
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n[Test {i}/{len(test_commands)}] Command: '{command}'")
        print("-" * 80)
        
        try:
            steps, result = agent.execute(command)
            
            print(f"✅ Execution completed in {len(steps)} steps")
            print(f"Summary: {result.get('summary', 'N/A')}")
            
            results.append({
                "command": command,
                "success": result.get("success", False),
                "summary": result.get("summary", ""),
                "steps": len(steps)
            })
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            results.append({
                "command": command,
                "success": False,
                "error": str(e),
                "steps": 0
            })
    
    return results

def generate_expected_output():
    """Generate expected dashboard output in JSON format"""
    print("\n" + "=" * 80)
    print("EXPECTED DASHBOARD OUTPUT")
    print("=" * 80)
    
    expected = {
        "dashboard_kpis": {
            "total_containers": 3,
            "running": 3,
            "stopped": 0,
            "restarting": 0,
            "unhealthy": 0
        },
        "containers_table": [
            {
                "name": "nginx-test",
                "status": "running",
                "image": "nginx",
                "cpu_percent": "0.5-2.0",
                "memory_mb": "30-60",
                "id": "dynamic"
            },
            {
                "name": "redis-test",
                "status": "running",
                "image": "redis",
                "cpu_percent": "0.2-1.0",
                "memory_mb": "10-30",
                "id": "dynamic"
            },
            {
                "name": "mysql-test",
                "status": "running",
                "image": "mysql",
                "cpu_percent": "1.0-5.0",
                "memory_mb": "200-400",
                "id": "dynamic"
            }
        ],
        "ai_agent_execution": {
            "command": "show running containers",
            "steps": [
                {"step": 1, "name": "User Request", "status": "completed"},
                {"step": 2, "name": "AI Analysis", "status": "completed"},
                {"step": 3, "name": "Tool Selection", "status": "completed"},
                {"step": 4, "name": "Tool Execution", "status": "completed"},
                {"step": 5, "name": "Result Collection", "status": "completed"},
                {"step": 6, "name": "Summary Generation", "status": "completed"},
                {"step": 7, "name": "Response Return", "status": "completed"}
            ],
            "summary": "Found 3 container(s). 3 running normally. Resource usage is within normal range."
        },
        "analytics_charts": {
            "status_distribution": {
                "running": 3,
                "stopped": 0,
                "restarting": 0
            },
            "cpu_usage": {
                "nginx-test": "0.5-2.0%",
                "redis-test": "0.2-1.0%",
                "mysql-test": "1.0-5.0%"
            },
            "memory_usage": {
                "nginx-test": "30-60 MB",
                "redis-test": "10-30 MB",
                "mysql-test": "200-400 MB"
            }
        }
    }
    
    print(json.dumps(expected, indent=2))
    return expected

def cleanup_containers():
    """Remove test containers"""
    print("\n" + "=" * 80)
    print("CLEANUP")
    print("=" * 80)
    
    response = input("\nDo you want to remove test containers? (y/N): ")
    
    if response.lower() == 'y':
        containers = ["nginx-test", "redis-test", "mysql-test"]
        
        for name in containers:
            print(f"Removing {name}...")
            run_command(f"docker rm -f {name}")
        
        print("✅ Cleanup completed")
    else:
        print("ℹ️  Test containers kept for manual testing")

def main():
    """Main test execution"""
    print("\n" + "=" * 80)
    print("AI DOCKER NL DASHBOARD - TEST & DEMO")
    print("=" * 80)
    print("\nThis script will:")
    print("1. Create 3 test Docker containers (nginx, redis, mysql)")
    print("2. Test natural language commands via the AI agent")
    print("3. Generate expected dashboard output")
    print("4. Optionally cleanup test containers")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Create containers
    containers = create_test_containers()
    
    if not containers:
        print("\n❌ No containers created. Exiting.")
        return
    
    # Step 2: Test agent commands
    test_results = test_agent_commands()
    
    # Step 3: Generate expected output
    expected = generate_expected_output()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in test_results if r.get("success", False))
    total = len(test_results)
    
    print(f"\nTests Passed: {successful}/{total}")
    print(f"Containers Created: {len(containers)}")
    print(f"\n✅ Dashboard should now show:")
    print(f"   - Total Containers: {len(containers)}")
    print(f"   - Running: {len(containers)}")
    print(f"   - All visualizations populated with data")
    
    print(f"\n📊 Access the dashboard at: http://localhost:8501")
    
    # Step 4: Cleanup
    cleanup_containers()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
