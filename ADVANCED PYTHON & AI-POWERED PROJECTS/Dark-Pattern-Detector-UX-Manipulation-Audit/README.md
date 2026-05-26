# Day 26 — The Dark Pattern Detector
### Apps Aren't Tricking YOU. They're Tricking EVERYONE. | 10x.in

---

## What is this?

Every app you use is manipulating you. Not all of them. But most of them.

Fake urgency timers. Hidden fees that appear at checkout. Pre-checked boxes for add-ons you didn't want. Guilt-trip cancellation flows ("No thanks, I hate saving money"). Free trials that auto-charge. "Only 2 left in stock" when they have 10,000.

These aren't accidents. They're called **dark patterns** — design tricks engineered to make you spend more, stay longer, and give up more data than you intended.

This project analyzes 12,000 user sessions across 10 apps and exposes every manipulation technique being used — and puts a dollar sign on how much money they're extracting.

---

## The Core Idea

Dark patterns aren't bugs. They're features. Designed on purpose. Tested. Optimized. Rolled out.

Companies hire UX researchers to measure exactly how much extra money they can extract by moving a button, pre-checking a box, or adding guilt-trip language. The entire "growth hacking" industry is partially built on manipulation.

Users lose money. Users lose time. Users lose trust. But they don't realize it's happening because it's invisible by design.

**The shift**: Stop blaming yourself for overspending on apps. Start recognizing the 14 patterns they use to manipulate you.

---

## The Data

12,000 user sessions across 10 apps:

| Column | What It Tells Us |
|---|---|
| app_name / app_category | Which app and category |
| device / user_age_group / user_tech_savvy | User profile |
| intended_action | What the user wanted to do |
| 14 dark pattern columns | Which patterns were encountered |
| total_pattern_instances | Total manipulation events in the session |
| time_spent_minutes | How long it took (manipulation slows people down) |
| intended_spend_usd / actual_spend_usd / extra_charges_usd | How much MORE they paid than they wanted |
| action_outcome | What actually happened |
| completed_intended_action | Did they achieve their goal? |
| frustration_score | How frustrated they were (1-10) |
| would_use_again | Will they come back? |

**The 14 Dark Patterns**: hidden fees, fake urgency, pre-checked boxes, confirmshaming, sneaked into basket, hard to cancel, false social proof, forced continuity, roach motel, misdirection, price comparison blocking, trick questions, disguised ads, bait and switch.

---

## The 8 Outputs

1. **Manipulation Audit Dashboard** — complete exposure of app tricks
2. **App Manipulation Scoreboard** — all 10 apps ranked by how manipulative they are
3. **The Money Stolen** — exact dollars extracted by each pattern
4. **Time Tax** — how much extra time users spend dealing with manipulation
5. **Cancellation Trap** — who gets stuck in subscriptions
6. **Vulnerability Map** — which user groups fall for which patterns
7. **Pattern Recognition Cards** — visual guide to the 14 dark patterns
8. **Manipulation Report** — full audit with user + business recommendations

---

## Project Structure

```
dark-pattern-detector/
├── CLAUDE.md              ← Claude Code reads this
├── data/
│   └── app_sessions.csv   ← 12,000 sessions
└── output/                ← 8 files land here
```

---

## The Prompts

### Prompt 01 — Run It
```
Run it
```

### Prompt 02 — Dashboard
```
Open the dashboard
```

### Prompt 03 — The Worst Offenders
```
Rank all 10 apps by how manipulative they are. Which app uses the most dark patterns? Which apps are actually ethical?
```

### Prompt 04 — How Much Money
```
Calculate the exact dollar cost of dark patterns. Which pattern steals the most money? How much extra does the average user pay?
```

### Prompt 05 — The Cancellation Trap
```
For subscription apps — what percentage of users successfully cancel vs give up? How many people are trapped in subscriptions they don't want?
```

### Prompt 06 — Who's Most Vulnerable
```
Which user groups fall for dark patterns the most? Break down by age, tech savvy, and device.
```

### Prompt 07 — Ethics vs Revenue
```
Do ethical apps (no dark patterns) make less money? Compare clean apps vs manipulative apps on retention, frustration, and revenue.
```

### Prompt 08 — The Pattern Cheat Sheet
```
Create a visual reference of all 14 dark patterns with names, descriptions, and examples. Make it shareable.
```

### Prompt 09 — The Full Exposure Report
```
Write a complete manipulation audit — every app's dark pattern score, every dollar extracted, every hour stolen, and 5 actions users can take to protect themselves.
```

---

## What You'll Discover

| What You Think | What's Actually True |
|---|---|
| I'm too smart to fall for dark patterns | Tech-savvy users fall for 40% fewer, but still fall for them |
| Dark patterns are rare | The average manipulative app uses 5 of them per session |
| Ethical apps lose money | Clean apps have higher retention and similar revenue |
| Hidden fees are the worst | Forced continuity (trial auto-conversion) steals more silently |
| Cancelling a subscription is easy | Up to 38% of users give up on cancellation due to friction |

---

## The Shift

> You're not overspending because you're weak.
> You're overspending because apps are engineered to extract money.
>
> You're not staying in subscriptions because you want to.
> You're staying because cancellation was designed to be impossible.
>
> Once you can name the 14 patterns,
> you can never be tricked by them again.

---

*Day 26 of 28 | Built with Claude Code | 10x.in*
