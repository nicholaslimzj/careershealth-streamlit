# Docker Setup for Local Development

This guide will help you run the Google Analytics dashboard locally using Docker, keeping your system clean from Python dependencies.

## Prerequisites

1. **Docker** installed on your system
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows/Mac
   - [Docker Engine](https://docs.docker.com/engine/install/) for Linux

2. **Docker Compose** (usually comes with Docker Desktop)

3. **Google Analytics 4 Property ID** and **Service Account credentials** (see setup instructions below)

## Quick Start

### 1. Clone and Navigate to Project

```bash
git clone <your-repo-url>
cd careershealth-streamlit
```

### 2. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit the `.env` file with your actual credentials:

```env
# Your Google Analytics 4 Property ID
GA_PROPERTY_ID=123456789

# Your Google Service Account JSON (as a single line)
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", "project_id": "your-project", ...}
```

### 3. Build and Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up
```

### 4. Access the Application

Open your browser and go to: **http://localhost:8501**

## Alternative: Direct Docker Commands

If you prefer not to use Docker Compose:

```bash
# Build the image
docker build -t ga-dashboard .

# Run the container
docker run -p 8501:8501 --env-file .env ga-dashboard
```

## Google Analytics Setup (Required)

Before running the app, you need to set up Google Analytics access:

### Step 1: Get Your Property ID

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your GA4 property
3. Go to **Admin** → **Property Settings**
4. Copy the **Property ID** (e.g., `123456789`)

### Step 2: Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Analytics Data API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create a new service account
6. Download the JSON credentials file

### Step 3: Add Service Account to GA4

1. In your GA4 property, go to **Admin** → **Property Access Management**
2. Add the service account email with **Viewer** permissions

### Step 4: Configure .env File

1. Copy your Property ID to `GA_PROPERTY_ID`
2. Copy the entire JSON file content to `GOOGLE_APPLICATION_CREDENTIALS_JSON` (as a single line)

## Development Workflow

### Making Changes

Since we mount the app directory as a volume, you can edit files locally and see changes:

```bash
# Start the app
docker-compose up

# Edit app.py in your local editor
# Changes will be reflected automatically (Streamlit auto-reloads)
```

### Rebuilding After Dependency Changes

If you modify `requirements.txt`:

```bash
# Stop the app
docker-compose down

# Rebuild with new dependencies
docker-compose build --no-cache

# Start again
docker-compose up
```

### Viewing Logs

```bash
# View logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f streamlit-app
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8501
lsof -i :8501

# Or use a different port
docker-compose up -p 8502:8501
```

#### 2. Permission Issues (Linux)
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### 3. Environment Variables Not Loading
```bash
# Check if .env file exists and has correct format
cat .env

# Verify variables are loaded
docker-compose config
```

#### 4. Google Analytics Authentication Errors
- Verify your Property ID is correct
- Check that service account JSON is properly formatted
- Ensure service account has access to GA4 property
- Verify Google Analytics Data API is enabled

### Debugging

#### Access Container Shell
```bash
# Get container ID
docker ps

# Access shell
docker exec -it <container_id> /bin/bash
```

#### Check Environment Variables in Container
```bash
docker exec -it <container_id> env | grep GA
```

## Production Considerations

For production deployment, consider:

1. **Remove volume mount** from docker-compose.yml
2. **Use multi-stage builds** for smaller images
3. **Add health checks** (already included)
4. **Configure proper logging**
5. **Use secrets management** for credentials

## Commands Reference

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Rebuild images
docker-compose build

# View logs
docker-compose logs

# Restart services
docker-compose restart

# Remove containers and volumes
docker-compose down -v

# Clean up unused images
docker system prune
```

## Next Steps

Once you have the app running locally:

1. **Test with your GA4 data**
2. **Customize the dashboard** as needed
3. **Deploy to Render.com** when ready (see main README.md)

The Docker setup ensures a clean, reproducible environment for development! 