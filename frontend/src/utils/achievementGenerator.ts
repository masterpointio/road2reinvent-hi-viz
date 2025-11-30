/**
 * Generates snarky achievement text based on the burn amount
 */
export function generateAchievementText(amount: number): string {
  const achievements = [
    {
      threshold: 1000,
      messages: [
        "Baby's First Burn! You've wasted $${amount} on AWS. That's like 200 coffees you'll never drink, but at least your Lambda functions are 'serverless'.",
        "Congratulations! You spent $${amount} learning that 'free tier' doesn't mean 'free forever'. Your credit card company sends their regards.",
        "Achievement Unlocked: $${amount} burned! That's enough to subscribe to Netflix for 5 years, but you chose NAT Gateways instead. Bold choice.",
      ],
    },
    {
      threshold: 5000,
      messages: [
        "Impressive! $${amount} down the drain. You could've bought a decent used car, but instead you got EC2 instances running at 3% CPU. Living the dream!",
        "You've burned $${amount}! That's a nice vacation you're not taking because you forgot to turn off your RDS instances. Hope those logs were worth it.",
        "$${amount} wasted! Your accountant called - they want to know why you need 47 load balancers for a todo app. We're wondering too.",
      ],
    },
    {
      threshold: 10000,
      messages: [
        "Holy overspending! $${amount} burned! You could've bought a luxury car, but instead you got 50 Kubernetes nodes running at 2% CPU. Your DevOps team is impressed by your commitment to waste.",
        "Congratulations on burning $${amount}! That's enough to hire a junior developer for 3 months, but you chose SageMaker instances running 24/7 instead. Priorities!",
        "$${amount} obliterated! You've achieved 'Enterprise Architect' level waste. Your CloudFront distribution for localhost is particularly inspired.",
      ],
    },
    {
      threshold: 25000,
      messages: [
        "LEGENDARY WASTE! $${amount} burned! You could've made a down payment on a house, but you chose to run AWS Ground Station for your weather app. Respect.",
        "$${amount} incinerated! That's a year of college tuition, but instead you have multi-region active-active deployment for your personal blog. Chef's kiss.",
        "You've torched $${amount}! Your CFO is crying, your CTO is confused, and AWS is sending you a thank-you card. This is art.",
      ],
    },
    {
      threshold: 50000,
      messages: [
        "ABSOLUTE MADNESS! $${amount} BURNED! You could've bought a Tesla, but you chose AWS Outposts for your cloud-native app. The irony is not lost on us.",
        "$${amount} ANNIHILATED! That's a small business you could've started, but instead you have 200 idle EC2 instances. Your legacy will live forever in AWS billing history.",
        "HALL OF FAME WASTE! $${amount} destroyed! You've transcended mere incompetence and achieved pure chaos. AWS named a data center after you.",
      ],
    },
    {
      threshold: Infinity,
      messages: [
        "COSMIC LEVEL DESTRUCTION! $${amount} VAPORIZED! You've achieved what we thought was impossible. AWS is considering making you a board member.",
        "$${amount} OBLITERATED FROM EXISTENCE! Your spending has its own gravitational field. Scientists are studying your billing statements.",
        "ULTIMATE ACHIEVEMENT! $${amount} BURNED! You've won AWS Bill Burner. There's nothing left to burn. Your name will be whispered in hushed tones at FinOps conferences.",
      ],
    },
  ];

  // Find the appropriate tier
  const tier = achievements.find((a) => amount < a.threshold) || achievements[achievements.length - 1];

  // Pick a random message from the tier
  const message = tier.messages[Math.floor(Math.random() * tier.messages.length)];

  // Replace ${amount} with the actual formatted amount
  return message.replace('${amount}', amount.toLocaleString());
}
