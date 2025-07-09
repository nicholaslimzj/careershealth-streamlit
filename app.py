import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt, timedelta
import os
import time
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression
)
from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json
import streamlit_authenticator as stauth

# Load environment variables
load_dotenv()

# Authentication setup
def setup_authentication():
    """Setup authentication with username and password from environment variables"""
    username = os.getenv('APP_USERNAME', 'admin')
    password = os.getenv('APP_PASSWORD', 'password123')
    
    # Create credentials dictionary in the new format
    credentials = {
        'usernames': {
            username: {
                'name': 'Admin',
                'password': password
            }
        }
    }
    
    # Create authenticator
    authenticator = stauth.Authenticate(
        credentials,
        'career_health_dashboard',
        'auth_key',
        cookie_expiry_days=30
    )
    
    return authenticator

# Page configuration
st.set_page_config(
    page_title="Career Health SG - Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the deploy button and menu
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    /* Ensure sidebar is always visible */
    .css-1d391kg {display: block !important;}
    .css-1lcbmhc {display: block !important;}
</style>
""", unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    @media (max-width: 600px) {
        .metric-card {
            margin-bottom: 1rem;
        }
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    /* Ensure sidebar is visible */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
    .css-1d391kg {
        display: block !important;
        visibility: visible !important;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
    }
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stDateInput > div > div > input {
        border-radius: 8px;
    }
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    .stPlotlyChart {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

def initialize_ga_client():
    """Initialize Google Analytics client with service account credentials"""
    try:
        # Check if service account key is provided via environment variable
        service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if service_account_info:
            # Parse the JSON string from environment variable
            credentials_info = json.loads(service_account_info)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/analytics.readonly']
            )
            return BetaAnalyticsDataClient(credentials=credentials)
        else:
            # Fallback to default credentials (for local development)
            credentials, project = default(scopes=['https://www.googleapis.com/auth/analytics.readonly'])
            return BetaAnalyticsDataClient(credentials=credentials)
    except Exception as e:
        st.error(f"Error initializing GA client: {str(e)}")
        return None

def get_ga_data(client, property_id, start_date, end_date, dimensions=None, metrics=None, row_limit=10):
    """Fetch data from Google Analytics"""
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=dimensions or [],
            metrics=metrics or [],
            limit=row_limit
        )
        
        response = client.run_report(request)
        return response
    except Exception as e:
        st.error(f"Error fetching GA data: {str(e)}")
        return None

def format_number(value):
    """Format numbers for display"""
    if value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return f"{value:,}"

def main():
    # Authentication
    authenticator = setup_authentication()
    authenticator.login()
    authentication_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    name = st.session_state.get("name")
    
    if authentication_status == False:
        st.error('Username/password is incorrect')
        return
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        return
    elif authentication_status:
        # Reset data fetch state after login to ensure auto-load
        st.session_state.has_fetched = False
        # Header with logo
        col_logo, col_title = st.columns([1, 8])
        with col_logo:
            st.markdown('<img src="/app/static/images/career-health-logo.png" width="120" style="display: block; margin: auto;">', unsafe_allow_html=True)
        with col_title:
            st.markdown('<h1 class="main-header">Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        ga_property_id = os.getenv('GA_PROPERTY_ID', '')
        st.subheader("Date Range")
        date_range = st.selectbox(
            "Select Date Range",
            ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
            index=1
        )
        if date_range == "Custom":
            default_start = dt.now().date()
            default_end = dt.now().date()
            picked_range = st.date_input(
                "Select Date Range",
                value=(default_start, default_end)
            )
            if isinstance(picked_range, tuple) and len(picked_range) == 2:
                start_date, end_date = picked_range
            else:
                start_date = default_start
                end_date = default_end
        else:
            days_map = {
                "Last 7 days": 7,
                "Last 30 days": 30,
                "Last 90 days": 90
            }
            days = days_map[date_range]
            end_date = dt.now().date()
            start_date = (dt.now() - timedelta(days=days)).date()
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        st.info(f"📅 Date Range: {start_date_str} to {end_date_str}")
    
    # Track last used date range in session state
    current_date_key = f"{start_date_str}_{end_date_str}"
    if 'last_date_key' not in st.session_state:
        st.session_state.last_date_key = current_date_key
    if st.session_state.last_date_key != current_date_key:
        st.session_state.has_fetched = False
        st.session_state.last_date_key = current_date_key

    # Ensure session state variable is initialized
    if 'has_fetched' not in st.session_state:
        st.session_state.has_fetched = False
    
    # Initialize GA client
    if not ga_property_id:
        st.warning("⚠️ Please enter your Google Analytics Property ID in the sidebar to get started.")
        return
    
    client = initialize_ga_client()
    if not client:
        st.error("❌ Failed to initialize Google Analytics client. Please check your credentials.")
        return
    
    # Manual refresh button (hidden)
    refresh_clicked = False
    
    # Main dashboard logic
    if not st.session_state.has_fetched or refresh_clicked:
        with st.spinner("Fetching data from Google Analytics..."):
            st.session_state.has_fetched = True
            st.session_state.last_refresh = time.time()
            # Basic metrics
            basic_metrics = [
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate")
            ]
            
            basic_response = get_ga_data(
                client, ga_property_id, start_date_str, end_date_str,
                metrics=basic_metrics
            )
            
            if basic_response and basic_response.rows:
                row = basic_response.rows[0]
                
                # Display basic metrics in cards
                st.subheader("📊 Key Metrics Overview")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{format_number(int(row.metric_values[1].value))}</div>
                        <div class="metric-label">Total Visits (Sessions)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{format_number(int(row.metric_values[0].value))}</div>
                        <div class="metric-label">Unique Visitors</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{format_number(int(row.metric_values[2].value))}</div>
                        <div class="metric-label">Total Page Views</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    avg_duration = float(row.metric_values[3].value)
                    minutes = int(avg_duration // 60)
                    seconds = int(avg_duration % 60)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{minutes}m {seconds}s</div>
                        <div class="metric-label">Avg Session Duration</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    bounce_rate = float(row.metric_values[4].value) * 100
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{bounce_rate:.1f}%</div>
                        <div class="metric-label">Bounce Rate</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Time series data
                st.subheader("📈 Traffic Over Time")
                
                time_series_response = get_ga_data(
                    client, ga_property_id, start_date_str, end_date_str,
                    dimensions=[Dimension(name="date")],
                    metrics=[Metric(name="totalUsers"), Metric(name="sessions")],
                    row_limit=100
                )
                
                if time_series_response and time_series_response.rows:
                    dates = []
                    users = []
                    sessions = []
                    
                    for row in time_series_response.rows:
                        dates.append(row.dimension_values[0].value)
                        users.append(int(row.metric_values[0].value))
                        sessions.append(int(row.metric_values[1].value))
                    
                    # Create time series chart
                    df_time = pd.DataFrame({
                        'Date': pd.to_datetime(dates),
                        'Users': users,
                        'Sessions': sessions
                    })
                    
                    fig = px.line(df_time, x='Date', y=['Users', 'Sessions'],
                                title='Daily Traffic',
                                labels={'value': 'Count', 'variable': 'Metric'})
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Top pages
                st.subheader("📄 Top Pages")
                
                pages_response = get_ga_data(
                    client, ga_property_id, start_date_str, end_date_str,
                    dimensions=[Dimension(name="pagePath")],
                    metrics=[Metric(name="screenPageViews"), Metric(name="totalUsers")],
                    row_limit=10
                )
                
                if pages_response and pages_response.rows:
                    pages_data = []
                    for row in pages_response.rows:
                        pages_data.append({
                            'Page': row.dimension_values[0].value,
                            'Page Views': int(row.metric_values[0].value),
                            'Users': int(row.metric_values[1].value)
                        })
                    
                    df_pages = pd.DataFrame(pages_data)
                    st.dataframe(df_pages, use_container_width=True)
                
                # Traffic sources
                st.subheader("🌐 Traffic Sources")
                
                sources_response = get_ga_data(
                    client, ga_property_id, start_date_str, end_date_str,
                    dimensions=[Dimension(name="sessionDefaultChannelGrouping")],
                    metrics=[Metric(name="sessions"), Metric(name="totalUsers")],
                    row_limit=10
                )
                
                if sources_response and sources_response.rows:
                    sources_data = []
                    for row in sources_response.rows:
                        sources_data.append({
                            'Source': row.dimension_values[0].value,
                            'Sessions': int(row.metric_values[0].value),
                            'Users': int(row.metric_values[1].value)
                        })
                    
                    df_sources = pd.DataFrame(sources_data)
                    
                    # Create pie chart for traffic sources
                    fig = px.pie(df_sources, values='Sessions', names='Source',
                                title='Traffic by Source')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display as table
                    st.dataframe(df_sources, use_container_width=True)
            else:
                st.error("❌ No data returned from Google Analytics. Please check your property ID and credentials.")
        
        # Add logout button in sidebar
        with st.sidebar:
            st.divider()
            authenticator.logout('Logout', 'sidebar')

if __name__ == "__main__":
    main() 