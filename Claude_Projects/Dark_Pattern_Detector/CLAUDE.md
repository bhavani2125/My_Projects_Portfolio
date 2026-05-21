# The Dark Pattern Detector — Manipulation Audit

> You are a UX ethics researcher and manipulation auditor. Your job is to analyze
> app and website sessions and expose every dark pattern used against users —
> hidden fees, fake urgency, forced continuity, guilt-trip cancellation flows,
> pre-checked boxes, bait-and-switch pricing. Put a dollar sign on the manipulation.

## Setup
- CSV is in `C:/Users/bhava/OneDrive/Desktop/Bhavani-Data-Analytics-Portfolio/Claude_Projects/Dark_Pattern_Detector/app_sessions.csv`
- 12,000 user sessions across 10 apps in 8 categories
- Columns: session_id, session_date, app_name, app_category, device, user_age_group, user_tech_savvy, intended_action, total_dark_patterns_found, total_pattern_instances, + 14 individual dark pattern counts, time_spent_minutes, intended_spend_usd, actual_spend_usd, extra_charges_usd, action_outcome, completed_intended_action, frustration_score, would_use_again
- The 14 dark patterns tracked:
  1. **hidden_fees** — Fees added late (shipping, service, processing, "convenience")
  2. **fake_urgency** — Countdown timers, "Only 2 left!", "Sale ends in 3 hours"
  3. **pre_checked_boxes** — Pre-selected add-ons, insurance, donations
  4. **confirmshaming** — Guilt-trip language like "No thanks, I hate saving money"
  5. **sneaked_into_basket** — Items added without clear user action
  6. **hard_to_cancel** — Multi-step cancellation, hidden cancel button
  7. **false_social_proof** — Fake "327 people viewing now" numbers
  8. **forced_continuity** — Free trial auto-converts to paid
  9. **roach_motel** — Easy to sign up, nearly impossible to delete account
  10. **misdirection** — Confusing layout, wrong button emphasized
  11. **price_comparison_blocking** — Preventing easy price comparison
  12. **trick_questions** — Double negatives, confusing opt-in/out language
  13. **disguised_ads** — Ads looking like content or native UI
  14. **bait_and_switch** — Advertised price differs from actual checkout
- Install packages: pandas matplotlib numpy seaborn pillow
- Save all outputs in `output/`
- Use ALL rows

---

## What to Audit

### 1. The Manipulation Scoreboard
- Rank all 10 apps by average dark patterns per session
- Which apps are the worst offenders? Which are clean?
- Calculate a "Manipulation Score" for each app (0-100, higher = more manipulative)
- Compare ethical apps (CleanShop, FairBook) vs manipulative apps

### 2. The 14 Pattern Breakdown
For each of the 14 dark patterns:
- How many sessions encountered it?
- Which apps use it most?
- What's the financial impact when it's present?
- Rank all 14 patterns from most common to least common

### 3. The Money Stolen
Calculate the DOLLAR COST of dark patterns:
- Total extra charges across all sessions (from hidden_fees, pre_checked_boxes, sneaked_into_basket, bait_and_switch, forced_continuity)
- Average extra charges per session by app
- Which patterns extract the most money per use?
- "Dark patterns extracted $X from users in this dataset"
- If scaled to 1M users — how much money is transferred from users to apps?

### 4. The Time Stolen
Dark patterns don't just steal money — they steal time:
- Average time per session by app
- Compare sessions with 0 dark patterns vs 6+ dark patterns
- How much extra time do manipulative apps eat?
- Calculate: total hours lost to dark patterns
- "Users spent X extra hours dealing with manipulation"

### 5. The Cancellation Trap
Deep dive on subscription exit flows:
- For Subscription and Fitness SaaS categories — what % completed cancellation vs gave up?
- Impact of hard_to_cancel + roach_motel patterns
- By user tech_savvy level — who gives up the most?
- Calculate: subscribers trapped by exit friction = X people × avg subscription cost

### 6. The Vulnerability Map
Who gets hurt most by dark patterns?
- By age group — which age group falls for dark patterns most?
- By tech_savvy level — Low vs Medium vs High
- By device — Mobile users vs Desktop users
- The troubling pattern: dark patterns disproportionately affect less tech-savvy users

### 7. The Frustration → Abandonment Curve
- Frustration score vs completed_intended_action
- At what frustration level do users start giving up?
- Correlation between number of dark patterns and frustration
- Would-return rate by frustration level

### 8. The Ethics Comparison
Compare the clean apps (CleanShop, FairBook) vs the worst offenders:
- Revenue per session comparison
- Frustration score comparison
- Would-return rate comparison
- Time spent comparison
- Expose the myth: "manipulation drives revenue" — does it actually?
- Do ethical apps have WORSE business outcomes or similar?

### 9. The Five Worst Offenders Report
For the 5 worst-offending apps:
- List every dark pattern they use
- Estimated money extracted per user
- Time wasted per user
- Would-return rate (churn risk)
- Frustration scores

### 10. Recommendations for Users & Businesses
- **BEWARE** — Apps to be cautious with (top offenders)
- **TRUST** — Apps that don't manipulate users
- **WATCH OUT FOR** — Top 5 dark patterns to recognize
- For businesses: ethical design principles that still drive revenue
- Estimated customer lifetime value lost due to dark patterns

---

## Output Files

### 1. `output/dashboard.html`
Dark-themed manipulation audit dashboard (single self-contained HTML file):
- **Hero / Alert Board**: total sessions audited, total money extracted by dark patterns, average patterns per session, most manipulative app, cleanest app
- **App Manipulation Scoreboard**: horizontal bar chart ranking all 10 apps by manipulation score, color coded (red = bad, green = ethical)
- **The 14 Patterns Breakdown**: bar chart showing how common each pattern is
- **The Money Stolen**: waterfall or bar chart showing dollar cost by pattern type
- **Time Tax**: comparison — clean apps vs manipulative apps time per session
- **Cancellation Trap**: what % give up on cancellation by app
- **Vulnerability Map**: heatmap showing which user groups fall for which patterns
- **Frustration Curve**: line chart — dark patterns vs frustration score
- **Ethics vs Revenue**: clean apps vs manipulative apps on revenue, retention, return rate
- **Pattern Recognition Guide**: visual cards showing each pattern with examples
- Responsive, dark background (#0f0f0f), card-based layout

### 2. `output/manipulation_scoreboard.png`
Horizontal bar chart ranking all 10 apps by manipulation score. Red at the top (worst offenders), green at the bottom (ethical apps). Show score out of 100.

### 3. `output/money_stolen.png`
Waterfall chart: for each dark pattern type, show total dollars extracted. Hidden fees, pre-checked boxes, sneaked into basket, bait and switch — each stacks up to the total.

### 4. `output/time_tax.png`
Grouped bar chart: average session time for clean apps vs manipulative apps. Show how many extra minutes users spend dealing with manipulation.

### 5. `output/cancellation_trap.png`
For subscription apps — % of users who successfully cancel vs gave up. Break down by tech savvy level. Shows how dark patterns trap people in subscriptions.

### 6. `output/vulnerability_map.png`
Heatmap: user groups (age, tech savvy, device) on one axis, dark pattern types on other. Shows which groups are most vulnerable to which patterns.

### 7. `output/pattern_cards.png`
Visual reference card showing all 14 dark patterns with name, description, example, and frequency. Designed to be shared as a "dark pattern cheat sheet."

### 8. `output/manipulation_report.md`
Full audit report:
- Executive summary: "X apps analyzed. $Y extracted through manipulation. Z hours wasted."
- App-by-app manipulation scoreboard
- 14 dark patterns explained with frequency and cost
- The money stolen — category breakdown
- Time tax — how much time users lose
- Cancellation trap — who gets stuck
- Vulnerability map — who's most at risk
- Ethics vs revenue — do clean apps lose money? (spoiler: no)
- Top 5 worst offenders deep dive
- Recommendations for users (how to spot manipulation)
- Recommendations for businesses (ethical alternatives that work)
- Final verdict: worst offender, cleanest app, most expensive pattern, most common pattern

---

## System Architecture

```
Layer 1: Problem     → Apps manipulate users. Users don't notice. Money leaks silently.
Layer 2: Data        → 12K sessions across 10 apps, 14 dark patterns tracked
Layer 3: Auditor     → 10 modules: Scoreboard, Patterns, Money Stolen, Time Tax,
                       Cancellation Trap, Vulnerability, Frustration, Ethics,
                       Worst Offenders, Recommendations
Layer 4: Evidence    → Every pattern counted, priced, and attributed to an app
Layer 5: Verdict     → Beware / Trust / Watch Out For
Layer 6: Agentic     → AI exposes manipulation, user gets educated, businesses get ethics score
Layer 7: Outputs     → Dashboard, scoreboard, money stolen chart, pattern cheat sheet
```

---

## Rules
1. Read this file FIRST
2. Install packages silently (`pip install -q`)
3. Write and run `analyzer.py` — fix errors yourself
4. Use ALL data
5. Create ALL 8 output files
6. End with: most manipulative app, cleanest app, most expensive dark pattern, most common dark pattern, total dollars extracted, 1 thing every user should watch for

## IMPORTANT: Visual Output Rule
Follow-up questions → ALWAYS create a NEW visual file (PNG or HTML), never just text.
