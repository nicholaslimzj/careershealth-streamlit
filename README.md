# Google Analytics Dashboard with Streamlit

A beautiful and interactive dashboard to visualize your Google Analytics 4 data, built with Streamlit and ready for deployment on Render.com.

## Features

- 📊 **Key Metrics Display**: 
  - Total Visits (Sessions)
  - Unique Visitors
  - Total Page Views
  - Average Session Duration
  - Bounce Rate
- 📈 **Time Series Charts**: Visualize traffic trends over time
- 📄 **Top Pages Analysis**: See your most popular pages
- 🌐 **Traffic Sources**: Understand where your traffic comes from (social, ads, search, referral, direct)
- 📉 **Page Drop-off Analysis**: Identify which pages have the highest exit rates
- 📱 **Responsive Design**: Works great on desktop and mobile
- 🔄 **Real-time Data**: Pull fresh data from Google Analytics API
- 🎨 **Beautiful UI**: Modern, clean interface with custom styling

## Quick Start

### Option 1: Docker (Recommended for Local Development)

#### Quick Start (Automatic)
```bash
# Clone the repository
git clone <your-repo-url>
cd careershealth-streamlit

# Run the quick start script
./start.sh          # Linux/Mac
# OR
start.bat           # Windows
```

#### Manual Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd careershealth-streamlit

# Copy and configure environment variables
cp env.example .env
# Edit .env with your GA4 credentials

# Build and run with Docker
docker-compose build
docker-compose up
```

**Access the app at:** http://localhost:8501

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker instructions.

### Option 2: Local Python Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd careershealth-streamlit
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Analytics

#### Step 1: Get Your GA4 Property ID
1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your GA4 property
3. Go to Admin → Property Settings
4. Copy the Property ID (format: 123456789)

#### Step 2: Create a Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Analytics Data API**
4. Go to IAM & Admin → Service Accounts
5. Create a new service account
6. Download the JSON credentials file

#### Step 3: Add Service Account to GA4
1. In your GA4 property, go to Admin → Property Access Management
2. Add the service account email as a user with **Viewer** permissions

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GA_PROPERTY_ID=your_property_id_here
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
```

**Note**: For the `GOOGLE_APPLICATION_CREDENTIALS_JSON`, copy the entire contents of your downloaded JSON file as a single line.

### 5. Run Locally

```bash
streamlit run app.py
```

## Deployment on Render.com

### Quick Deploy (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Deploy using render.yaml**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will auto-configure using `render.yaml`
   - Enter your environment variables when prompted

### Manual Deploy

1. Go to [Render.com](https://render.com/) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `ga-dashboard` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

5. **Set Environment Variables** in Render dashboard:
   - `GA_PROPERTY_ID`: Your Google Analytics Property ID
   - `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Your service account JSON (as a single line)

6. Click "Create Web Service" and wait for deployment.

**See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.**

## Usage

1. **Enter Property ID**: Input your GA4 Property ID in the sidebar
2. **Select Date Range**: Choose from predefined ranges or set custom dates
3. **Refresh Data**: Click the "Refresh Data" button to fetch latest metrics
4. **Explore**: View different sections like traffic trends, top pages, and traffic sources

## Project Structure

```
careershealth-streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker build exclusions
├── env.example           # Example environment variables
├── render.yaml           # Render.com deployment configuration
├── README.md             # This file
├── DOCKER_SETUP.md       # Docker setup instructions
├── RENDER_DEPLOYMENT.md  # Render deployment guide
├── METRICS_SUMMARY.md    # Detailed metrics breakdown
├── setup_instructions.md # Google Analytics setup guide
├── start.sh              # Quick start script (Linux/Mac)
└── .env                  # Environment variables (create from env.example)
```

## Dependencies

- **streamlit**: Web app framework
- **google-analytics-data**: Google Analytics Data API client
- **google-auth**: Google authentication
- **pandas**: Data manipulation
- **plotly**: Interactive charts
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **"No data returned" error**
   - Check your Property ID is correct
   - Verify service account has access to GA4 property
   - Ensure Google Analytics Data API is enabled

2. **Authentication errors**
   - Verify your service account JSON is correctly formatted
   - Check that the service account email is added to GA4 with Viewer permissions

3. **Render deployment fails**
   - Ensure all environment variables are set
   - Check that the start command includes the port configuration

### Getting Help

- Check the setup instructions in the app's expandable section
- Verify your Google Cloud Console project has the Analytics Data API enabled
- Ensure your GA4 property has data (new properties might take 24-48 hours to show data)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE). 