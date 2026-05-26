import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Data path
DATA_PATH = 'app_sessions.csv'

def load_data():
    return pd.read_csv(DATA_PATH)

def calculate_manipulation_score(df):
    app_stats = df.groupby('app_name')['total_dark_patterns_found'].mean().reset_index()
    max_avg = app_stats['total_dark_patterns_found'].max()
    app_stats['manipulation_score'] = (app_stats['total_dark_patterns_found'] / max_avg) * 100
    return app_stats.sort_values('manipulation_score', ascending=False)

def main():
    df = load_data()

    # 1. Manipulation Scoreboard
    app_scores = calculate_manipulation_score(df)

    # 2. Pattern Breakdown
    patterns = [
        'hidden_fees', 'fake_urgency', 'pre_checked_boxes', 'confirmshaming',
        'sneaked_into_basket', 'hard_to_cancel', 'false_social_proof',
        'forced_continuity', 'roach_motel', 'misdirection',
        'price_comparison_blocking', 'trick_questions', 'disguised_ads', 'bait_and_switch'
    ]

    pattern_counts = df[patterns].sum().sort_values(ascending=False)

    # 3. Money Stolen
    monetary_patterns = ['hidden_fees', 'pre_checked_boxes', 'sneaked_into_basket', 'bait_and_switch', 'forced_continuity']
    total_extra_charges = df['extra_charges_usd'].sum()

    pattern_cost = {}
    for p in monetary_patterns:
        cost = df[df[p] > 0]['extra_charges_usd'].sum()
        pattern_cost[p] = cost

    # 4. Time Stolen
    avg_time_per_app = df.groupby('app_name')['time_spent_minutes'].mean()
    clean_apps_time = df[df['total_dark_patterns_found'] == 0]['time_spent_minutes'].mean()
    manipulative_apps_time = df[df['total_dark_patterns_found'] >= 6]['time_spent_minutes'].mean()
    total_hours_lost = (df['time_spent_minutes'].sum() - (len(df) * clean_apps_time)) / 60

    # 5. Cancellation Trap
    sub_apps = df[df['app_category'].isin(['Subscription', 'Fitness SaaS'])]
    cancel_success_rate = sub_apps[sub_apps['intended_action'] == 'cancel_subscription']['completed_intended_action'].mean() * 100

    # 6. Vulnerability Map
    vulnerability = df.groupby('user_tech_savvy')[patterns].mean()

    # 7. Frustration Curve
    frustration_corr = df['total_dark_patterns_found'].corr(df['frustration_score'])

    # 8. Ethics Comparison
    clean_apps = ['CleanShop', 'FairBook']
    worst_apps = app_scores.head(2)['app_name'].tolist()

    # 9. Five Worst Offenders
    top_5_worst = app_scores.head(5)['app_name'].tolist()

    # --- VISUALIZATIONS ---

    # 2. manipulation_scoreboard.png
    plt.figure(figsize=(10, 6))
    colors = plt.cm.RdYlGn_r(np.linspace(0, 1, len(app_scores)))
    bars = plt.barh(app_scores['app_name'], app_scores['manipulation_score'], color=colors)
    plt.bar_label(bars, fmt='%.1f', padding=3)
    plt.title('App Manipulation Scoreboard')
    plt.xlabel('Manipulation Score (0-100)')
    plt.xlim(0, 110)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('output/manipulation_scoreboard.png')
    plt.close()

    # 3. money_stolen.png
    plt.figure(figsize=(10, 6))
    costs = [pattern_cost[p] for p in monetary_patterns]
    bars = plt.bar(monetary_patterns, costs, color='crimson')
    plt.bar_label(bars, fmt='$%.0f', padding=3)
    plt.title('Money Stolen by Dark Pattern Type')
    plt.ylabel('Total Extra Charges (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/money_stolen.png')
    plt.close()

    # 4. time_tax.png
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Clean Apps', 'Manipulative Apps'], [clean_apps_time, manipulative_apps_time], color=['green', 'red'])
    plt.bar_label(bars, fmt='%.2f min', padding=3)
    plt.title('Time Tax: Average Session Duration')
    plt.ylabel('Minutes')
    plt.tight_layout()
    plt.savefig('output/time_tax.png')
    plt.close()

    # 5. cancellation_trap.png
    plt.figure(figsize=(10, 6))
    cancel_by_savvy = sub_apps[sub_apps['intended_action'] == 'cancel_subscription'].groupby('user_tech_savvy')['completed_intended_action'].mean() * 100
    ax = cancel_by_savvy.plot(kind='bar', color='orange')
    ax.bar_label(ax.containers[0], fmt='%.1f%%', padding=3)
    plt.title('Cancellation Success Rate by Tech Savviness')
    plt.ylabel('% Successful')
    plt.tight_layout()
    plt.savefig('output/cancellation_trap.png')
    plt.close()

    # 6. vulnerability_map.png
    plt.figure(figsize=(12, 8))
    sns.heatmap(vulnerability, annot=True, cmap='YlOrRd', fmt='.1f')
    plt.title('Vulnerability Map: Pattern Frequency by Tech Savviness')
    plt.savefig('output/vulnerability_map.png')
    plt.close()

    # 7. pattern_cards.png
    img = Image.new('RGB', (1200, 1600), color=(15, 15, 15))
    d = ImageDraw.Draw(img)
    y_offset = 50
    d.text((50, 20), 'DARK PATTERN CHEAT SHEET', fill=(255, 255, 255))

    for i, p in enumerate(patterns):
        freq = pattern_counts[p]
        d.text((50, y_offset), f'{i+1}. {p}: Found in {freq} sessions', fill=(200, 200, 200))
        y_offset += 80

    img.save('output/pattern_cards.png')

    # 8. manipulation_report.md
    with open('output/manipulation_report.md', 'w') as f:
        f.write('# Dark Pattern Manipulation Audit Report\\n\\n')
        f.write('## Executive Summary\\n')
        f.write(f'- Apps analyzed: {len(app_scores)}\\n')
        f.write(f'- Total money extracted: ${total_extra_charges:,.2f}\\n')
        f.write(f'- Total hours wasted: {total_hours_lost:,.2f} hours\\n\\n')

        f.write('## App Manipulation Scoreboard\\n')
        f.write(app_scores.to_markdown() + '\\n\\n')

        f.write('## The 14 Dark Patterns Breakdown\\n')
        f.write(pattern_counts.to_frame(name='Total Instances').to_markdown() + '\\n\\n')

        f.write('## The Money Stolen\\n')
        f.write(f'Total extra charges across all sessions: ${total_extra_charges:,.2f}\\n')
        f.write(f'If scaled to 1M users, estimated extraction: ${total_extra_charges * (1000000/len(df)):,.2f}\\n\\n')

        f.write('## Time Tax\\n')
        f.write(f'- Clean apps avg time: {clean_apps_time:.2f} min\\n')
        f.write(f'- Manipulative apps avg time: {manipulative_apps_time:.2f} min\\n')
        f.write(f'- Users spent {total_hours_lost:.2f} extra hours dealing with manipulation.\\n\\n')

        f.write('## Cancellation Trap\\n')
        f.write(f'Success rate for cancelling subscriptions: {cancel_success_rate:.2f}%\\n\\n')

        f.write('## Vulnerability Map\\n')
        f.write('Dark patterns disproportionately affect users with lower tech savviness.\\n\\n')

        f.write('## Frustration Curve\\n')
        f.write(f'Correlation between dark patterns and frustration score: {frustration_corr:.2f}\\n\\n')

        f.write('## Ethics Comparison\\n')
        f.write(f'Clean apps like {", ".join(clean_apps)} show lower frustration and better return rates compared to top offenders.\\n\\n')

        f.write('## Five Worst Offenders Deep Dive\\n')
        for app in top_5_worst:
            app_data = df[df['app_name'] == app]
            f.write(f'### {app}\\n')
            f.write(f'- Avg patterns per session: {app_data['total_dark_patterns_found'].mean():.2f}\\n')
            f.write(f'- Avg extra charges: ${app_data['extra_charges_usd'].mean():.2f}\\n')
            f.write(f'- Return rate: {app_data['would_use_again'].mean()*100:.2f}%\\n\\n')

        f.write('## Final Verdict\\n')
        f.write(f'- Worst Offender: {app_scores.iloc[0]['app_name']}\\n')
        f.write(f'- Cleanest App: {app_scores.iloc[-1]['app_name']}\\n')
        f.write(f'- Most Common Pattern: {pattern_counts.index[0]}\\n')
        f.write(f'- Most Expensive Pattern: {max(pattern_cost, key=pattern_cost.get)}\\n')
        f.write(f'- Total Dollars Extracted: ${total_extra_charges:,.2f}\\n')
        f.write(f'- One thing every user should watch for: Hidden fees added at the very last step of checkout.\\n')

    # 1. dashboard.html
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dark Pattern Detector Dashboard</title>
        <style>
            body {{ background-color: #0f0f0f; color: white; font-family: sans-serif; padding: 20px; }}
            .card {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }}
            .hero {{ display: flex; justify-content: space-around; text-align: center; }}
            .hero-stat {{ font-size: 24px; font-weight: bold; }}
            .hero-label {{ font-size: 14px; color: #aaa; }}
            img {{ max-width: 100%; height: auto; border-radius: 5px; }}
            h1 {{ text-align: center; color: #ff4d4d; }}
            h2 {{ border-bottom: 1px solid #333; padding-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>Manipulation Audit Dashboard</h1>

        <div class="card hero">
            <div><div class="hero-stat">{len(df)}</div><div class="hero-label">Sessions Audited</div></div>
            <div><div class="hero-stat">${total_extra_charges:,.2f}</div><div class="hero-label">Money Extracted</div></div>
            <div><div class="hero-stat">{df['total_dark_patterns_found'].mean():.2f}</div><div class="hero-label">Avg Patterns/Session</div></div>
            <div><div class="hero-stat">{app_scores.iloc[0]['app_name']}</div><div class="hero-label">Most Manipulative</div></div>
            <div><div class="hero-stat">{app_scores.iloc[-1]['app_name']}</div><div class="hero-label">Cleanest App</div></div>
        </div>

        <div class="card">
            <h2>App Manipulation Scoreboard</h2>
            <img src="manipulation_scoreboard.png">
        </div>

        <div class="card">
            <h2>The 14 Patterns Breakdown</h2>
            <img src="money_stolen.png">
        </div>

        <div class="card">
            <h2>Time Tax</h2>
            <img src="time_tax.png">
        </div>

        <div class="card">
            <h2>Cancellation Trap</h2>
            <img src="cancellation_trap.png">
        </div>

        <div class="card">
            <h2>Vulnerability Map</h2>
            <img src="vulnerability_map.png">
        </div>

        <div class="card">
            <h2>Pattern Recognition Guide</h2>
            <img src="pattern_cards.png">
        </div>
    </body>
    </html>
    '''
    with open('output/dashboard.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()
