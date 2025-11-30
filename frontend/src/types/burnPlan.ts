export interface BurnPlanResponse {
  total_amount: string;
  timeline_days: number;
  efficiency_level: string;
  architecture_type?: string;
  burning_style?: string;
  services_deployed: ServiceDeployment[];
  total_calculated_cost: number;
  deployment_scenario: string;
  key_mistakes: string[];
  recommendations: string[];
  roast: string,
  achievement?: {
    title: string;
    text: string;
  };
}

export interface ServiceDeployment {
  service_name: string;
  instance_type: string;
  quantity: number;
  unit_cost: number;
  total_cost: number;
  start_day: number;
  end_day: number;
  duration_used: string;
  usage_pattern: string;
  waste_factor: string;
  roast: string;
}

// Helper to convert backend format to frontend chart format
export function convertToChartData(burnPlan: BurnPlanResponse) {
  // For racing bar chart - sort by total cost
  const racingBarData = burnPlan.services_deployed
    .map((service) => ({
      name: `${service.service_name} ${service.instance_type}`,
      value: service.total_cost,
    }))
    .sort((a, b) => b.value - a.value);

  // For pie chart - group by service category
  const serviceCategories = new Map<string, number>();
  burnPlan.services_deployed.forEach((service) => {
    const category = getServiceCategory(service.service_name);
    const current = serviceCategories.get(category) || 0;
    serviceCategories.set(category, current + service.total_cost);
  });

  const pieChartData = Array.from(serviceCategories.entries()).map(([name, value]) => ({
    name,
    value,
  }));

  // For line chart - calculate cumulative cost over timeline
  const timelineData = calculateTimelineData(burnPlan);

  return {
    racingBarData,
    pieChartData,
    timelineData,
    totalCost: burnPlan.total_calculated_cost,
    timeline: burnPlan.timeline_days,
  };
}

function getServiceCategory(serviceName: string): string {
  const categories: Record<string, string> = {
    EC2: 'Compute',
    EKS: 'Compute',
    Lambda: 'Compute',
    Fargate: 'Compute',
    RDS: 'Database',
    DynamoDB: 'Database',
    Aurora: 'Database',
    S3: 'Storage',
    EBS: 'Storage',
    EFS: 'Storage',
    CloudFront: 'Networking',
    'API Gateway': 'Networking',
    'NAT Gateway': 'Networking',
    ALB: 'Networking',
    SageMaker: 'ML/AI',
    Bedrock: 'ML/AI',
  };

  return categories[serviceName] || 'Other';
}

function calculateTimelineData(burnPlan: BurnPlanResponse) {
  const days = burnPlan.timeline_days;
  const points = Math.min(days, 60); // Max 60 data points
  const interval = days / points;

  const timestamps: string[] = [];
  const values: number[] = [];

  for (let i = 0; i <= points; i++) {
    const currentDay = Math.floor(i * interval);
    timestamps.push(`Day ${currentDay}`);

    // Calculate cumulative cost up to this day
    let cumulativeCost = 0;
    burnPlan.services_deployed.forEach((service) => {
      if (currentDay >= service.start_day && currentDay <= service.end_day) {
        const daysActive = Math.min(currentDay - service.start_day, service.end_day - service.start_day);
        const totalDuration = service.end_day - service.start_day;
        cumulativeCost += (service.total_cost / totalDuration) * daysActive;
      }
    });

    values.push(cumulativeCost);
  }

  return { timestamps, values };
}

// Helper to scale burn plan to a new amount
export function scaleBurnPlan(
  originalPlan: BurnPlanResponse,
  newAmount: number
): BurnPlanResponse {
  const originalAmount = parseFloat(originalPlan.total_amount.replace('$', ''));
  const scaleFactor = newAmount / originalAmount;

  return {
    ...originalPlan,
    total_amount: `$${newAmount}`,
    services_deployed: originalPlan.services_deployed.map((service) => ({
      ...service,
      total_cost: service.total_cost * scaleFactor,
    })),
    total_calculated_cost: originalPlan.total_calculated_cost * scaleFactor,
  };
}
