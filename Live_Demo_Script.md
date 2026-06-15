# 🎙️ 20-Minute Live Demonstration Presenter Script
## AI Docker Natural Language Health Dashboard

This guide provides a step-by-step presenter script for a **20-minute live demonstration** of the AI Docker Natural Language Health Dashboard. It outlines exact talking points, command executions, dashboard clicks, and expected system responses.

---

## ⏱️ Live Demo Timeline & Outline

*   **Phase 1: Startup & Bootstrap (00:00 - 04:00):** Booting services, checking sockets, and loading the UI.
*   **Phase 2: UI Tour & Operations Grid (04:00 - 08:00):** Custom-styled KPI cards and tabular management controls.
*   **Phase 3: Live AI Agent Chat & ReAct Loop (08:00 - 13:00):** Executing natural language commands and explaining agent reasoning.
*   **Phase 4: Analytics, Auditing & Persistence (13:00 - 17:00):** Visualizing telemetry and checking SQLite tables.
*   **Phase 5: Automated QA Run & Handover (17:00 - 20:00):** Running automated validation checks and concluding.

---

### 🟢 Phase 1: Startup & Bootstrap (00:00 - 04:00)

**Goal:** Show that the platform is ready for production, boot it up live, check service connections, and open the web app.

#### 🎙️ Presenter Script & Talking Points:
> "Hello everyone. In this section of our presentation, I am going to demonstrate the live working of the AI Docker Natural Language Health Dashboard. 
> 
> Before we look at the web dashboard, let's verify our environment configuration. The system is designed to run locally, ensuring that server data and command prompts are kept private on-premise. It connects directly to the host's Docker socket and uses local LLM models."

#### 💻 Actions (In the Terminal):
1. **Open your terminal** in the project directory.
2. **Execute the startup command** to launch the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```
3. **Show that the services are running** by typing:
   ```bash
   docker ps
   ```
   *Point out that the `docker-nl-dashboard` and `ollama-service` containers are active.*
4. **Test the Ollama connection** to confirm the translation model is ready:
   ```bash
   curl http://localhost:11434/api/tags
   ```
   *Explain that this API response list confirms the `llama3` model is loaded locally and ready to receive instructions.*
5. **Open the browser** and navigate to:
   ```
   http://localhost:8501
   ```
   *Show the browser screen loading the modern, dark-themed operations center.*

---

### 🔵 Phase 2: UI Tour & Operations Grid (04:00 - 08:00)

**Goal:** Tour the dashboard layout, showcase the custom styling overrides, and show how to manage containers with standard click buttons.

#### 🎙️ Presenter Script & Talking Points:
> "We are now inside the dashboard. As you can see, we have overridden Streamlit's default templates to construct a dark-themed, corporate-grade dashboard. 
> 
> Let's look at Page 1: the **Dashboard Overview**. At the top, we have our key performance indicator (KPI) metric cards. These cards dynamically fetch states from the Docker socket. We can see the Total Containers, Running, Stopped, and Unhealthy counts.
> 
> Now, let's navigate to Page 2: the **Containers Management Grid**."

#### 💻 Actions (In the UI):
1. **Click on "Dashboard"** in the sidebar. Point out the KPI counters matching your Docker daemon state.
2. **Click on "Containers"** in the sidebar to open the grid page.
3. **Filter the container table** by using the status select dropdown (select "Running" then "All").
4. **Demonstrate manual administrative override buttons**:
   * Locate a test container (e.g. `redis-test` or `nginx-test`).
   * **Click the "Stop" button** next to it in the grid.
   * *Point to the screen as the container status changes to "exited".*
   * **Click the "Start" button** to bring it back online.
5. **Explain the architecture:**
   > "When I click these buttons, app.py catches the UI event and triggers a wrapped function in docker_manager.py. The script communicates with the UNIX socket, completes the state transition, and refreshes the data frame. This is a simple fallback for manual administrators."

---

### 🟠 Phase 3: Live AI Agent Chat & ReAct Loop (08:00 - 13:00)

**Goal:** Demonstrate the core value of the project—commanding Docker using natural language. Show how the ReAct loop reasons through commands.

#### 🎙️ Presenter Script & Talking Points:
> "Now, let's look at the core of this project: the **AI Agent Chat Interface**. 
> 
> In traditional setups, if an operator wants to review logs or check resource utilization, they have to write complex commands with exact flags in the terminal. Here, we can input natural English commands.
> 
> What makes our agent unique is that it does not execute prompts blindly. It steps through a 7-phase Reasoning + Acting (ReAct) loop. Let's see this in action."

#### 💻 Actions (In the UI):
1. **Click on "AI Agent"** in the sidebar.
2. **Input Prompt 1:** Type `"show running containers"` and press Enter.
   * **What to point out:** Show the steps checklist appearing in real-time. Point to the thought trace that maps "show running" to the `list_containers` action with a status filter of `running`.
3. **Input Prompt 2:** Type `"stop redis-test"` and press Enter.
   * **What to point out:** Explain how the agent identifies the target name `redis-test` and maps the intent to the `stop_container` action. Point out the green checkmarks (✅) indicating each phase completed successfully.
4. **Input Prompt 3:** Type `"get resource usage for mysql-test"` and press Enter.
   * **What to point out:** Explain how the system calculates the delta CPU load in real-time (comparing container ticks with system ticks) and renders the utilization statistics (e.g., CPU: `1.4%` | Memory: `340 MB`).
5. **Input Prompt 4:** Type `"show nginx-test logs"` and press Enter.
   * **What to point out:** Show how the agent pulls the stdout stream from the container socket and displays the output blocks directly in the UI.

---

### 🟡 Phase 4: Analytics, Auditing & Persistence (13:00 - 17:00)

**Goal:** Show how data collected by the agent is stored and visualized. Explain the SQLite schemas.

#### 🎙️ Presenter Script & Talking Points:
> "Every action we execute, whether it is a button click or a natural language command, is permanently tracked. The dashboard writes logs to both flat files and a local SQLite database file.
> 
> Let's look at Page 5: the **Analytics View**."

#### 💻 Actions (In the UI):
1. **Click on "Analytics"** in the sidebar.
   * **Show the Plotly charts:** Show the pie chart representing container status distribution and the bar charts displaying historical resource spikes.
   * Explain: *"These interactive charts read records directly from our SQLite container_history tables."*
2. **Click on "Logs"** in the sidebar.
   * **Open the "Prompt Logs" tab:** Expand the log entries. Show the user prompt, the JSON action generated by Llama, and the execution times in milliseconds.
   * **Open the "Audit Logs" tab:** Show the audit rows detailing the administrative container stop/start transitions.
3. **Explain the database security:**
   > "By saving prompt logs, container histories, and audit events in SQLite tables, our dashboard provides complete transparency. IT departments can audit every command to see who initiated an action, what parameters were parsed, and how the system responded."

---

### 🔵 Phase 5: Automated QA Run & Handover (17:00 - 20:00)

**Goal:** Run the automated testing scripts to show how the project is validated, summarize the architecture, and hand over for Q&A.

#### 🎙️ Presenter Script & Talking Points:
> "Finally, let's look at how we verify our application's stability. We have built an automated test runner script called test_demo.py. It automates environment verification by spinning up mock containers, executing test prompts, checking database states, and cleaning up."

#### 💻 Actions (In the Terminal):
1. **Open your terminal** alongside the web browser.
2. **Execute the test suite**:
   ```bash
   python test_demo.py
   ```
3. **Show the test output**:
   * Point out the creation of `nginx-test`, `redis-test`, and `mysql-test`.
   * Point out the test logs showing queries (e.g. "show running", "restart nginx-test") resolving with status `success`.
   * Point out the database verification printing counts of logs saved.
   * Point out the cleanup section deleting the testing containers.
4. **Switch back to the presentation slides or wrap up**:
   > "This concludes our live demonstration. We have shown that the AI Docker Natural Language Health Dashboard successfully:
   > 1. Translates plain English statements into Docker socket commands.
   > 2. Visualizes CPU and Memory metrics in real-time.
   > 3. Enforces strict JSON security boundaries via Groq Llama models.
   > 4. Maintains complete local privacy and compliance auditing records.
   > 
   > Thank you, and I am now ready to open the floor to any questions."

---

## 💡 Pro-Tips for a Successful Demo

*   **Pre-Create Test Containers:** Before starting your presentation, ensure your docker environment is clean. Run `docker ps -a` to make sure there are no conflicting container names like `nginx-test` or `redis-test`.
*   **Keep settings open:** If Ollama response times are slightly slow due to hardware constraints, explain that this is because model execution is happening locally on-premise, preserving complete privacy.
*   **Use the Settings Page:** If you run into Ollama connection errors during the demo, click on the **Settings** tab in the sidebar and verify that the Ollama Host address matches your backend port (e.g. `http://localhost:11434`).
