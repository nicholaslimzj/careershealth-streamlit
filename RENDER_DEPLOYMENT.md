# Deploy to Render.com

This guide will walk you through deploying your Google Analytics dashboard to Render.com's free tier.

## Prerequisites

1. **GitHub Repository**: Your code should be pushed to a GitHub repository
2. **Google Analytics Setup**: You should have completed the GA4 setup (see `setup_instructions.md`)
3. **Render Account**: Sign up at [render.com](https://render.com)

## Deployment Options

### Option 1: Using render.yaml (Recommended)

The `render.yaml` file in this repository will automatically configure your service and prompt for environment variables during deployment.

### Option 2: Manual Configuration

If you prefer to configure manually, follow the steps below.

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

```bash
# If you haven't already
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Deploy on Render

#### Using render.yaml (Automatic Configuration)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select the repository containing your code
5. Render will detect the `render.yaml` file and configure the service automatically
6. You'll be prompted to enter the required environment variables:
   - **GA_PROPERTY_ID**: Your GA4 Property ID
   - **GOOGLE_APPLICATION_CREDENTIALS_JSON**: Your service account JSON (as a single line)
7. Click **"Apply"** to start the deployment

#### Manual Configuration

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `ga-dashboard` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
   - **Plan**: Free

### 3. Set Environment Variables

#### During Initial Deployment (render.yaml method)
- You'll be prompted to enter the variables when you first deploy
- The `GOOGLE_APPLICATION_CREDENTIALS_JSON` will be marked as a secret

#### After Deployment (Manual method)
1. In your Render service dashboard, go to **"Environment"**
2. Add these environment variables:

   **GA_PROPERTY_ID**
   - **Key**: `GA_PROPERTY_ID`
   - **Value**: Your GA4 Property ID (e.g., `123456789`)
   - **Type**: Plain Text

   **GOOGLE_APPLICATION_CREDENTIALS_JSON**
   - **Key**: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value**: Your entire service account JSON as a single line
   - **Type**: Secret

### 4. Deploy

Click **"Create Web Service"** and wait for the deployment to complete (usually 2-5 minutes).

## Environment Variables Setup

### Getting Your Values

#### GA_PROPERTY_ID
1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your GA4 property
3. Go to **Admin** → **Property Settings**
4. Copy the **Property ID** (e.g., `123456789`)

#### GOOGLE_APPLICATION_CREDENTIALS_JSON
1. Open your downloaded service account JSON file
2. Copy the **entire content** as a single line
3. Example format:
   ```json
   {"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"your-service-account@your-project.iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}
   ```

### Important Notes

- **Single Line**: The JSON must be on a single line with no line breaks
- **Secret Variable**: The credentials JSON is marked as a secret for security
- **No Quotes**: Don't add extra quotes around the values in Render
- **Validation**: Render will validate the JSON format

## Post-Deployment

### 1. Access Your App

Your app will be available at: `https://your-app-name.onrender.com`

### 2. Test the Dashboard

1. Open your deployed app
2. Enter your GA4 Property ID in the sidebar
3. Click "Refresh Data" to test the connection
4. Verify all metrics are loading correctly

### 3. Monitor Logs

- Go to your Render service dashboard
- Click on **"Logs"** to monitor the application
- Check for any errors or issues

## Troubleshooting

### Common Issues

#### 1. Build Fails
- Check that `requirements.txt` is in the root directory
- Verify all dependencies are listed correctly
- Check build logs for specific errors

#### 2. App Won't Start
- Verify the start command includes port configuration
- Check that `app.py` is in the root directory
- Review startup logs for errors

#### 3. Environment Variables Not Working
- Verify variables are set correctly in Render dashboard
- Check that JSON is properly formatted (single line)
- Ensure Property ID is correct

#### 4. Google Analytics Authentication Errors
- Verify service account has access to GA4 property
- Check that Google Analytics Data API is enabled
- Ensure Property ID matches your GA4 property

### Debugging Commands

```bash
# Check if your app is running
curl https://your-app-name.onrender.com

# Check environment variables (if accessible)
echo $GA_PROPERTY_ID
echo $GOOGLE_APPLICATION_CREDENTIALS_JSON
```

## Security Best Practices

1. **Never commit credentials** to your repository
2. **Use Render's secret variables** for sensitive data
3. **Regularly rotate** your service account keys
4. **Monitor API usage** in Google Cloud Console
5. **Use least privilege** for service account permissions

## Scaling Considerations

- **Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: Always-on, more resources, custom domains
- **Auto-scaling**: Available on paid plans

## Next Steps

After successful deployment:

1. **Set up monitoring** for your app
2. **Configure alerts** for downtime
3. **Set up custom domain** (optional)
4. **Monitor costs** if using paid plans
5. **Regular updates** of dependencies

Your Google Analytics dashboard is now live and accessible from anywhere! 