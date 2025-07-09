# Detailed Setup Instructions

## Google Analytics 4 Setup

### Step 1: Get Your Property ID

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your GA4 property (or create one if you don't have it)
3. Navigate to **Admin** (gear icon) → **Property Settings**
4. Copy the **Property ID** (it's a number like `123456789`)

### Step 2: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Make sure you're in the correct project (check the project selector at the top)

### Step 3: Enable Google Analytics Data API

1. In your Google Cloud project, go to **APIs & Services** → **Library**
2. Search for "Google Analytics Data API"
3. Click on it and press **Enable**

### Step 4: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Fill in the details:
   - **Service account name**: `ga-dashboard-service`
   - **Service account ID**: Will auto-generate
   - **Description**: `Service account for GA dashboard`
4. Click **Create and Continue**
5. For **Grant this service account access to project**:
   - Select **Viewer** role
   - Click **Continue**
6. Click **Done**

### Step 5: Create and Download Key

1. Click on your newly created service account
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON** format
5. Click **Create**
6. The JSON file will download automatically - **keep this safe!**

### Step 6: Add Service Account to GA4

1. Go back to your Google Analytics property
2. Navigate to **Admin** → **Property Access Management**
3. Click the **+** button
4. Add the service account email (found in the JSON file under `client_email`)
5. Give it **Viewer** permissions
6. Click **Add**

## Local Development Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Environment File

Create a `.env` file in the project root:

```env
GA_PROPERTY_ID=your_property_id_here
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", "project_id": "your-project", "private_key_id": "...", "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n", "client_email": "your-service-account@your-project.iam.gserviceaccount.com", "client_id": "...", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}
```

**Important**: Copy the entire contents of your downloaded JSON file as a single line for the `GOOGLE_APPLICATION_CREDENTIALS_JSON` value.

### Step 3: Run Locally

```bash
streamlit run app.py
```

## Render.com Deployment

### Step 1: Prepare Your Repository

1. Initialize git if not already done:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a GitHub repository and push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [Render.com](https://render.com/) and sign up/login
2. Click **New +** → **Web Service**
3. Connect your GitHub account and select your repository
4. Configure the service:
   - **Name**: `ga-dashboard` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: Free (or paid if you need more resources)

### Step 3: Set Environment Variables

1. In your Render service dashboard, go to **Environment**
2. Add these environment variables:
   - **Key**: `GA_PROPERTY_ID`
     **Value**: Your GA4 Property ID (e.g., `123456789`)
   
   - **Key**: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
     **Value**: Your entire service account JSON as a single line

### Step 4: Deploy

1. Click **Create Web Service**
2. Wait for the build to complete (usually 2-5 minutes)
3. Your app will be available at the provided URL

## Troubleshooting

### Common Issues and Solutions

#### 1. "No data returned" Error
- **Cause**: Property ID incorrect or no access
- **Solution**: 
  - Double-check your Property ID
  - Verify service account email is added to GA4 with Viewer permissions
  - Ensure your GA4 property has data (new properties take 24-48 hours)

#### 2. Authentication Errors
- **Cause**: Incorrect service account setup
- **Solution**:
  - Verify JSON credentials are correctly formatted
  - Check that Google Analytics Data API is enabled
  - Ensure service account has proper permissions

#### 3. Render Build Fails
- **Cause**: Missing dependencies or incorrect configuration
- **Solution**:
  - Check that `requirements.txt` is in the root directory
  - Verify all environment variables are set
  - Check the build logs for specific errors

#### 4. App Won't Start on Render
- **Cause**: Incorrect start command or port configuration
- **Solution**:
  - Ensure start command includes `--server.port $PORT --server.address 0.0.0.0`
  - Check that `app.py` is in the root directory

### Testing Your Setup

1. **Local Testing**: Run `streamlit run app.py` and verify it works
2. **Data Verification**: Check that your GA4 property has recent data
3. **API Access**: Verify service account can access your GA4 property
4. **Render Deployment**: Test the deployed app with your GA4 data

### Security Notes

- Never commit your `.env` file or service account JSON to git
- Use environment variables for all sensitive data
- Regularly rotate your service account keys
- Monitor your Google Cloud API usage

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all setup steps were completed correctly
3. Check the app's built-in setup instructions
4. Review Google Cloud Console logs for API errors 