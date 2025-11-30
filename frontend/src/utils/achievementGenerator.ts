export interface Achievement {
  title: string;
  description: string;
}

/**
 * Achievement titles with their snarky descriptions
 */
const ACHIEVEMENT_TYPES: Achievement[] = [
  {
    title: 'Money Bonfire',
    description:
      "You've successfully turned your AWS budget into smoke and ashes. At least a real bonfire would've kept you warm.",
  },
  {
    title: 'Cash Incinerator',
    description:
      "Congratulations! You've built the world's most expensive furnace. Your money went up in flames faster than a serverless cold start.",
  },
  {
    title: 'Budget Arsonist',
    description:
      "You didn't just burn the budget - you doused it in gasoline and threw in a match. The finance team is calling the fire department.",
  },
  {
    title: 'Spend Wrecker',
    description:
      "You've demolished spending limits with the precision of a wrecking ball. Your cost optimization strategy is 'what cost optimization?'",
  },
  {
    title: "CFO's Worst Nightmare",
    description:
      "The CFO wakes up in cold sweats thinking about your AWS bill. You've achieved legendary status in the accounting department (not the good kind).",
  },
  {
    title: "Finance's Enemy",
    description:
      "The finance team has your photo on a dartboard. You've single-handedly proven that cloud costs can indeed spiral out of control.",
  },
];

/**
 * Generates a random achievement with title and description
 */
export function generateRandomAchievement(): Achievement {
  const randomIndex = Math.floor(Math.random() * ACHIEVEMENT_TYPES.length);
  return ACHIEVEMENT_TYPES[randomIndex];
}
