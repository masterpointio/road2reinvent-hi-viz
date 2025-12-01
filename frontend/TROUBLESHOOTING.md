# Troubleshooting Guide

## redirect_mismatch Error

This error occurs when the callback URL your app is using doesn't match what's configured in Cognito.

### Quick Fix

1. **Find your callback URL:**
   - Open `frontend/check-callback-url.html` in your browser
   - Or manually construct it: `http://localhost:5173/login-callback` (for local dev)

2. **Add it to Cognito:**
   - AWS Console → Cognito → Your User Pool
   - App Integration → App clients → Your app client
   - Hosted UI settings → Allowed callback URLs
   - Add: `http://localhost:5173/login-callback`
   - Save changes

3. **For production:**
   - Also add: `https://yourdomain.com/login-callback`

### What URLs to Add

Add ALL of these to Cognito (comma-separated):
```
http://localhost:5173/login-callback,
http://localhost:3000/login-callback,
https://yourdomain.com/login-callback
```

### Verify Configuration

Check your `.env` file has:
```bash
VITE_COGNITO_DOMAIN=r2r-auth-114713347049.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=69fd6e78jd23pctos94qbq4uqr
```

### Debug the Login URL

Open browser console and check what URL is being generated:
```javascript
console.log(window.location.origin + '/login-callback')
```

This should match exactly what's in Cognito.

## Other Common Issues

### "Configuration missing" error
- Check `.env` file exists in `frontend/` directory
- Verify `VITE_COGNITO_DOMAIN` and `VITE_COGNITO_CLIENT_ID` are set
- Restart dev server after changing `.env`

### "Token exchange failed"
- Verify Cognito domain is correct (no `https://` prefix)
- Check client ID is correct
- Ensure app client has "Authorization code grant" enabled

### "API request failed"
- Add `VITE_API_BASE_URL` to `.env`
- Get URL from: `cdk deploy` output
- Should end with `/prod/` or `/prod`

### CORS errors
- Backend needs to allow your frontend origin
- Check FastAPI CORS middleware configuration
- For local dev, backend should allow `http://localhost:5173`

## Testing Checklist

- [ ] Callback URL added to Cognito
- [ ] `.env` file configured
- [ ] Dev server restarted after `.env` changes
- [ ] Browser cache cleared
- [ ] Cognito app client has "Authorization code grant" enabled
- [ ] API URL configured in `.env`

## Still Having Issues?

1. Check browser console for errors
2. Check network tab for failed requests
3. Verify Cognito configuration in AWS Console
4. Try in incognito/private browsing mode
5. Clear localStorage: `localStorage.clear()`
