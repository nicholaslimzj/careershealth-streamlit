# Authentication Setup for Render Deployment

## Quick Setup (5 minutes)

Your Streamlit app now has built-in password protection using `streamlit-authenticator`.

### 1. Set Environment Variables on Render

In your Render dashboard, add these environment variables:

```
APP_USERNAME=your_username
APP_PASSWORD=your_secure_password
```

### 2. Deploy

The app will automatically install the authentication dependency and show a login screen.

### 3. Access

- **Username**: What you set in `APP_USERNAME`
- **Password**: What you set in `APP_PASSWORD`
- **Session**: 30 days (users stay logged in)

## Features

✅ **Simple login form** - Username/password fields  
✅ **Session management** - Users stay logged in for 30 days  
✅ **Logout button** - Available in the sidebar  
✅ **Secure password hashing** - Passwords are hashed, not stored in plain text  
✅ **Environment variable config** - Easy to change credentials  

## Security Notes

- Passwords are hashed using bcrypt
- Sessions are stored in browser cookies
- No database required - everything is in-memory
- Perfect for single-user or small team access

## Alternative Options

If you need more advanced authentication:

1. **Cloudflare Access** - Add authentication layer in front of your app
2. **Auth0** - Enterprise-grade authentication service
3. **Custom OAuth** - Integrate with Google, GitHub, etc.

But for most use cases, the built-in authentication is perfect and the fastest to deploy! 