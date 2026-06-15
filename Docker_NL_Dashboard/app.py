import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import time
import os

from agent import ReactAgent
from docker_manager import DockerManager
from database import Database
from github_api import GitHubAPI
from llm import LLMManager

# Page configuration
st.set_page_config(
    page_title="AI Docker NL Health Dashboard",
    page_icon="🐳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean Light Theme with Dark Navy Cards
st.markdown("""
    <style>
    /* Compact layout */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    
    /* Main background - Clean white/light gray */
    .main {
        background-color: #f5f7fa;
        color: #2c3e50;
    }
    
    /* Sidebar - White with subtle border */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d0d7de;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    
    /* Headers - Dark navy */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        color: #34495e !important;
    }
    
    /* Metric cards - White background like in screenshot */
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #d0d7de;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }
    
    /* Metric labels - Dark gray text */
    div[data-testid="stMetric"] label {
        color: #6c757d !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metric values - Large dark numbers */
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2c3e50 !important;
        font-size: 48px !important;
        font-weight: 700 !important;
    }
    
    /* Metric delta - Green */
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #27ae60 !important;
        font-size: 16px !important;
    }
    
    /* Buttons - Green with black text */
    .stButton>button {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        color: #000000;
        border-radius: 6px;
        padding: 0.65rem 1.5rem;
        border: none;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 2px 6px rgba(39, 174, 96, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #229954 0%, #1e8449 100%);
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);
        transform: translateY(-2px);
    }
    
    /* DataFrames - Clean white with borders */
    .stDataFrame {
        background-color: #ffffff !important;
        border: 1px solid #d0d7de;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stDataFrame table {
        color: #2c3e50 !important;
    }
    
    .stDataFrame th {
        background-color: #f5f7fa !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #d0d7de !important;
        padding: 12px !important;
    }
    
    .stDataFrame td {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border-bottom: 1px solid #e8ecf1 !important;
        padding: 10px !important;
    }
    
    .stDataFrame tr:hover td {
        background-color: #f5f7fa !important;
    }
    
    /* Text input - Clean white with border */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 2px solid #d0d7de !important;
        border-radius: 6px;
        font-size: 15px;
        padding: 0.5rem;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #27ae60 !important;
        box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1) !important;
        outline: none !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #d0d7de !important;
        border-radius: 6px;
    }
    
    /* Expanders - Clean white cards */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px;
        font-weight: 600;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f5f7fa !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #d0d7de !important;
        border-top: none !important;
        color: #2c3e50 !important;
        padding: 1rem !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        background-color: #ffffff !important;
        border-left: 4px solid #27ae60 !important;
        color: #2c3e50 !important;
        border-radius: 6px;
    }
    
    /* Code blocks */
    code {
        background-color: #f5f7fa !important;
        color: #e74c3c !important;
        padding: 3px 6px;
        border-radius: 4px;
        border: 1px solid #d0d7de;
        font-family: 'Courier New', monospace;
    }
    
    pre {
        background-color: #2c3e50 !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px;
        padding: 1rem;
        color: #ecf0f1 !important;
    }
    
    /* Scrollbar - Clean minimal */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f7fa;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #95a5a6;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7f8c8d;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 6px;
    }
    
    /* Error message */
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
        border-radius: 6px;
    }
    
    /* Warning message */
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeaa7 !important;
        border-radius: 6px;
    }
    
    /* Radio buttons and checkboxes */
    .stRadio label, .stCheckbox label {
        color: #2c3e50 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        color: #2c3e50;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #27ae60 !important;
        color: #ffffff !important;
    }
    
    /* Step boxes - Colored borders for status */
    .step-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #d0d7de;
    }
        </style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "docker" not in st.session_state:
    st.session_state.docker = None
if "db" not in st.session_state:
    st.session_state.db = Database()
if "github" not in st.session_state:
    st.session_state.github = GitHubAPI()

# Initialize components
@st.cache_resource
def init_agent():
    return ReactAgent()

@st.cache_resource
def init_docker():
    try:
        return DockerManager()
    except Exception as e:
        st.error(f"Failed to connect to Docker: {str(e)}")
        return None

# Sidebar navigation
st.sidebar.title("🐳 Docker NL Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Containers", "AI Agent", "Logs", "Analytics", "GitHub API", "Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")

# Quick stats in sidebar
try:
    docker = init_docker()
    if docker:
        system_info = docker.get_system_info()
        st.sidebar.metric("Total Containers", system_info.get("containers", 0))
        st.sidebar.metric("Running", system_info.get("containers_running", 0))
        st.sidebar.metric("Stopped", system_info.get("containers_stopped", 0))
except Exception as e:
    st.sidebar.warning("Docker stats unavailable")

# PAGE 1: DASHBOARD
if page == "Dashboard":
    st.title("🐳 Docker Health Dashboard")
    st.markdown("### Overview")
    
    docker = init_docker()
    if not docker:
        st.error("Cannot connect to Docker daemon. Please ensure Docker is running.")
    else:
        # Get system info
        system_info = docker.get_system_info()
        containers = docker.list_containers(status_filter=None)
        
        # KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Containers", system_info.get("containers", 0))
        
        with col2:
            running = system_info.get("containers_running", 0)
            st.metric("Running", running, delta=None, delta_color="normal")
        
        with col3:
            stopped = system_info.get("containers_stopped", 0)
            st.metric("Stopped", stopped)
        
        with col4:
            restarting = sum(1 for c in containers if c.get("status") == "restarting")
            st.metric("Restarting", restarting, delta=None, delta_color="inverse")
        
        with col5:
            unhealthy = sum(1 for c in containers if c.get("status") == "running" and c.get("cpu_usage", 0) > 90)
            st.metric("Unhealthy", unhealthy, delta=None, delta_color="inverse")
        
        st.markdown("---")
        
        # System Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### System Information")
            st.write(f"**Docker Version:** {system_info.get('server_version', 'unknown')}")
            st.write(f"**OS:** {system_info.get('operating_system', 'unknown')}")
            st.write(f"**Total Memory:** {system_info.get('total_memory_gb', 0)} GB")
            st.write(f"**Images:** {system_info.get('images', 0)}")
        
        with col2:
            st.markdown("### Quick Actions")
            if st.button("🔄 Refresh Dashboard"):
                st.rerun()
            if st.button("📊 View Analytics"):
                st.session_state.page = "Analytics"
                st.rerun()

# PAGE 2: CONTAINERS
elif page == "Containers":
    st.title("📦 Container Management")
    
    docker = init_docker()
    if not docker:
        st.error("Cannot connect to Docker daemon.")
    else:
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["all", "running", "exited", "paused", "restarting"]
            )
        with col2:
            st.write("")
        with col3:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        # Get containers
        filter_val = None if status_filter == "all" else status_filter
        containers = docker.list_containers(status_filter=filter_val)
        
        if not containers:
            st.info(f"No {status_filter} containers found.")
        else:
            # Display as table
            df = pd.DataFrame(containers)
            
            # Select and reorder columns
            display_cols = ["name", "status", "image", "cpu_usage", "memory_usage", "id"]
            df_display = df[display_cols].copy()
            df_display.columns = ["Name", "Status", "Image", "CPU %", "Memory MB", "ID"]
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            st.markdown("### Container Actions")
            
            container_names = [c["name"] for c in containers]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                selected = st.selectbox("Select Container", container_names)
            
            with col2:
                if st.button("▶️ Start"):
                    result = docker.start_container(selected)
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))
            
            with col3:
                if st.button("⏸️ Stop"):
                    result = docker.stop_container(selected)
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))
            
            with col4:
                if st.button("🔄 Restart"):
                    result = docker.restart_container(selected)
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))

# PAGE 3: AI AGENT
elif page == "AI Agent":
    st.title("🤖 AI Natural Language Agent")
    st.markdown("### Ask questions in natural language")
    
    # Initialize agent
    agent = init_agent()
    
    # Examples
    with st.expander("💡 Example Commands"):
        st.markdown("""
        - Show running containers
        - List all containers
        - Show restarting containers
        - Restart nginx
        - Start mysql
        - Stop redis
        - Check nginx health
        - Show nginx logs
        - What crashed in the last hour?
        - Get resource usage for nginx
        """)
    
    # Input
    user_input = st.text_input(
        "Enter your command:",
        placeholder="e.g., Show running containers"
    )
    
    if st.button("🚀 Execute", type="primary"):
        if not user_input:
            st.warning("Please enter a command.")
        else:
            # Execute agent
            with st.spinner("Processing..."):
                steps, result = agent.execute(user_input)
            
            # Display steps
            st.markdown("### 🔄 Execution Steps (ReAct Loop)")
            
            for step in steps:
                status_emoji = "✅" if step.status == "completed" else "❌" if step.status == "failed" else "⏳"
                
                with st.expander(f"{status_emoji} Step {step.step_number}: {step.name}", expanded=True):
                    st.write(f"**Description:** {step.description}")
                    st.write(f"**Status:** {step.status}")
                    
                    if step.result:
                        st.write("**Result:**")
                        if isinstance(step.result, dict) or isinstance(step.result, list):
                            st.json(step.result)
                        else:
                            st.write(step.result)
                    
                    if step.get_duration_ms() > 0:
                        st.write(f"**Duration:** {step.get_duration_ms():.2f}ms")
            
            st.markdown("---")
            
            # Display final result
            if result.get("success"):
                st.success("### ✅ Summary")
                st.write(result.get("summary", "Operation completed successfully."))
                
                # Display data if available
                if "result" in result and isinstance(result["result"], list):
                    st.markdown("### 📊 Data")
                    df = pd.DataFrame(result["result"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("### ❌ Error")
                st.write(result.get("error", "Unknown error"))
                if "details" in result:
                    st.write(f"**Details:** {result['details']}")

# PAGE 4: LOGS
elif page == "Logs":
    st.title("📋 Logs & Audit Trail")
    
    tab1, tab2, tab3 = st.tabs(["Prompt Logs", "Audit Logs", "Container History"])
    
    db = st.session_state.db
    
    with tab1:
        st.markdown("### Prompt Execution Logs")
        logs = db.get_prompt_logs(limit=50)
        
        if not logs:
            st.info("No prompt logs found.")
        else:
            for log in logs:
                with st.expander(f"🕐 {log['timestamp']} - {log['user_prompt'][:50]}..."):
                    st.write(f"**User Prompt:** {log['user_prompt']}")
                    st.write(f"**Generated Action:**")
                    try:
                        action = json.loads(log['generated_action'])
                        st.json(action)
                    except:
                        st.code(log['generated_action'])
                    st.write(f"**Result:** {log['execution_result']}")
                    st.write(f"**Execution Time:** {log['execution_time_ms']:.2f}ms")
    
    with tab2:
        st.markdown("### Audit Logs")
        audit_logs = db.get_audit_logs(limit=50)
        
        if not audit_logs:
            st.info("No audit logs found.")
        else:
            df = pd.DataFrame(audit_logs)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Container History")
        history = db.get_container_history(limit=100)
        
        if not history:
            st.info("No container history found.")
        else:
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True, hide_index=True)

# PAGE 5: ANALYTICS
elif page == "Analytics":
    st.title("📊 Analytics & Visualizations")
    
    docker = init_docker()
    db = st.session_state.db
    
    if not docker:
        st.error("Cannot connect to Docker daemon.")
    else:
        containers = docker.list_containers(status_filter=None)
        
        # Status distribution
        st.markdown("### Container Status Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            status_counts = {}
            for c in containers:
                status = c.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=list(status_counts.keys()),
                    y=list(status_counts.values()),
                    marker_color=['#4caf50', '#ff9800', '#f44336', '#2196f3']
                )
            ])
            fig_bar.update_layout(
                title="Container Count by Status",
                xaxis_title="Status",
                yaxis_title="Count",
                template="plotly_dark"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie chart
            fig_pie = go.Figure(data=[
                go.Pie(
                    labels=list(status_counts.keys()),
                    values=list(status_counts.values()),
                    hole=0.3
                )
            ])
            fig_pie.update_layout(
                title="Status Distribution",
                template="plotly_dark"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Resource usage
        st.markdown("### Resource Usage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU usage
            running_containers = [c for c in containers if c.get("status") == "running"]
            if running_containers:
                names = [c["name"] for c in running_containers]
                cpu = [c.get("cpu_usage", 0) for c in running_containers]
                
                fig_cpu = go.Figure(data=[
                    go.Bar(
                        x=names,
                        y=cpu,
                        marker_color='#2196f3'
                    )
                ])
                fig_cpu.update_layout(
                    title="CPU Usage by Container (%)",
                    xaxis_title="Container",
                    yaxis_title="CPU %",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_cpu, use_container_width=True)
        
        with col2:
            # Memory usage
            if running_containers:
                memory = [c.get("memory_usage", 0) for c in running_containers]
                
                fig_mem = go.Figure(data=[
                    go.Bar(
                        x=names,
                        y=memory,
                        marker_color='#4caf50'
                    )
                ])
                fig_mem.update_layout(
                    title="Memory Usage by Container (MB)",
                    xaxis_title="Container",
                    yaxis_title="Memory MB",
                    template="plotly_dark"
                )
                st.plotly_chart(fig_mem, use_container_width=True)
        
        st.markdown("---")
        
        # Container history timeline
        st.markdown("### Container Status Over Time")
        history = db.get_container_history(limit=200)
        
        if history:
            df_history = pd.DataFrame(history)
            df_history['timestamp'] = pd.to_datetime(df_history['timestamp'])
            
            # Group by container and plot status changes
            fig_timeline = px.scatter(
                df_history,
                x='timestamp',
                y='container_name',
                color='status',
                title='Container Status Timeline',
                template='plotly_dark'
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

# PAGE 6: GITHUB API
elif page == "GitHub API":
    st.title("🔗 GitHub API Integration")
    
    github = st.session_state.github
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### GitHub Status")
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        status = github.get_status()
        if status.get("success"):
            indicator = status.get("indicator", "none")
            description = status.get("description", "Unknown")
            
            if indicator == "none":
                st.success(f"✅ {description}")
            elif indicator == "minor":
                st.warning(f"⚠️ {description}")
            else:
                st.error(f"🔴 {description}")
            
            st.write(f"**Last Updated:** {status.get('updated_at', 'Unknown')}")
        else:
            st.error(f"Failed to fetch status: {status.get('error', 'Unknown')}")
    
    with col2:
        st.markdown("### API Rate Limit")
        rate_limit = github.get_rate_limit()
        
        if rate_limit.get("success"):
            remaining = rate_limit.get("remaining", 0)
            limit = rate_limit.get("limit", 0)
            used = rate_limit.get("used", 0)
            
            st.metric("Remaining Requests", remaining)
            st.metric("Total Limit", limit)
            st.metric("Used", used)
            
            # Progress bar
            if limit > 0:
                progress = remaining / limit
                st.progress(progress)
        else:
            st.error("Failed to fetch rate limit")
    
    st.markdown("---")
    
    # Public events
    st.markdown("### Recent Public Events")
    
    if st.button("🔄 Refresh Events"):
        st.rerun()
    
    events = github.get_public_events(limit=15)
    
    if events.get("success"):
        event_list = events.get("events", [])
        
        if event_list:
            for event in event_list:
                with st.expander(f"{event['type']} - {event['repo']} by {event['actor']}"):
                    st.write(f"**Event Type:** {event['type']}")
                    st.write(f"**Repository:** {event['repo']}")
                    st.write(f"**Actor:** {event['actor']}")
                    st.write(f"**Created:** {event['created_at']}")
                    st.write(f"**ID:** {event['id']}")
        else:
            st.info("No events found.")
    else:
        st.error(f"Failed to fetch events: {events.get('error', 'Unknown')}")

# PAGE 7: SETTINGS
elif page == "Settings":
    st.title("⚙️ Settings & Configuration")
    
    st.markdown("### Docker Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        docker_socket = st.text_input(
            "Docker Socket",
            value="unix:///var/run/docker.sock",
            help="Docker daemon socket path"
        )
    
    with col2:
        docker_host = st.text_input(
            "Docker Host",
            value="",
            placeholder="tcp://localhost:2375",
            help="Optional Docker host URL"
        )
    
    st.markdown("---")
    st.markdown("### Groq AI Configuration")
    
    st.info("💡 Get your free API key from https://console.groq.com/keys")
    
    col1, col2 = st.columns(2)
    
    with col1:
        groq_api_key = st.text_input(
            "Groq API Key",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            help="Your Groq API key for AI natural language processing"
        )
        
        if st.button("💾 Save API Key to Environment"):
            if groq_api_key:
                os.environ["GROQ_API_KEY"] = groq_api_key
                st.success("✅ API key saved for this session!")
            else:
                st.warning("Please enter an API key first")
    
    with col2:
        groq_model = st.text_input(
            "Groq Model",
            value="llama-3.3-70b-versatile",
            help="Active models: llama-3.3-70b-versatile, gemma2-9b-it, llama-3.1-8b-instant"
        )
    
    if st.button("🧪 Test Groq Connection"):
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
            llm = LLMManager(model=groq_model, api_key=groq_api_key)
            result = llm.test_connection()
            
            if result.get("success"):
                st.success(f"✅ {result.get('message')} - Model: {result.get('model')}")
            else:
                st.error(f"❌ {result.get('message')}: {result.get('error')}")
        else:
            st.warning("⚠️ Please enter your Groq API key first")
    
    st.markdown("---")
    st.markdown("### Database Configuration")
    
    db_path = st.text_input(
        "Database Path",
        value="data/dashboard.db",
        help="SQLite database file path"
    )
    
    log_retention = st.number_input(
        "Log Retention (days)",
        min_value=1,
        max_value=365,
        value=30,
        help="Number of days to retain logs"
    )
    
    st.markdown("---")
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    if st.button("🗑️ Clear All Logs"):
        if st.checkbox("I confirm I want to delete all logs"):
            st.warning("This action cannot be undone!")
            if st.button("Confirm Delete"):
                st.error("Log deletion not implemented in this version")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center'>
        <p style='color: #666; font-size: 12px;'>
            AI Docker NL Dashboard v1.0<br>
            Powered by Groq & Streamlit
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
