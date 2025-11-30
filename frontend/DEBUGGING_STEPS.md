# Debugging Steps for Burn Plan Integration

## Step 1: Verify you're on the right page

1. Navigate to: `http://localhost:5173/app/burn-config`
2. You should see "🔥 Configure Your Burn" as the title
3. Make sure you're logged in (if not, you'll be redirected to login)

## Step 2: Open Browser DevTools

1. Press F12 or right-click → Inspect
2. Go to the **Console** tab
3. Clear any existing logs

## Step 3: Check Initial Logs

You should see when the page loads:
```
ApiClient initialized with baseUrl: https://colvvp9z97.execute-api.us-east-1.amazonaws.com/prod
```

If you DON'T see this, the issue is:
- Dev server not restarted after .env change
- .env file not being read

**Fix:** Stop the dev server (Ctrl+C) and restart with `npm run dev`

## Step 4: Fill Out the Form

Fill out ALL fields:
1. **Amount:** Enter a number like `1500`
2. **Timeline:** Click one of the buttons (e.g., "30 Days")
3. **Architecture:** Click one (e.g., "Serverless")
4. **Burning Style:** Click one (e.g., "Horizontal")
5. **Efficiency Level:** Move the slider (default is 5)

## Step 5: Check Button State

The "🔥 Start Burning" button should:
- Be ENABLED (not grayed out) if all fields are filled
- Be DISABLED (grayed out) if any field is missing

If the button is disabled, check which field is missing.

## Step 6: Click the Button

When you click "🔥 Start Burning", you should see in Console:
```
startBurn called
isFormValid: true
config: { totalAmount: 1500, timeline: 30, ... }
Calling createBurnPlan...
Creating burn plan with config: { ... }
Request payload: { config: { amount: "$1500", ... } }
API Request: { url: "...", method: "POST", ... }
```

## Step 7: Check Network Tab

1. Go to the **Network** tab in DevTools
2. Click "🔥 Start Burning"
3. You should see a request to `/burn-plan`
4. Click on it to see:
   - Request Headers (should include `Authorization: Bearer ...`)
   - Request Payload
   - Response

## Common Issues

### No logs at all
- Page not loaded correctly
- JavaScript error preventing execution
- Check Console for red errors

### "ApiClient initialized" but nothing when clicking button
- Button click handler not attached
- Form validation failing
- Check if button is disabled

### Logs show but no network request
- Error in apiClient
- Check for red errors in console
- Check if `config.apiBaseUrl` is empty

### Network request fails
- **401:** Not logged in or token expired
- **403:** Authorization issue
- **404:** Wrong URL
- **CORS:** Backend CORS not configured
- **500:** Backend error

## Quick Test

Open the browser console and run:
```javascript
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL)
console.log('Is Authenticated:', localStorage.getItem('auth_token') !== null)
```

This will tell you if the environment variables are loaded and if you're logged in.
