# Chart Data Formats for AWS Bill Burner

This document describes the data formats needed for each chart type in the Bill Burner visualization.

## Racing Bar Chart (Primary Visualization)

The racing bar chart shows AWS services consuming money over time, with bars that animate and reorder based on cumulative spending.

### Data Format

```typescript
interface RacingBarDataPoint {
  name: string;      // Service name (e.g., "EC2 m5.24xlarge")
  value: number;     // Current cumulative cost in USD
  timestamp?: number; // Optional: Unix timestamp for this data point
}

type RacingBarData = RacingBarDataPoint[];
```

### Example Data

```json
[
  { "name": "EC2 m5.24xlarge", "value": 8500 },
  { "name": "RDS Aurora", "value": 6200 },
  { "name": "S3 Storage", "value": 4800 },
  { "name": "Lambda Invocations", "value": 3500 },
  { "name": "NAT Gateway", "value": 2100 }
]
```

### Backend Requirements

The backend should provide:
1. **Initial snapshot**: Starting values for all services (can be zeros)
2. **Updates over time**: New values at regular intervals (e.g., every 1-2 seconds)
3. **Cumulative values**: Each update should show the total spent so far, not incremental

### Update Pattern

For a 60-second burn simulation:

```json
// t=0s
[
  { "name": "EC2 m5.24xlarge", "value": 0 },
  { "name": "RDS Aurora", "value": 0 },
  { "name": "S3 Storage", "value": 0 }
]

// t=15s
[
  { "name": "EC2 m5.24xlarge", "value": 2125 },
  { "name": "RDS Aurora", "value": 1550 },
  { "name": "S3 Storage", "value": 1200 }
]

// t=30s
[
  { "name": "EC2 m5.24xlarge", "value": 4250 },
  { "name": "RDS Aurora", "value": 3100 },
  { "name": "S3 Storage", "value": 2400 }
]

// t=60s (final)
[
  { "name": "EC2 m5.24xlarge", "value": 8500 },
  { "name": "RDS Aurora", "value": 6200 },
  { "name": "S3 Storage", "value": 4800 }
]
```

---

## Line Chart (Money Remaining Over Time)

Shows the total money remaining as it burns down to zero.

### Data Format

```typescript
interface LineChartData {
  timestamps: string[];  // Time labels (e.g., ["0s", "10s", "20s", ...])
  values: number[];      // Money remaining at each timestamp
}
```

### Example Data

```json
{
  "timestamps": ["0s", "10s", "20s", "30s", "40s", "50s", "60s"],
  "values": [10000, 8500, 6800, 4200, 2500, 800, 0]
}
```

### Backend Requirements

- **Total amount**: Starting amount (e.g., $10,000)
- **Time points**: Regular intervals matching the burn duration
- **Decreasing values**: Money should monotonically decrease to zero

---

## Pie Chart (Cost Distribution by Category)

Shows how money is distributed across different AWS service categories.

### Data Format

```typescript
interface PieChartDataPoint {
  name: string;   // Category name (e.g., "Compute", "Storage")
  value: number;  // Total cost for this category in USD
}

type PieChartData = PieChartDataPoint[];
```

### Example Data

```json
[
  { "name": "Compute", "value": 3500 },
  { "name": "Storage", "value": 2800 },
  { "name": "Database", "value": 2100 },
  { "name": "Networking", "value": 1200 },
  { "name": "Other", "value": 400 }
]
```

### Backend Requirements

- **Categories**: Group services into logical categories
- **Totals**: Sum of all services in each category
- **Static data**: This doesn't need to update in real-time (calculated once from burn plan)

---

## Stacked Area Chart (Cumulative Resource Consumption)

Shows multiple services burning money simultaneously over time.

### Data Format

```typescript
interface StackedAreaData {
  timestamps: string[];  // Time labels
  series: {
    name: string;        // Service name
    data: number[];      // Cumulative cost at each timestamp
  }[];
}
```

### Example Data

```json
{
  "timestamps": ["0s", "15s", "30s", "45s", "60s"],
  "series": [
    {
      "name": "EC2",
      "data": [0, 2000, 3500, 4200, 4500]
    },
    {
      "name": "RDS",
      "data": [0, 1500, 2200, 2800, 3000]
    },
    {
      "name": "S3",
      "data": [0, 800, 1200, 1500, 1600]
    },
    {
      "name": "Lambda",
      "data": [0, 500, 800, 1000, 1100]
    }
  ]
}
```

### Backend Requirements

- **Multiple series**: One per major service
- **Aligned timestamps**: All series must have the same time points
- **Cumulative values**: Each value is the total spent so far for that service

---

## Gauge Chart (Burn Progress)

Shows overall burn completion percentage.

### Data Format

```typescript
interface GaugeData {
  value: number;      // Percentage (0-100)
  name?: string;      // Optional label (e.g., "Burn Progress")
}
```

### Example Data

```json
{
  "value": 73,
  "name": "Burn Progress"
}
```

### Backend Requirements

- **Percentage**: Calculate as `(moneyBurned / totalAmount) * 100`
- **Real-time updates**: Update as the burn progresses

---

## Burn Plan Structure (From Backend)

The backend should provide a burn plan that the frontend can use to generate all visualizations.

### Data Format

```typescript
interface BurnPlan {
  sessionId: string;
  totalAmount: number;        // Total USD to burn
  duration: number;           // Duration in seconds
  resources: Resource[];
}

interface Resource {
  service: string;            // Full service name (e.g., "EC2 m5.24xlarge")
  category: string;           // Category (e.g., "Compute", "Storage")
  cost: number;               // Total cost for this resource
  startTime: number;          // When to start (seconds from 0)
  endTime: number;            // When to stop (seconds from start)
  description: string;        // Snarky description
  costPerSecond?: number;     // Optional: pre-calculated rate
}
```

### Example Burn Plan

```json
{
  "sessionId": "abc-123-def",
  "totalAmount": 10000,
  "duration": 60,
  "resources": [
    {
      "service": "EC2 m5.24xlarge",
      "category": "Compute",
      "cost": 8500,
      "startTime": 0,
      "endTime": 60,
      "description": "Because you need 96 vCPUs to run a hello world app",
      "costPerSecond": 141.67
    },
    {
      "service": "RDS Aurora",
      "category": "Database",
      "cost": 6200,
      "startTime": 5,
      "endTime": 60,
      "description": "A database cluster for your 3 users",
      "costPerSecond": 112.73
    },
    {
      "service": "S3 Storage",
      "category": "Storage",
      "cost": 4800,
      "startTime": 0,
      "endTime": 60,
      "description": "Storing cat pictures at enterprise scale",
      "costPerSecond": 80.00
    }
  ]
}
```

---

## Frontend Calculation Logic

The frontend will:

1. **Receive the burn plan** from the backend
2. **Calculate time-series data** by:
   - Iterating through time points (e.g., every second)
   - For each time point, calculating which resources are active
   - Summing up costs based on `costPerSecond * elapsed time`
3. **Update charts** at regular intervals (e.g., 60fps for smooth animation)

### Example Calculation

```typescript
function calculateCostAtTime(resource: Resource, currentTime: number): number {
  // Resource hasn't started yet
  if (currentTime < resource.startTime) {
    return 0;
  }
  
  // Resource has ended
  if (currentTime >= resource.endTime) {
    return resource.cost;
  }
  
  // Resource is active - calculate proportional cost
  const elapsed = currentTime - resource.startTime;
  const duration = resource.endTime - resource.startTime;
  return (resource.cost / duration) * elapsed;
}
```

---

## API Endpoints Needed

### 1. POST /api/burn-plan
**Request:**
```json
{
  "amount": 10000,
  "burningStyle": "Horizontal",
  "stupidityLevel": 7,
  "timeHorizon": "1h"
}
```

**Response:**
```json
{
  "sessionId": "abc-123",
  "burnPlan": { /* BurnPlan structure */ }
}
```

### 2. GET /api/burn-status?sessionId=abc-123
**Response:**
```json
{
  "sessionId": "abc-123",
  "startTime": 1234567890,
  "currentTime": 1234567920,
  "moneyRemaining": 7000,
  "moneyBurned": 3000,
  "activeResources": [
    { "service": "EC2 m5.24xlarge", "cost": 2000 },
    { "service": "RDS Aurora", "cost": 1000 }
  ],
  "progress": 0.30
}
```

### 3. POST /api/roast
**Request:**
```json
{
  "sessionId": "abc-123",
  "moneyBurned": 5000,
  "totalAmount": 10000,
  "stupidityLevel": 7,
  "activeResources": ["EC2 m5.24xlarge", "RDS Aurora"]
}
```

**Response:**
```json
{
  "roast": "You've burned $5,000 - that's 2,500 burritos you'll never eat. Hope those EC2 instances are keeping you warm at night."
}
```

---

## Notes for Backend Team

1. **Pre-calculate rates**: Include `costPerSecond` in the burn plan to simplify frontend calculations
2. **Realistic timing**: Ensure `startTime` and `endTime` create an interesting visualization (stagger services)
3. **Category grouping**: Assign each service to a category for the pie chart
4. **Total validation**: Ensure sum of all resource costs equals the requested amount (±5%)
5. **Stupidity scaling**: Higher stupidity levels should produce more absurd service combinations

---

## Testing Data

For frontend development, use this mock burn plan:

```json
{
  "sessionId": "test-123",
  "totalAmount": 10000,
  "duration": 60,
  "resources": [
    {
      "service": "EC2 m5.24xlarge",
      "category": "Compute",
      "cost": 3500,
      "startTime": 0,
      "endTime": 60,
      "description": "Massive compute for minimal work",
      "costPerSecond": 58.33
    },
    {
      "service": "RDS Aurora",
      "category": "Database",
      "cost": 2800,
      "startTime": 5,
      "endTime": 60,
      "description": "Enterprise database for a todo list",
      "costPerSecond": 50.91
    },
    {
      "service": "S3 Storage",
      "category": "Storage",
      "cost": 2100,
      "startTime": 0,
      "endTime": 60,
      "description": "Storing memes at scale",
      "costPerSecond": 35.00
    },
    {
      "service": "Lambda",
      "category": "Compute",
      "cost": 1200,
      "startTime": 10,
      "endTime": 60,
      "description": "Serverless functions that never get called",
      "costPerSecond": 24.00
    },
    {
      "service": "NAT Gateway",
      "category": "Networking",
      "cost": 400,
      "startTime": 0,
      "endTime": 60,
      "description": "Routing packets to nowhere",
      "costPerSecond": 6.67
    }
  ]
}
```
