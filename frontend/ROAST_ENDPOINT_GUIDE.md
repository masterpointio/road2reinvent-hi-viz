# Roast/Snark Endpoint Implementation Guide

## Overview

The roast endpoint generates snarky, humorous commentary about the user's AWS spending choices. It's called at key milestones (25%, 50%, 75%, 100%) during the burn to provide entertainment and emphasize the absurdity of the spending.

## Endpoint Specification

### POST /api/roast

**Request:**
```json
{
  "sessionId": "demo-123",
  "moneyBurned": 5000,
  "totalAmount": 10000,
  "progress": 50,
  "stupidityLevel": 7,
  "activeResources": [
    "EC2 m5.24xlarge",
    "RDS Aurora",
    "NAT Gateway"
  ],
  "topService": "EC2 m5.24xlarge",
  "topServiceCost": 2500
}
```

**Response:**
```json
{
  "roast": "You've burned $5,000 - that's 2,500 burritos you'll never eat. Hope those EC2 instances are keeping you warm at night."
}
```

## Roast Generation Strategies

### 1. **Relatable Comparisons** (Most Effective)

Compare AWS costs to everyday items people understand:

**Examples:**
- "That's 2,500 burritos you'll never eat"
- "You could've bought 83 Netflix subscriptions"
- "That's 1,250 cups of Starbucks coffee"
- "You just spent the equivalent of 50 Uber rides to nowhere"
- "That's 200 months of Spotify Premium"
- "You could've bought 25 Nintendo Switches"

**Formula:**
```
cost / itemPrice = quantity
"That's {quantity} {items} you'll never {verb}"
```

**Common Items:**
- Burrito: $2
- Coffee: $4
- Netflix: $15/month
- Spotify: $10/month
- Movie ticket: $12
- Pizza: $15
- Uber ride: $20

### 2. **Service-Specific Roasts**

Tailor roasts to the specific AWS services being used:

**EC2 Instances:**
- "96 vCPUs to run a hello world app? Bold choice."
- "That EC2 instance has more cores than your entire user base."
- "Running a t2.micro would've been too reasonable, huh?"
- "Your EC2 fleet could mine Bitcoin... but it's just serving cat pictures."

**RDS/Databases:**
- "An enterprise database cluster for your 3 users. They'll appreciate the redundancy."
- "That RDS instance costs more per hour than most people make."
- "Multi-AZ for a todo list? Living dangerously."
- "Your database has more replicas than you have customers."

**S3 Storage:**
- "Storing memes at enterprise scale. Jeff Bezos thanks you."
- "That's a lot of S3 buckets for your vacation photos."
- "Glacier would've been cheaper, but where's the fun in that?"

**Lambda:**
- "Serverless functions that never get called. The cloud is crying."
- "1 million Lambda invocations for a function that returns 'Hello World'."
- "Your Lambda functions are lonelier than a 404 page."

**NAT Gateway:**
- "NAT Gateways routing packets to nowhere. Efficient."
- "That NAT Gateway costs more than your actual compute."
- "Paying premium prices to route traffic you don't have."

**Load Balancers:**
- "An Application Load Balancer for one server. Just in case."
- "Load balancing zero traffic like a pro."

### 3. **Progress-Based Roasts**

Adjust tone based on how far into the burn they are:

**25% Progress:**
- "Just getting started and already burned ${amount}. This is going well."
- "Quarter of the way there. Your wallet is already crying."
- "25% done, 75% more regret to go."

**50% Progress:**
- "Halfway to zero. How does it feel?"
- "You're at the point of no return. Well, you were at the point of no return at 0%."
- "$5,000 down, $5,000 to go. At least you're consistent."

**75% Progress:**
- "Three quarters done. Your accountant is drafting their resignation."
- "Almost there! Just a few thousand more dollars to waste."
- "75% complete. That's a passing grade in school, but an F in financial planning."

**100% Progress:**
- "Congratulations! You've successfully burned ${amount}. Your AWS bill will remember this."
- "Mission accomplished. You've turned money into... well, nothing."
- "All done! That was fun. Your CFO might disagree."
- "You did it! ${amount} gone in 60 seconds. Faster than a Nicolas Cage movie."

### 4. **Stupidity Level Scaling**

Adjust roast severity based on stupidity level (1-10):

**Low Stupidity (1-3):**
- Mild, educational tone
- "That's a bit wasteful, but at least it's somewhat practical."
- "Could've been worse. Could've been better too."

**Medium Stupidity (4-7):**
- Sarcastic, humorous
- "Bold choices were made here."
- "Your architecture is... creative."

**High Stupidity (8-10):**
- Savage, absurd
- "This is performance art, right? Please tell me this is performance art."
- "I've seen more sensible spending at a casino."
- "Your AWS bill is going to need its own AWS bill."

### 5. **Time-Based Roasts**

Reference how quickly money is burning:

**Fast Burn Rate:**
- "Burning money faster than a bonfire burns marshmallows."
- "At this rate, you could fund a small country's deficit."
- "That's ${rate}/second. Most people don't make that per hour."

**Slow Burn Rate:**
- "Taking your time with this financial disaster. I respect the patience."
- "Slow and steady loses the race... and the money."

### 6. **Comparison Roasts**

Compare to other wasteful things:

- "This is less efficient than using a helicopter to commute."
- "You're burning money faster than a politician's campaign."
- "This makes buying lottery tickets look like a sound investment."
- "Even crypto bros are impressed by this waste."

## Strands Agent Prompt Structure

### System Prompt

```
You are a snarky AWS cost analyst who roasts people for wasting money on cloud resources. 
Your job is to generate witty, humorous commentary that:

1. Compares costs to relatable everyday items (burritos, coffee, Netflix, etc.)
2. Points out the absurdity of their service choices
3. Uses sarcasm and humor, but stays lighthearted (not mean-spirited)
4. Keeps responses under 100 words
5. Adjusts tone based on stupidity level (1-10 scale)

Style: Witty, sarcastic, tech-savvy, slightly condescending but funny
Tone: Like a friend roasting you for a bad decision, not an angry parent
```

### Dynamic Prompt Template

```
The user has burned ${{moneyBurned}} out of ${{totalAmount}} ({{progress}}% complete).

Active services:
{{#each activeResources}}
- {{this}}
{{/each}}

Top spending service: {{topService}} (${{topServiceCost}})
Stupidity level: {{stupidityLevel}}/10

Generate a snarky roast about their spending. Include:
1. A relatable comparison (burritos, coffee, Netflix, etc.)
2. A jab at their service choices
3. Keep it under 100 words
4. Match the stupidity level (higher = more savage)

{{#if progress == 25}}
This is their first milestone - set the tone.
{{else if progress == 50}}
They're halfway done - remind them of the damage.
{{else if progress == 75}}
Almost done - build anticipation.
{{else if progress == 100}}
Final roast - make it memorable.
{{/if}}
```

## Example Roasts by Milestone

### 25% Milestone Examples

```json
{
  "moneyBurned": 2500,
  "totalAmount": 10000,
  "progress": 25,
  "stupidityLevel": 7,
  "topService": "EC2 m5.24xlarge"
}
```

**Roast Options:**
1. "Just $2,500 in and you're already running EC2 instances that could power a small data center. That's 1,250 burritos you'll never taste. Bold start."
2. "Quarter of the way there! You've burned enough to buy 166 Netflix subscriptions. But sure, those 96 vCPUs are definitely necessary."
3. "25% done, and that EC2 instance is already costing more than most people's rent. Your hello world app must be very important."

### 50% Milestone Examples

```json
{
  "moneyBurned": 5000,
  "totalAmount": 10000,
  "progress": 50,
  "stupidityLevel": 8,
  "topService": "RDS Aurora"
}
```

**Roast Options:**
1. "Halfway to zero! That's 2,500 burritos, 833 coffees, or one very confused accountant. Your RDS cluster is living its best life serving 3 users."
2. "You're at 50% and that Aurora database is eating money faster than you can say 'multi-AZ'. That's 416 Uber rides to nowhere."
3. "$5,000 down the drain. You could've bought a used car, but instead you chose enterprise-grade database redundancy for a todo list. Respect."

### 75% Milestone Examples

```json
{
  "moneyBurned": 7500,
  "totalAmount": 10000,
  "progress": 75,
  "stupidityLevel": 9,
  "topService": "NAT Gateway"
}
```

**Roast Options:**
1. "75% complete and your NAT Gateway is routing packets to the void. That's 3,750 burritos that could've been yours. Almost there!"
2. "Three quarters done! You've spent enough to fund 500 months of Spotify Premium. But sure, those NAT Gateways are definitely earning their keep."
3. "$7,500 gone. Your AWS bill is going to need therapy. That NAT Gateway is living rent-free in your budget."

### 100% Milestone Examples

```json
{
  "moneyBurned": 10000,
  "totalAmount": 10000,
  "progress": 100,
  "stupidityLevel": 10,
  "topService": "EC2 m5.24xlarge"
}
```

**Roast Options:**
1. "🎉 Congratulations! You've successfully burned $10,000 in 60 seconds. That's 5,000 burritos, 666 Netflix subscriptions, or one very expensive lesson. Your EC2 instances salute you."
2. "Mission accomplished! $10,000 gone faster than a Nicolas Cage movie. You could've bought a decent used car, but instead you chose cloud computing glory. Jeff Bezos sends his regards."
3. "All done! You've turned $10,000 into absolutely nothing. That's 2,500 Starbucks runs, 833 movie tickets, or one legendary AWS bill. Your CFO is updating their resume as we speak."

## Implementation Tips

### 1. **Use Templates with Variables**

```python
templates = [
    "That's {quantity} {item} you'll never {verb}. {service_roast}",
    "You could've bought {quantity} {item}, but instead you chose {service}. {commentary}",
    "{progress_comment} That's {quantity} {item} down the drain. {service_roast}"
]

items = [
    {"name": "burritos", "price": 2, "verb": "eat"},
    {"name": "coffees", "price": 4, "verb": "drink"},
    {"name": "Netflix subscriptions", "price": 15, "verb": "watch"}
]
```

### 2. **Randomize for Variety**

Don't use the same roast twice. Mix and match:
- Different comparisons
- Different service roasts
- Different sentence structures

### 3. **Context Awareness**

Use the data provided:
- If EC2 is top service → roast EC2
- If progress is 100% → make it memorable
- If stupidity is 10 → go savage

### 4. **Keep It Fresh**

For a 60-second demo, you need 4 unique roasts. Make sure they:
- Don't repeat comparisons
- Build in intensity
- Reference different services
- Have variety in tone

## Testing Examples

### Test Case 1: Low Stupidity, Early Progress
```json
Input: {
  "moneyBurned": 2500,
  "progress": 25,
  "stupidityLevel": 3,
  "topService": "EC2 t3.medium"
}

Expected: Mild, educational tone
"$2,500 spent on a t3.medium. That's 1,250 burritos, but at least you chose a reasonable instance size. Could be worse!"
```

### Test Case 2: High Stupidity, Final Progress
```json
Input: {
  "moneyBurned": 10000,
  "progress": 100,
  "stupidityLevel": 10,
  "topService": "100 NAT Gateways"
}

Expected: Savage, memorable
"🎉 $10,000 GONE! You deployed 100 NAT Gateways. That's 5,000 burritos, or enough to make Jeff Bezos personally thank you. This is art."
```

## Frontend Integration

The frontend will display roasts in a toast notification or dedicated roast panel:

```typescript
// Call at milestones
if (progress === 25 || progress === 50 || progress === 75 || progress === 100) {
  const roast = await api.post('/api/roast', {
    sessionId,
    moneyBurned,
    totalAmount,
    progress,
    stupidityLevel,
    activeResources,
    topService,
    topServiceCost
  });
  
  // Display roast
  showRoast(roast.roast);
}
```

## Summary

**Key Principles:**
1. ✅ Compare to relatable items (burritos, coffee, Netflix)
2. ✅ Roast specific services being used
3. ✅ Scale intensity with stupidity level
4. ✅ Build momentum across milestones
5. ✅ Keep it funny, not mean
6. ✅ Under 100 words
7. ✅ Make it memorable

**Goal:** Make people laugh while emphasizing the absurdity of cloud waste. It's entertainment with a message!
