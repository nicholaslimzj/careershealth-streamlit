import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Google Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    # Password protection
    st.markdown("""
    <style>
        .auth-container {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin: 2rem auto;
            max-width: 400px;
        }
        .auth-title {
            color: #1f77b4;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Get password from environment variable (more secure than hardcoding)
    app_password = os.getenv('APP_PASSWORD', '')
    
    # Only show password protection if APP_PASSWORD is set
    if app_password and not st.session_state.authenticated:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="auth-title">🔐 Google Analytics Dashboard</h2>', unsafe_allow_html=True)
        st.markdown('**Please enter the password to access the dashboard**')
        
        # Password input
        password = st.text_input("Password", type="password", key="password_input")
        
        if st.button("Login", type="primary"):
            if password == app_password:
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # If authenticated, show logout button in sidebar
    if app_password and st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    # Header
    st.markdown('<h1 class="main-header">📊 Google Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # Property ID input
    property_id = st.sidebar.text_input(
        "Google Analytics Property ID",
        value=os.getenv('GA_PROPERTY_ID', ''),
        help="Enter your GA4 property ID (e.g., 123456789)"
    )
    
    # Date range selection
    st.sidebar.subheader("Date Range")
    date_range = st.sidebar.selectbox(
        "Select Date Range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
        index=1
    )
    
    if date_range == "Custom":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
    else:
        days_map = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90
        }
        days = days_map[date_range]
        end_date = datetime.now().date()
        start_date = (datetime.now() - timedelta(days=days)).date()
    
    # Convert dates to string format for GA API
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Display selected date range
    st.sidebar.info(f"📅 Date Range: {start_date_str} to {end_date_str}")
    
    # Initialize GA client
    if not property_id:
        st.warning("⚠️ Please enter your Google Analytics Property ID in the sidebar to get started.")
        st.info("""
        **Setup Instructions:**
        1. Get your GA4 Property ID from Google Analytics
        2. Set up a service account and download credentials
        3. Add credentials to environment variables
        4. Deploy to Render.com
        """)
        return
    
    client = initialize_ga_client()
    if not client:
        st.error("❌ Failed to initialize Google Analytics client. Please check your credentials.")
        return
    
    # Main dashboard
    if st.button("🔄 Refresh Data", type="primary"):
        with st.spinner("Fetching data from Google Analytics..."):
            # Basic metrics
            basic_metrics = [
                Metric(name="totalUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate")
            ]
            
            basic_response = get_ga_data(
                client, property_id, start_date_str, end_date_str,
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
                    client, property_id, start_date_str, end_date_str,
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
                    client, property_id, start_date_str, end_date_str,
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
                    client, property_id, start_date_str, end_date_str,
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
                
                # Page drop-off analysis
                st.subheader("📉 Page Drop-off Analysis")
                
                # Get pages with exit rate data
                dropoff_response = get_ga_data(
                    client, property_id, start_date_str, end_date_str,
                    dimensions=[Dimension(name="pagePath")],
                    metrics=[
                        Metric(name="screenPageViews"),
                        Metric(name="totalUsers"),
                        Metric(name="exits"),
                        Metric(name="sessions")
                    ],
                    row_limit=15
                )
                
                if dropoff_response and dropoff_response.rows:
                    dropoff_data = []
                    for row in dropoff_response.rows:
                        page_views = int(row.metric_values[0].value)
                        users = int(row.metric_values[1].value)
                        exits = int(row.metric_values[2].value)
                        sessions = int(row.metric_values[3].value)
                        
                        # Calculate exit rate (drop-off rate)
                        exit_rate = (exits / page_views * 100) if page_views > 0 else 0
                        
                        dropoff_data.append({
                            'Page': row.dimension_values[0].value,
                            'Page Views': page_views,
                            'Users': users,
                            'Exits': exits,
                            'Exit Rate (%)': round(exit_rate, 1),
                            'Sessions': sessions
                        })
                    
                    df_dropoff = pd.DataFrame(dropoff_data)
                    
                    # Sort by exit rate (highest drop-off first)
                    df_dropoff = df_dropoff.sort_values('Exit Rate (%)', ascending=False)
                    
                    # Create bar chart for exit rates
                    fig = px.bar(df_dropoff.head(10), x='Exit Rate (%)', y='Page',
                                title='Top 10 Pages by Exit Rate (Drop-off)',
                                orientation='h',
                                color='Exit Rate (%)',
                                color_continuous_scale='Reds')
                    fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display detailed table
                    st.dataframe(df_dropoff, use_container_width=True)
                    
                    # Summary insights
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_exit_rate = df_dropoff['Exit Rate (%)'].mean()
                        st.metric("Average Exit Rate", f"{avg_exit_rate:.1f}%")
                    
                    with col2:
                        highest_exit = df_dropoff.iloc[0]
                        st.metric("Highest Exit Rate", f"{highest_exit['Exit Rate (%)']:.1f}%", 
                                f"on {highest_exit['Page'][:30]}...")
                    
                    with col3:
                        lowest_exit = df_dropoff.iloc[-1]
                        st.metric("Lowest Exit Rate", f"{lowest_exit['Exit Rate (%)']:.1f}%",
                                f"on {lowest_exit['Page'][:30]}...")
            else:
                st.error("❌ No data returned from Google Analytics. Please check your property ID and credentials.")
    
    # Setup instructions
    with st.expander("🔧 Setup Instructions"):
        st.markdown("""
        ### Google Analytics Setup
        
        1. **Create a Google Analytics 4 Property** (if you haven't already)
        2. **Set up a Service Account:**
           - Go to [Google Cloud Console](https://console.cloud.google.com/)
           - Create a new project or select existing one
           - Enable Google Analytics Data API
           - Create a service account
           - Download the JSON credentials file
        
        3. **Add Service Account to GA4:**
           - Go to your GA4 property settings
           - Add the service account email as a user with Viewer permissions
        
        4. **Environment Variables for Render.com:**
           ```
           GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
           GA_PROPERTY_ID=your_property_id_here
           ```
        
        5. **Deploy to Render.com:**
           - Connect your GitHub repository
           - Set build command: `pip install -r requirements.txt`
           - Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
        """)

if __name__ == "__main__":
    main() 