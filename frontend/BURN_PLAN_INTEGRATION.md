# Burn Plan API Integration

## Overview

The frontend now calls the `/api/burn-plan` endpoint with Cognito authentication to generate burn plans.

## What Was Changed

### 1. Updated `useBurnPlan.ts` Composable

**Location:** `frontend/src/composables/useBurnPlan.ts`

**Changes:**
- Fixed request payload to match backend API contract
- Maps frontend `efficiencyLevel` (1-10) to backend `stupidity` levels
- Properly formats the amount as `$1000` string
- Transforms backend response to frontend format
- Added comprehensive error handling for different HTTP status codes
- Uses `apiClient` which automatically includes `Authorization: Bearer <token>` header

**Request Format:**
```typescript
{
  config: {
    amount: "$1500",           // String with $ prefix
    timeline: 30,              // Number of days
    architecture: "serverless", // Literal type
    burning_style: "horizontal", // Literal type
    stupidity: "Moderately stupid" // Mapped from efficiencyLevel
  }
}
```

**Response Format:**
```typescript
{
  session_id: "uuid",
  burn_plan: {
    total_amount: "$1500",
    timeline_days: 30,
    efficiency_level: "Moderately stupid",
    services_deployed: [...],
    total_calculated_cost: 1500.00,
    deployment_scenario: "...",
    key_mistakes: [...],
    recommendations: [...]
  }
}
```

### 2. Updated `BurnConfigurationView.vue`

**Location:** `frontend/src/views/BurnConfigurationView.vue`

**Changes:**
- Fixed type casting for architecture and burningStyle
- Added loading state to buttons
- Shows "Generating..." text while API call is in progress
- Disables buttons during loading

### 3. Authentication Flow

The authentication is handled automatically:

1. **Login:** User authenticates via Cognito hosted UI
2. **Token Storage:** Access token stored in localStorage
3. **API Calls:** `apiClient` reads token and adds to headers:
   ```typescript
   headers['Authorization'] = `Bearer ${accessToken.value}`
   ```
4. **Backend Validation:** Lambda authorizer validates token against Cognito User Pool

## API Client Architecture

```
BurnConfigurationView
    ↓
useBurnPlan.createBurnPlan()
    ↓
apiClient.post('/burn-plan', payload)
    ↓
getHeaders() → adds Authorization header
    ↓
fetch(API_BASE_URL + '/burn-plan', { headers, body })
    ↓
Backend Lambda (with Cognito authorizer)
```

## Error Handling

The composable provides user-friendly error messages:

- **401/403:** "Authentication failed. Please log in again."
- **429:** "Rate limit exceeded. Please try again later."
- **504:** "Request timed out. The agent is taking too long to respond."
- **502/503:** "Service temporarily unavailable. Please try again."
- **Other:** Generic error message from API

## Testing

### Prerequisites
1. Set `VITE_API_BASE_URL` in `frontend/.env`
2. Deploy backend with `cdk deploy`
3. Ensure Cognito is configured

### Test Steps
1. Log in to the app
2. Navigate to "Configure Burn"
3. Fill out the form:
   - Amount: $1500
   - Timeline: 30 days
   - Architecture: Serverless
   - Style: Horizontal
   - Efficiency: 5 (Moderately stupid)
4. Click "Start Burning"
5. Check Network tab for API call
6. Verify redirect to results page

### Expected Network Request

**URL:** `https://your-api.execute-api.us-east-1.amazonaws.com/prod/burn-plan`

**Method:** POST

**Headers:**
```
Authorization: Bearer eyJraWQ...
Content-Type: application/json
```

**Body:**
```json
{
  "config": {
    "amount": "$1500",
    "timeline": 30,
    "architecture": "serverless",
    "burning_style": "horizontal",
    "stupidity": "Moderately stupid"
  }
}
```

## Efficiency Level Mapping

| Frontend Level | Backend Stupidity |
|---------------|-------------------|
| 1-2           | Mildly dumb       |
| 3-5           | Moderately stupid |
| 6-8           | Very stupid       |
| 9-10          | Brain damage      |

## Next Steps

1. **Set API URL:** Update `frontend/.env` with your API Gateway URL
2. **Test Integration:** Follow testing steps above
3. **Monitor Logs:** Check CloudWatch logs for any backend errors
4. **Handle Edge Cases:** Test with various amounts and timelines

## Troubleshooting

See `API_SETUP.md` for detailed troubleshooting guide.
