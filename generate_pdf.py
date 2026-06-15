import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages dynamically and draws headers and footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Draw visual borders/accents on the cover page
            self.saveState()
            # Left accent color block (Teal)
            self.setFillColor(colors.HexColor("#0d9488"))
            self.rect(0, 0, 30, 792, fill=True, stroke=False)
            self.restoreState()
            return
            
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Header
        self.drawString(54, 750, "AI Docker Natural Language Health Dashboard — 1-Hour Presentation Guide")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 742, 558, 742)
        
        # Running Footer
        self.line(54, 55, 558, 55)
        self.drawString(54, 40, "Confidential — Presenter Reference Manual")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.restoreState()

def build_pdf():
    # Setup document template with 0.75 in (54 pt) margins
    # Since header is at 742/750 and footer at 55/40, printable top margin is 72, bottom is 72
    doc = SimpleDocTemplate(
        "Docker_NL_Dashboard_Presentation_Guide.pdf",
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Theme Styling
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=15,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0d9488'),
        spaceAfter=30,
        alignment=0
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#f8fafc'),
        backColor=colors.HexColor('#0f172a'),
        borderColor=colors.HexColor('#1e293b'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=5,
        spaceAfter=7
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )
    
    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    story = []
    
    # ==========================================
    # PAGE 1: TITLE/COVER PAGE
    # ==========================================
    story.append(Spacer(1, 120))
    story.append(Paragraph("<b>AI DOCKER NATURAL LANGUAGE<br/>HEALTH DASHBOARD</b>", title_style))
    story.append(Paragraph("<b>Presenter's Comprehensive Reference & 1-Hour Presentation Guide</b>", subtitle_style))
    
    story.append(Spacer(1, 40))
    
    meta_text = """
    <b>Document Class:</b> Systems Architecture & Technical Reference Guide<br/>
    <b>Target Audience:</b> DevOps Engineers, Site Reliability Engineers, and Product Stakeholders<br/>
    <b>Allocated Presentation Time:</b> 60 Minutes (with Q&A)<br/>
    <b>Core Technology Stack:</b> Python 3.11+, Streamlit Framework, Docker SDK, SQLite Engine, Ollama (Llama 3)<br/>
    <b>Release Status:</b> Production Ready (Version 1.0.0)<br/>
    <b>Compiled Date:</b> June 2026<br/>
    """
    story.append(Paragraph(meta_text, ParagraphStyle('CoverMeta', parent=body_style, fontSize=10, leading=15, textColor=colors.HexColor('#334155'))))
    
    story.append(Spacer(1, 100))
    story.append(Paragraph("<i>This reference guide provides deep architectural checklists, schemas, and troubleshooting workflows. Keep open for visual mapping support during presentations.</i>", ParagraphStyle('CoverFootnote', parent=body_style, fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=colors.HexColor('#64748b'))))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: EXECUTIVE BRIEF & 60-MIN AGENDA
    # ==========================================
    story.append(Paragraph("Executive Brief & Timing Breakdown", h1_style))
    story.append(Paragraph("The <b>AI Docker Natural Language Health Dashboard</b> is an operational dashboard designed to simplify container systems management. By integrating a local Large Language Model (LLM) with a transparent Reasoning + Acting (ReAct) agent orchestration loop, the platform translates plain-English administrative requests into secure, deterministic Docker SDK socket executions. It represents an important tool for hybrid deployment security, keeping metrics and configuration changes fully private on-premise.", body_style))
    
    story.append(Paragraph("1-Hour Presentation Session Outline", h2_style))
    story.append(Paragraph("This reference document maps directly to the slides and should be presented over a 60-minute duration. Use the following structured outline to balance theoretical concepts with live operational terminal demos:", body_style))
    
    # Timing Breakdown Table
    agenda_data = [
        [Paragraph("<b>Time (Mins)</b>", table_header_style), Paragraph("<b>Presentation Block & Focus Area</b>", table_header_style), Paragraph("<b>Presenter Key Goals</b>", table_header_style)],
        [Paragraph("00 - 10", table_body_style), Paragraph("Context & Solution Value Statement", table_body_style), Paragraph("Introduce Docker CLI barriers, cognitive load issues, and explain natural language mapping benefits.", table_body_style)],
        [Paragraph("10 - 25", table_body_style), Paragraph("System Architecture & ReAct Loop Mechanics", table_body_style), Paragraph("Walk through layers: app.py, agent.py, llm.py, and docker_manager.py. Explain the 7 ReAct steps.", table_body_style)],
        [Paragraph("25 - 40", table_body_style), Paragraph("UI Page Showcase & Operational Demo", table_body_style), Paragraph("Execute live command inputs ('restart nginx-test') to show the agent tracing, Plotly analytics, and GitHub status.", table_body_style)],
        [Paragraph("40 - 50", table_body_style), Paragraph("Operations, Persistence & Code Walkthrough", table_body_style), Paragraph("Explain SQLite DB schemas (prompt logs, container metrics), deployment compose files, and permissions.", table_body_style)],
        [Paragraph("50 - 60", table_body_style), Paragraph("Troubleshooting, QA Checklists & Q&A Open", table_body_style), Paragraph("Review socket error diagnostics and open-source roadmap items. Address audience questions.", table_body_style)]
    ]
    
    t = Table(agenda_data, colWidths=[80, 180, 244])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Core Audience Takeaways:", h2_style))
    story.append(Paragraph("• <b>Reliability:</b> The dashboard uses strict JSON schema templates to guarantee LLM command output security, avoiding the risk of free-text command execution.", bullet_style))
    story.append(Paragraph("• <b>Transparency:</b> SRE operators can view every reasoning thought, tool input parameter, and socket output directly in the UI, avoiding black-box automation risks.", bullet_style))
    story.append(Paragraph("• <b>Local Sovereignty:</b> Runs locally via Ollama with no external APIs required, making it safe for secure intranet environments.", bullet_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: CONTEXT, PROBLEM STATEMENT & VALUE PROPOSITION
    # ==========================================
    story.append(Paragraph("Context & Problem Statement", h1_style))
    story.append(Paragraph("In modern microservice operations, container runtimes like Docker have become ubiquitous. However, administering these stacks remains an operational bottleneck due to three critical friction points:", body_style))
    
    story.append(Paragraph("<b>1. Technical CLI Barriers:</b> The Docker command-line interface (CLI) is syntax-heavy. Operations like restarting crashed containers, checking resource utilization limits, or printing text logs require exact spelling, flag ordering, and target container hashes. Junior engineering staff or business stakeholders are frequently locked out of simple diagnostics, resulting in high MTTR (Mean Time to Resolution) during production incidents.", bullet_style))
    
    story.append(Paragraph("<b>2. Telemetry and Diagnostic Silos:</b> Standard setups scatter container health indicators across CLI logs, Docker API hooks, separate metric storage backends, and system journals. Operators must log into server terminals and run multiple tools to correlate resource spikes with container crash logs, introducing diagnostic delay.", bullet_style))
    
    story.append(Paragraph("<b>3. Privacy & Network Security Constraints:</b> Cloud-based AI management solutions (e.g. OpenAI API integrations) are unacceptable for high-security, firewalled server configurations. Passing system prompts containing internal service names, network maps, and credentials over external APIs creates a security risk.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("The Strategic Solution: Natural Language Operations", h1_style))
    story.append(Paragraph("The NL Dashboard bridges the technical knowledge gap by offering a <b>safe natural language system translation interface</b>. Instead of memorizing command structures, administrators write natural intent statements in a secure chat box. The interface handles the rest:", body_style))
    
    # Solution comparison box
    solution_code = """
   $ user_prompt: "restart the database container"
   
   $ react_thought: "The user wants to restart a container. I need to locate the container matching 'database'."
   $ react_tool_call: {"action": "restart_container", "name": "mysql-test"}
   $ docker_socket_api: client.containers.get("mysql-test").restart()
   
   $ result_summary: "Successfully restarted container mysql-test (ID: a1b2c3d4) in 842ms."
    """
    story.append(Paragraph(solution_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    
    story.append(Paragraph("This model changes systems administration from **procedural syntax commands** to **declarative state statements**, lowering operational requirements while retaining complete audit capabilities.", body_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: SYSTEM ARCHITECTURE & FILE LAYOUT
    # ==========================================
    story.append(Paragraph("High-Level System Architecture Layers", h1_style))
    story.append(Paragraph("The platform is structured following clean, decoupled modular patterns. Responsibility is divided across four isolated layers:", body_style))
    
    story.append(Paragraph("<b>1. Presentation Layer (app.py):</b> Built with Streamlit, it controls page state routing, injects custom navy-card CSS styles, maps pandas data tables, and hosts interactive Plotly chart structures.", bullet_style))
    story.append(Paragraph("<b>2. Orchestration Layer (agent.py):</b> Manages the ReactAgent logic loop. Steps through prompt validation, Thought interpretation, Tool routing parameters matching, and execution logging.", bullet_style))
    story.append(Paragraph("<b>3. Translation & Bindings Layer (llm.py, docker_manager.py, github_api.py):</b> Houses APIs wrapping native clients. Binds directly to the local UNIX Docker socket or named pipes, runs translation prompts, and queries GitHub status widgets.", bullet_style))
    story.append(Paragraph("<b>4. Database Layer (database.py):</b> Drives local transaction logging. Binds to a local SQLite database file to record prompt runs, metrics snapshots, and system audit logs.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Codebase File Structure Mapping", h1_style))
    story.append(Paragraph("The repository layout is organized to match these functional responsibilities, ensuring zero dependencies overlap:", body_style))
    
    # Structure details
    struct_text = """
    <b>docker-nl-dashboard/</b>
    ├── <b>app.py</b>                       # Streamlit UI bootstrap; handles 7 functional dashboard views.
    ├── <b>agent.py</b>                     # Implements ReactAgent orchestration logic & step state trackers.
    ├── <b>llm.py</b>                       # LLM connection wrappers (Ollama local API / Groq API fallbacks).
    ├── <b>docker_manager.py</b>           # Bindings to Python Docker SDK socket API and metrics helpers.
    ├── <b>database.py</b>                 # Core SQLite connection pools and table write/query wrappers.
    ├── <b>github_api.py</b>               # Connects to status.github.com and events feed under rate limit caps.
    ├── <b>prompts/</b>
    │   └── <b>system_prompt.txt</b>       # Rigid LLM translation prompts enforcing strict JSON schemas.
    ├── <b>data/</b>
    │   └── <b>dashboard.db</b>            # Auto-generated SQLite database file (prompt logs, telemetry).
    ├── <b>logs/</b>
    │   └── <b>prompt_log.txt</b>          # Simple text-file audit logger mapping raw LLM traces.
    ├── <b>test_demo.py</b>                 # QA script spinning up mock containers and verifying NLP actions.
    ├── <b>Dockerfile</b>                  # Multi-stage python base container configuration.
    └── <b>docker-compose.yml</b>          # Multi-container topology orchestration.
    """
    story.append(Paragraph(struct_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), ParagraphStyle('StructStyle', parent=body_style, fontName='Courier', fontSize=8.5, leading=12, backColor=colors.HexColor('#f1f5f9'), borderPadding=6, borderWidth=0.5, borderColor=colors.HexColor('#cbd5e1'))))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: THE REACT AGENT LOOP & THE 7 STEPS
    # ==========================================
    story.append(Paragraph("The ReAct (Reasoning & Acting) Loop Concept", h1_style))
    story.append(Paragraph("Traditional LLM integrations use a single 'blind' completion API call. This pattern is unsafe for system operations because the model must output the correct command immediately, with no intermediate logic review. Our dashboard implements a **ReAct loop structure**, forcing the agent to output its **Thought** (reasoning path) and **Action parameters** (parsed tool inputs) as visible data structures prior to socket execution.", body_style))
    
    story.append(Paragraph("Detailed Breakdown of the 7 Loop Steps", h1_style))
    story.append(Paragraph("Presenter Goal: Walk through each of the 7 stages that execute in sequence whenever a user enters a command:", body_style))
    
    # Table layout for steps
    steps_data = [
        [Paragraph("<b>Step</b>", table_header_style), Paragraph("<b>Name</b>", table_header_style), Paragraph("<b>Functional Responsibility & Code Boundary</b>", table_header_style)],
        [Paragraph("<b>1</b>", table_body_style), Paragraph("User Ingestion", table_body_style), Paragraph("Streamlit captures the command text block. Triggers layout state resets and renders step indicators.", table_body_style)],
        [Paragraph("<b>2</b>", table_body_style), Paragraph("AI Analysis", table_body_style), Paragraph("The text string is sent to llm.py along with system prompt instructions to build the Thought reasoning path.", table_body_style)],
        [Paragraph("<b>3</b>", table_body_style), Paragraph("Tool Selection", table_body_style), Paragraph("The agent parses the model's locked JSON structure, identifying target tool actions and container identifiers.", table_body_style)],
        [Paragraph("<b>4</b>", table_body_style), Paragraph("Tool Execution", table_body_style), Paragraph("The agent routes the parameters to docker_manager.py. The python SDK contacts the Docker socket to alter container states.", table_body_style)],
        [Paragraph("<b>5</b>", table_body_style), Paragraph("Result Ingestion", table_body_style), Paragraph("Docker socket logs, success strings, and elapsed millisecond execution metrics are captured as system observations.", table_body_style)],
        [Paragraph("<b>6</b>", table_body_style), Paragraph("Summary Design", table_body_style), Paragraph("The observations are sent back to the LLM. The model translates the raw JSON results into a natural English status message.", table_body_style)],
        [Paragraph("<b>7</b>", table_body_style), Paragraph("Render & Log", table_body_style), Paragraph("Renders step checklists (ticks/crosses) and summaries on screen. Triggers parallel async SQLite logging commits.", table_body_style)]
    ]
    
    t_steps = Table(steps_data, colWidths=[40, 100, 364])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(t_steps)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("This structural decomposition ensures that **even if a step fails** (e.g. Docker API returns a permissions error), the operator sees exactly where the pipeline failed, preserving complete diagnostic trace visibility.", body_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: PROMPT ENGINEERING & llm.py DETAILS
    # ==========================================
    story.append(Paragraph("Prompt Engineering & Schema Control", h1_style))
    story.append(Paragraph("To guarantee safety, the LLM must never output arbitrary conversation or markdown text headers during interpretation. If the model outputs text explanation, the agent parser fails. The system enforces strict **JSON output boundaries** using systemic instructions stored in prompts/system_prompt.txt.", body_style))
    
    story.append(Paragraph("Key Prompt Directives & Safe Rules:", h2_style))
    story.append(Paragraph("• <b>Rigid Output Constraints:</b> The prompt commands: <i>'You are a translator. You must output ONLY valid JSON. No conversational text, no headers, no markdown blocks.'</i> This forces the model's tokenizer to start with curly braces.", bullet_style))
    story.append(Paragraph("• <b>Schema White-listing:</b> The prompt lists the only valid action keys allowed: restart_container, stop_container, start_container, list_containers, get_container_logs, and get_container_resource_usage.", bullet_style))
    story.append(Paragraph("• <b>Few-Shot Scaffolding:</b> The system includes multiple question-answer mappings inside the context, showing the model how to resolve user prompts like <i>'check resource usage for nginx'</i> to `get_container_resource_usage` actions.", bullet_style))
    story.append(Paragraph("• <b>Muted Temperature Configuration:</b> The LLM completion client sets temperature to `0.1` and top_p to `0.1` to minimize speculative output variations and enforce deterministic responses.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Under the Hood: llm.py Implementation", h1_style))
    story.append(Paragraph("The `LLMManager` class handles API connections. It is built to support both local Ollama containers and cloud completions providers (such as Groq) as fallbacks:", body_style))
    
    llm_code = """
class LLMManager:
    def __init__(self, host="http://localhost:11434", model="llama3"):
        self.host = host
        self.model = model
        self.api_key = os.getenv("GROQ_API_KEY", "")
        
    def generate_action(self, user_prompt):
        # 1. Load prompts/system_prompt.txt
        # 2. Package prompt and context into structured API payload
        # 3. Call local Ollama completion server POST /api/generate
        # 4. If connection fails, attempts Groq llama-3.3-70b cloud fallback
        # 5. Parses and validates JSON block; returns fallback structure if errors occur
    """
    story.append(Paragraph(llm_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    
    story.append(Paragraph("By utilizing this multi-tier connection architecture, the dashboard maintains operational availability even during local GPU outages.", body_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: DOCKER MANAGER WRAPPER & SQL persistence
    # ==========================================
    story.append(Paragraph("Core Component: docker_manager.py Wrapper", h1_style))
    story.append(Paragraph("Direct Docker SDK access can block frontend threads. The `DockerManager` class acts as a safe, asynchronous wrapper around the python docker SDK. It encapsulates connection handling and calculates container resource statistics programmatically.", body_style))
    
    story.append(Paragraph("Presenter Focus: Telemetry Calculation Math", h2_style))
    story.append(Paragraph("Calculating CPU load trends from the raw Docker stats stream requires parsing delta values over time. The SDK returns cpu usage metrics as system ticks. The calculation is implemented as follows:", body_style))
    
    calc_code = """
# CPU utilization calculation formula
cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']

if system_delta > 0.0 and cpu_delta > 0.0:
    cpu_percent = (cpu_delta / system_delta) * len(cpu_stats['cpu_usage']['percpu_usage']) * 100.0
else:
    cpu_percent = 0.0
    
# Memory utilization conversion (from raw bytes to MBs)
memory_mb = stats['memory_stats']['usage'] / (1024.0 * 1024.0)
    """
    story.append(Paragraph(calc_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Core Component: database.py Persistence Schema", h1_style))
    story.append(Paragraph("The persistence system is built using SQLite, ensuring zero database configuration. The database `data/dashboard.db` contains three tables to track audits and metrics:", body_style))
    
    # Database Table Details
    db_text = """
    <b>1. prompt_logs:</b> Tracks AI Agent executions.<br/>
    • Schema: id (INTEGER PK), timestamp (TEXT), user_prompt (TEXT), generated_action (TEXT), execution_result (TEXT), execution_time_ms (REAL).<br/>
    <br/>
    <b>2. container_history:</b> Periodic telemetry resource snapshots.<br/>
    • Schema: id (INTEGER PK), timestamp (TEXT), container_id (TEXT), container_name (TEXT), status (TEXT), cpu_usage (REAL), memory_usage (REAL).<br/>
    <br/>
    <b>3. audit_logs:</b> Captures administrative state adjustments.<br/>
    • Schema: id (INTEGER PK), timestamp (TEXT), action (TEXT), status (TEXT), details (TEXT).
    """
    story.append(Paragraph(db_text, ParagraphStyle('DBStyle', parent=body_style, backColor=colors.HexColor('#f8fafc'), borderPadding=6, borderWidth=0.5, borderColor=colors.HexColor('#cbd5e1'))))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 8: MULTI-PAGE UI TOUR (STREAMLIT PAGES)
    # ==========================================
    story.append(Paragraph("Multi-Page UI Functional Tour", h1_style))
    story.append(Paragraph("Presenter Goal: Walk the audience through the Streamlit sidebar page routing. The application exposes seven dedicated pages, each styled with corporate navy KPI headers and responsive structures.", body_style))
    
    # 7 Pages list
    pages_data = [
        [Paragraph("<b>Page #</b>", table_header_style), Paragraph("<b>Page Name & Purpose</b>", table_header_style), Paragraph("<b>UI Features & Display Components</b>", table_header_style)],
        [Paragraph("1", table_body_style), Paragraph("Dashboard Overview", table_body_style), Paragraph("Displays metric cards for Total, Running, Stopped, and Unhealthy containers. Injects gradient colors and shadows.", table_body_style)],
        [Paragraph("2", table_body_style), Paragraph("Containers Grid", table_body_style), Paragraph("Displays container lists in a clean table (CPU%, Memory MB, ID). Interactive buttons trigger instant restarts.", table_body_style)],
        [Paragraph("3", table_body_style), Paragraph("AI Agent Console", table_body_style), Paragraph("Chat interface to type prompts. Displays step-by-step reasoning checkboxes (✅) as thoughts execute.", table_body_style)],
        [Paragraph("4", table_body_style), Paragraph("Diagnostic Logs", table_body_style), Paragraph("Renders tabular lists of historical logs. Expanders show prompt logs, container history databases, and auditable actions.", table_body_style)],
        [Paragraph("5", table_body_style), Paragraph("Plotly Analytics", table_body_style), Paragraph("Visualizes database telemetry logs. Draws pie/bar status distributions and historical CPU/Memory lines.", table_body_style)],
        [Paragraph("6", table_body_style), Paragraph("GitHub Sync Feed", table_body_style), Paragraph("Monitors status.github.com API health. Checks public feed event arrays under unauthenticated rate constraints.", table_body_style)],
        [Paragraph("7", table_body_style), Paragraph("System Settings", table_body_style), Paragraph("Configuration control panel. Tests socket paths, adjusts local Ollama host URLs, and model selection mappings.", table_body_style)]
    ]
    
    t_pages = Table(pages_data, colWidths=[45, 120, 339])
    t_pages.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(t_pages)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Streamlit Theme Overrides (app.py styling)", h2_style))
    story.append(Paragraph("Streamlit defaults are often plain. To create a modern, corporate look, `app.py` injects custom CSS to style the cards and buttons. For example, KPI cards are styled with soft shadows and thick slate borders: `border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; background-color: #ffffff;`. Command execution buttons are customized with solid teal backgrounds and white bold labels, matching enterprise software standards.", body_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 9: DEPLOYMENT & TROUBLESHOOTING
    # ==========================================
    story.append(Paragraph("Production Deployment Orchestration", h1_style))
    story.append(Paragraph("The platform is engineered to support rapid, isolated deployment configurations in server environments. Two main pipeline options are supported:", body_style))
    
    story.append(Paragraph("<b>Option 1: Multi-Service Docker Compose (Recommended)</b><br/>Orchestrates both the Streamlit dashboard app container and the local Ollama LLM service container. This setup isolates models locally and creates a local bridge network:", body_style))
    
    compose_code = """
version: '3.8'
services:
  ollama-service:
    image: ollama/ollama:latest
    container_name: ollama-service
    ports:
      - "11434:11434"
      
  dashboard-app:
    build: .
    container_name: docker-nl-dashboard
    ports:
      - "8501:8501"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro  # Read-Only Socket Mount
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - OLLAMA_HOST=http://ollama-service:11434
    depends_on:
      - ollama-service
    """
    story.append(Paragraph(compose_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    
    story.append(Paragraph("<b>Option 2: Standalone Container Mounting</b><br/>If Ollama runs as a native OS service, build and run the dashboard as a standalone container, mounting the host UNIX socket with read-only permission (`:ro`) for security.", body_style))
    
    story.append(Spacer(1, 5))
    story.append(Paragraph("Troubleshooting Diagnostic Playbook", h1_style))
    story.append(Paragraph("When deploying, operators may encounter environment permission blocks. Use this diagnostic flowchart to troubleshoot common issues:", body_style))
    
    story.append(Paragraph("• <b>Socket Bind Failures:</b> If the logs report <i>'Failed to connect to Docker daemon'</i>, the dashboard user lacks permissions to read `/var/run/docker.sock`. Fix on Linux by adding the user to the docker group: `sudo usermod -aG docker $USER`, then log out and back in.", bullet_style))
    story.append(Paragraph("• <b>Ollama Model Missing:</b> If the agent is unable to translate commands and reports empty thought blocks, check if the model is pulled. Verify by calling `curl http://localhost:11434/api/tags` and run `docker exec -it ollama-service ollama pull llama3`.", bullet_style))
    story.append(Paragraph("• <b>Port 8501 Conflicted:</b> If the dashboard does not boot, check for other processes using the port: `lsof -ti:8501 | xargs kill -9`, or override the port at startup: `streamlit run app.py --server.port 8502`.", bullet_style))
    
    story.append(PageBreak())

    # ==========================================
    # PAGE 10: QUALITY ASSURANCE & FUTURE ROADMAP
    # ==========================================
    story.append(Paragraph("Quality Assurance Protocol & Automated Testing", h1_style))
    story.append(Paragraph("To ensure reliability across microservice environments, the codebase includes a dedicated QA test suite in `test_demo.py`. Presenters should showcase this command line automation during technical deep-dives to highlight project stability.", body_style))
    
    story.append(Paragraph("The QA execution script performs the following validation pipeline:", body_style))
    story.append(Paragraph("1. Deploys three isolated mock containers: `nginx-test`, `redis-test`, and `mysql-test`.", bullet_style))
    story.append(Paragraph("2. Simulates natural language prompts in sequence (e.g. \"show running containers\", \"restart nginx-test\").", bullet_style))
    story.append(Paragraph("3. Intercepts JSON responses from the agent and verifies that the correct Docker API SDK calls were triggered.", bullet_style))
    story.append(Paragraph("4. Checks the database rows in `dashboard.db` to ensure that prompt execution times, latency logs, and container stats are successfully saved.", bullet_style))
    story.append(Paragraph("5. Cleans up by stopping and removing the mock containers.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Future Project Roadmap & Scaling", h1_style))
    story.append(Paragraph("The application layout is structured to support extensions. Future roadmap items for the development team include:", body_style))
    
    # Table layout for roadmap
    roadmap_data = [
        [Paragraph("<b>Phase</b>", table_header_style), Paragraph("<b>Development Milestone</b>", table_header_style), Paragraph("<b>Architectural Impact & Impact Area</b>", table_header_style)],
        [Paragraph("Phase 1", table_body_style), Paragraph("Remote Host Clustering", table_body_style), Paragraph("Extend Settings view to connect to remote Docker daemons via SSH credentials or HTTPS ports.", table_body_style)],
        [Paragraph("Phase 2", table_body_style), Paragraph("Compose Orchestration", table_body_style), Paragraph("Expand ReAct prompt dictionaries to support loading, configuring, and starting compose projects.", table_body_style)],
        [Paragraph("Phase 3", table_body_style), Paragraph("Live WebSocket Telemetry", table_body_style), Paragraph("Replace Streamlit pandas refresh intervals with real-time socket connections for charts.", table_body_style)],
        [Paragraph("Phase 4", table_body_style), Paragraph("Role-Based Access (RBAC)", table_body_style), Paragraph("Implement authentication, separating read-only telemetry viewers from active operators.", table_body_style)]
    ]
    
    t_road = Table(roadmap_data, colWidths=[55, 130, 319])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(t_road)
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("Conclusion & Key Takeaways", h1_style))
    story.append(Paragraph("The **AI Docker Natural Language Health Dashboard** successfully simplifies container administration by translating natural intent into deterministic actions. It provides a secure, traceable alternative to procedural CLI scripting. Running models locally preserves complete data privacy, and the detailed SQLite audit logging meets corporate compliance needs. This platform is fully prepared for local staging or production deployments.", body_style))
    
    # Build the PDF using our custom canvas class
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Compiled successfully!")

if __name__ == "__main__":
    build_pdf()
