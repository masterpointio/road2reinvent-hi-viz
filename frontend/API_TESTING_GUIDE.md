# API Testing Guide

## ✅ Current Implementation

The frontend is **already configured** to call the real API endpoint with authentication!

### What's Implemented:

1. **API Client** (`src/lib/apiClient.ts`)
   - Automatically includes `Authorization: Bearer <token>` header
   - Uses access token from `useAuth` composable
   - Handles errors with proper status codes

2. **Burn Plan Creation** (`src/views/BurnConfigurationView.vue`)
   - Calls `POST /api/burn-plan` with configuration
   - Sends authenticated request with token
   - Stores response in sessionStorage for results page

3. **Request Format:**
```json
{
  "config": {
    "amount": "1500",
    "timeline": 30,
    "architecture": "serverless",
    "burning_style": "horizontal",
    "stupidity": "Moderately stupid"
  }
}
```

4. **Expected Response Format:**
```json
{
  "burn_plan": {
    "total_amount": "$1,500",
    "timeline_days": 30,
    "efficiency_level": "Moderately stupid",
    "services_deployed": [
      {
        "service_name": "Lambda",
        "instance_type": "1024MB",
        "quantity": 100,
        "start_day": 1,
        "end_day": 30,
        "duration_used": "30 days",
        "unit_cost": 0.0000166667,
        "total_cost": 500.00,
        "usage_pattern": "24/7",
        "waste_factor": "Over-provisioned memory",
        "roast": "1024MB for hello world? Really?"
      }
    ],
    "total_calculated_cost": 1500.00,
    "deployment_scenario": "A serverless nightmare...",
    "key_mistakes": ["Mistake 1", "Mistake 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "roast": "Overall roast message"
  }
}
```

## 🧪 Testing Steps

### 1. Check Environment Variables
```bash
# In frontend/.env
VITE_API_BASE_URL=https://your-api.execute-api.us-east-1.amazonaws.com
VITE_COGNITO_DOMAIN=your-domain.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
```

### 2. Start Development Server
```bash
cd frontend
npm run dev
```

### 3. Test the Flow

1. **Login**
   - Visit `http://localhost:5173`
   - Click "Sign In"
   - Authenticate with Cognito
   - Should redirect to `/app`

2. **Create Burn Plan**
   - Fill out the form:
     - Amount: $1500
     - Timeline: 30 days
     - Architecture: Serverless
     - Burning Style: Horizontal
     - Stupidity: 5 (Moderately stupid)
   - Click "Start Burning"

3. **Check Network Tab**
   - Open browser DevTools → Network tab
   - Look for `POST /api/burn-plan` request
   - Verify headers include: `Authorization: Bearer <token>`
   - Check response status and data

4. **View Results**
   - Should redirect to `/app/burn-results`
   - Charts should display with real data
   - Progress meter should animate

## 🔍 Debugging

### Check Auth Token
```javascript
// In browser console
localStorage.getItem('auth_access_token')
```

### Check API Request
```javascript
// In browser console on burn-config page
// After filling form, check what will be sent:
console.log({
  amount: document.querySelector('input[type="number"]').value,
  timeline: 30, // selected timeline
  architecture: 'serverless', // selected architecture
  burning_style: 'horizontal', // selected style
  stupidity: 'Moderately stupid' // based on slider
});
```

### Check Stored Response
```javascript
// In browser console on burn-results page
JSON.parse(sessionStorage.getItem('currentBurnPlan'))
```

## 🐛 Common Issues

### 1. **401 Unauthorized**
- Token expired or invalid
- Solution: Log out and log back in

### 2. **CORS Error**
- API not configured for frontend origin
- Solution: Add CORS headers to API Gateway

### 3. **504 Gateway Timeout**
- Agent taking too long to respond
- Solution: Increase Lambda timeout or optimize agent

### 4. **No data in results**
- Response format mismatch
- Solution: Check console for errors, verify response structure

## 📊 Expected Behavior

### Success Flow:
1. Form submission → Loading state
2. API call with auth token
3. Response received (2-10 seconds)
4. Success toast: "Burn plan generated!"
5. Redirect to results page
6. Charts animate with real data

### Error Flow:
1. Form submission → Loading state
2. API call fails
3. Error toast with message
4. Stay on form page
5. User can retry

## 🔐 Security Notes

- ✅ Token automatically included in all API requests
- ✅ Token stored securely in localStorage
- ✅ Route guards prevent unauthorized access
- ✅ API validates JWT token on backend
- ✅ User-specific data returned based on token claims

## 📝 Response Mapping

The frontend expects this structure from the backend:

```typescript
interface BurnPlanResponse {
  burn_plan: {
    total_amount: string;           // "$1,500"
    timeline_days: number;          // 30
    efficiency_level: string;       // "Moderately stupid"
    services_deployed: Array<{
      service_name: string;         // "Lambda"
      instance_type?: string;       // "1024MB"
      quantity: number;             // 100
      start_day: number;            // 1
      end_day: number;              // 30
      duration_used: string;        // "30 days"
      unit_cost: number;            // 0.0000166667
      total_cost: number;           // 500.00
      usage_pattern?: string;       // "24/7"
      waste_factor?: string;        // "Over-provisioned"
      roast?: string;               // Service-specific roast
    }>;
    total_calculated_cost: number;  // 1500.00
    deployment_scenario: string;    // Narrative
    key_mistakes: string[];         // Array of mistakes
    recommendations: string[];      // Array of recommendations
    roast?: string;                 // Overall roast (optional)
  };
}
```

## ✨ Next Steps

1. **Test with real Cognito credentials**
2. **Verify API endpoint is deployed and accessible**
3. **Check API returns data in expected format**
4. **Test error scenarios** (invalid token, timeout, etc.)
5. **Monitor API logs** for any backend errors

The frontend is ready to consume real data from your API! 🚀
