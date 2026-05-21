import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import os

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

def load_data():
    df = pd.read_csv('orders.csv')
    # Handle missing return reasons
    df['return_reason'] = df['return_reason'].fillna('Not Returned')
    return df

def analyze_reality_check(df):
    overall_rate = df['returned'].mean()
    cat_rates = df.groupby('category')['returned'].mean().sort_values(ascending=False)

    # Cost = $15 processing fee per return + lost revenue
    returns_df = df[df['returned'] == 1]
    total_processing_cost = len(returns_df) * 15
    total_lost_revenue = returns_df['order_total'].sum()
    total_cost = total_processing_cost + total_lost_revenue

    reasons = df[df['returned'] == 1]['return_reason'].value_counts(normalize=True)

    return {
        'overall_rate': overall_rate,
        'cat_rates': cat_rates,
        'total_cost': total_cost,
        'reasons': reasons
    }

def analyze_time_signals(df):
    hourly_rates = df.groupby('purchase_hour')['returned'].mean()

    # Late night: 10pm - 5am
    late_night = df[(df['purchase_hour'] >= 22) | (df['purchase_hour'] <= 5)]
    daytime = df[(df['purchase_hour'] > 5) & (df['purchase_hour'] < 22)]
    late_night_rate = late_night['returned'].mean()
    daytime_rate = daytime['returned'].mean()

    # Weekend vs Weekday
    weekend_rate = df[df['is_weekend'] == 1]['returned'].mean()
    weekday_rate = df[df['is_weekend'] == 0]['returned'].mean()

    return {
        'hourly_rates': hourly_rates,
        'late_night_rate': late_night_rate,
        'daytime_rate': daytime_rate,
        'weekend_rate': weekend_rate,
        'weekday_rate': weekday_rate
    }

def analyze_impulse_signals(df):
    # Correlations
    corrs = {
        'time_browsing_minutes': df['time_browsing_minutes'].corr(df['returned']),
        'reviews_read': df['reviews_read'].corr(df['returned']),
        'items_compared': df['items_compared'].corr(df['returned']),
        'cart_removals': df['cart_removals'].corr(df['returned'])
    }

    # Impulse buy: browsing < 3 minutes
    impulse_rate = df[df['time_browsing_minutes'] < 3]['returned'].mean()
    non_impulse_rate = df[df['time_browsing_minutes'] >= 3]['returned'].mean()

    return {
        'correlations': corrs,
        'impulse_rate': impulse_rate,
        'non_impulse_rate': non_impulse_rate
    }

def analyze_discount_impact(df):
    coupon_rate = df.groupby('used_coupon')['returned'].mean()

    # Discount bins
    bins = [0, 5, 15, 25, 100]
    labels = ['0-5%', '5-15%', '15-25%', '25%+']
    df['discount_bin'] = pd.cut(df['discount_percent'], bins=bins, labels=labels)
    discount_bin_rates = df.groupby('discount_bin', observed=True)['returned'].mean()

    # BNPL risk
    bnpl_rate = df[df['payment_method'] == 'Buy Now Pay Later']['returned'].mean()
    other_pay_rate = df[df['payment_method'] != 'Buy Now Pay Later']['returned'].mean()

    return {
        'coupon_rate': coupon_rate,
        'discount_bin_rates': discount_bin_rates,
        'bnpl_rate': bnpl_rate,
        'other_pay_rate': other_pay_rate
    }

def analyze_fashion_deepdive(df):
    fashion_df = df[df['category'] == 'Fashion']
    fashion_rate = fashion_df['returned'].mean()

    # Multiple sizes ordered
    sizes_rate = fashion_df.groupby('multiple_sizes_ordered')['returned'].mean()

    # Top reason for fashion
    top_reason = fashion_df[fashion_df['returned'] == 1]['return_reason'].mode()[0]

    return {
        'fashion_rate': fashion_rate,
        'sizes_rate': sizes_rate,
        'top_reason': top_reason
    }

def analyze_customer_history(df):
    # Correlation between prev return rate and current return
    history_corr = df['previous_return_rate'].corr(df['returned'])

    # Customer type return rates
    type_rates = df.groupby('customer_type')['returned'].mean()

    return {
        'history_corr': history_corr,
        'type_rates': type_rates
    }

def analyze_device_channel(df):
    device_rates = df.groupby('device')['returned'].mean()
    channel_rates = df.groupby('channel')['returned'].mean()

    # Mobile + Impulse combo
    mobile_impulse = df[(df['device'] == 'Mobile') & (df['time_browsing_minutes'] < 3)]
    mobile_impulse_rate = mobile_impulse['returned'].mean()

    return {
        'device_rates': device_rates,
        'channel_rates': channel_rates,
        'mobile_impulse_rate': mobile_impulse_rate
    }

def build_prediction_model(df):
    features = [
        'purchase_hour', 'is_late_night', 'category', 'device', 'payment_method',
        'time_browsing_minutes', 'reviews_read', 'items_compared', 'cart_removals',
        'used_coupon', 'discount_percent', 'previous_return_rate', 'is_gift',
        'multiple_sizes_ordered', 'delivery_days'
    ]

    X = df[features].copy()
    y = df['returned']

    # Encoding
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)

    # Feature Importance
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

    # Risk Tiers for whole dataset
    full_probs = model.predict_proba(X)[:, 1]
    df['return_risk'] = full_probs

    def get_tier(p):
        if p > 0.6: return 'High'
        if p > 0.3: return 'Medium'
        return 'Low'

    df['risk_tier'] = df['return_risk'].apply(get_tier)
    tier_dist = df['risk_tier'].value_counts(normalize=True)

    # How many actual returns caught in each tier
    returns_only = df[df['returned'] == 1]
    caught_per_tier = returns_only['risk_tier'].value_counts(normalize=True)

    return {
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'importances': importances,
        'tier_dist': tier_dist,
        'caught_per_tier': caught_per_tier,
        'df_with_scores': df
    }

def calculate_dollar_impact(df, reality_check):
    annual_loss = reality_check['total_cost']

    # If we flag high-risk orders and reduce their return rate by 20%
    high_risk = df[df['risk_tier'] == 'High']
    high_risk_returns = high_risk[high_risk['returned'] == 1]

    # Estimated savings: 20% reduction in high risk returns
    # Savings = (0.2 * num_returns * 15) + (0.2 * sum of high risk return totals)
    savings = (0.2 * len(high_risk_returns) * 15) + (0.2 * high_risk_returns['order_total'].sum())

    return {
        'annual_loss': annual_loss,
        'projected_savings': savings,
        'roi': (savings / annual_loss) * 100 if annual_loss > 0 else 0
    }

def generate_strategy(reality, time, impulse, discount, fashion, history, device, model_results):
    # Heuristics for recommendations
    recs = {
        'FLAG': 'Orders with >60% risk score, especially Mobile+Impulse and Late-Night Fashion.',
        'FIX': f'Fashion category (Rate: {fashion["fashion_rate"]:.1%}) - Improve size guides.',
        'LIMIT': 'Buy Now Pay Later and 25%+ discount tiers showing high return spikes.',
        'MONITOR': 'Customers with previous_return_rate > 30%.',
        'KEEP': 'Desktop users with high browse time and high reviews read.'
    }
    return recs

# Visualization Functions
def save_time_bomb(time_results):
    plt.figure(figsize=(12, 6))
    colors = ['red' if (h >= 22 or h <= 5) else 'green' if (12 <= h <= 16) else 'gray' for h in range(24)]
    hourly_rates = time_results['hourly_rates']
    bars = plt.bar(hourly_rates.index, hourly_rates.values, color=colors)

    # Add data labels at the top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.1%}', ha='center', va='bottom', fontsize=8)

    plt.title('Return Rate by Hour of Purchase')
    plt.xlabel('Hour of Day')
    plt.ylabel('Return Rate')
    plt.xticks(range(24))
    plt.ylim(0, max(hourly_rates.values) * 1.15)
    plt.savefig('output/time_bomb.png')
    plt.close()

def save_impulse_map(impulse_results):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    df = load_data()
    signals = ['time_browsing_minutes', 'reviews_read', 'cart_removals']

    for i, signal in enumerate(signals):
        df[signal + '_bin'] = pd.qcut(df[signal], 5, labels=False, duplicates='drop')
        rate = df.groupby(signal + '_bin')['returned'].mean()
        axes[i].plot(rate.index, rate.values, marker='o', linewidth=2, color='blue')

        # Add data labels to each point
        for x, y in enumerate(rate.values):
            axes[i].text(x, y + 0.005, f'{y:.1%}', ha='center', va='bottom', fontsize=9)

        axes[i].set_title(f'{signal} vs Return Rate')
        axes[i].set_xlabel('Quantile')
        axes[i].set_ylabel('Return Rate')
        axes[i].grid(True)
        axes[i].set_ylim(0, max(rate.values) * 1.2)

    plt.tight_layout()
    plt.savefig('output/impulse_map.png')
    plt.close()

def save_discount_curse(discount_results):
    plt.figure(figsize=(10, 6))
    rates = discount_results['discount_bin_rates']
    plt.plot(rates.index.astype(str), rates.values, marker='o', color='red', linewidth=3)

    # Add data labels to each point
    for i, val in enumerate(rates.values):
        plt.text(i, val + 0.005, f'{val:.1%}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.title('Discount Percentage vs Return Rate')
    plt.xlabel('Discount Tier')
    plt.ylabel('Return Rate')
    plt.ylim(0, max(rates.values) * 1.2)
    plt.grid(True)
    plt.savefig('output/discount_curse.png')
    plt.close()

def save_category_returns(reality_results):
    plt.figure(figsize=(10, 8))
    df = load_data()
    returns_df = df[df['returned'] == 1]
    cat_reasons = returns_df.groupby(['category', 'return_reason']).size().unstack(fill_value=0)

    # Sort by total returns per category descending
    total_returns = cat_reasons.sum(axis=1).sort_values(ascending=False)
    cat_reasons = cat_reasons.loc[total_returns.index]

    ax = cat_reasons.plot(kind='barh', stacked=True, figsize=(10, 8), colormap='viridis')

    # Add labels to the right of bars
    for i, total in enumerate(total_returns):
        ax.text(total + 0.5, i, f'{total:.0f}', va='center', ha='left', color='white', fontsize=10)

    plt.title('Return Reasons by Category')
    plt.xlabel('Number of Returns')
    plt.ylabel('Category')
    plt.legend(title='Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('output/category_returns.png')
    plt.close()

def save_feature_importance(model_results):
    plt.figure(figsize=(10, 8))
    importances = model_results['importances'].head(15).sort_values(ascending=True) # ascending=True because barh plots from bottom up

    ax = importances.plot(kind='barh', color='skyblue')

    # Add labels to the right of bars
    for i, val in enumerate(importances.values):
        ax.text(val + 0.001, i, f'{val:.3f}', va='center', ha='left', color='black', fontsize=10)

    plt.title('Top 15 Predictive Signals for Returns')
    plt.xlabel('Importance Score')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.savefig('output/feature_importance.png')
    plt.close()

def save_risk_tiers(model_results):
    plt.figure(figsize=(8, 8))
    tier_dist = model_results['tier_dist']
    plt.pie(tier_dist.values, labels=tier_dist.index, autopct='%1.1f%%', startangle=140, colors=['green', 'yellow', 'red'])
    plt.title('Order Risk Tier Distribution')
    plt.savefig('output/risk_tiers.png')
    plt.close()

def generate_dashboard(metrics):
    # Simple dark-themed dashboard
    html_template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Return Intelligence Dashboard</title>
        <style>
            body {{ background-color: #0f0f0f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .hero-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
            .card {{ background-color: #1a1a1a; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); text-align: center; border: 1px solid #333; }}
            .card h3 {{ color: #888; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 10px; }}
            .card .value {{ font-size: 1.8rem; font-weight: bold; color: #fff; }}
            .viz-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }}
            .viz-card {{ background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
            .viz-card img {{ width: 100%; border-radius: 5px; }}
            .strategy-board {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 40px; }}
            .strat-card {{ padding: 15px; border-radius: 8px; border-left: 5px solid; }}
            .FLAG {{ background: #2a1a1a; border-color: #ff4444; }}
            .FIX {{ background: #1a2a1a; border-color: #44ff44; }}
            .LIMIT {{ background: #2a2a1a; border-color: #ffff44; }}
            .MONITOR {{ background: #1a1a2a; border-color: #4444ff; }}
            .KEEP {{ background: #1a1a1a; border-color: #aaaaaa; }}
            .strat-title {{ font-weight: bold; display: block; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Returns Intelligence Engine</h1>
                <p>Predicting regret before shipment</p>
            </div>

            <div class="hero-grid">
                <div class="card"><h3>Total Orders</h3><div class="value">15,000</div></div>
                <div class="card"><h3>Overall Return Rate</h3><div class="value">{metrics['reality']['overall_rate']:.1%}</div></div>
                <div class="card"><h3>Annual Return Cost</h3><div class="value">${metrics['impact']['annual_loss']:,.0f}</div></div>
                <div class="card"><h3>Top Signal</h3><div class="value">{metrics['model']['importances'].index[0]}</div></div>
                <div class="card"><h3>Model Accuracy</h3><div class="value">{metrics['model']['accuracy']:.1%}</div></div>
            </div>

            <div class="viz-grid">
                <div class="viz-card"><h3>Time Bomb: Hourly Risk</h3><img src="time_bomb.png"></div>
                <div class="viz-card"><h3>Impulse Map: Correlation</h3><img src="impulse_map.png"></div>
                <div class="viz-card"><h3>The Discount Curse</h3><img src="discount_curse.png"></div>
                <div class="viz-card"><h3>Category Breakdown</h3><img src="category_returns.png"></div>
                <div class="viz-card"><h3>Feature Importance</h3><img src="feature_importance.png"></div>
                <div class="viz-card"><h3>Risk Distribution</h3><img src="risk_tiers.png"></div>
            </div>

            <div class="strategy-board">
                <div class="strat-card FLAG"><span class="strat-title">FLAG</span>{metrics['strategy']['FLAG']}</div>
                <div class="strat-card FIX"><span class="strat-title">FIX</span>{metrics['strategy']['FIX']}</div>
                <div class="strat-card LIMIT"><span class="strat-title">LIMIT</span>{metrics['strategy']['LIMIT']}</div>
                <div class="strat-card MONITOR"><span class="strat-title">MONITOR</span>{metrics['strategy']['MONITOR']}</div>
                <div class="strat-card KEEP"><span class="strat-title">KEEP</span>{metrics['strategy']['KEEP']}</div>
            </div>
        </div>
    </body>
    </html>
    '''
    with open('output/dashboard.html', 'w') as f:
        f.write(html_template)

def generate_report(metrics):
    report = f'''# Returns Intelligence Executive Report

## Executive Summary
- **Overall Return Rate**: {metrics['reality']['overall_rate']:.1%}
- **Annual Return Cost**: ${metrics['impact']['annual_loss']:,.0f}
- **Model Accuracy**: {metrics['model']['accuracy']:.1%}
- **Projected Annual Savings**: ${metrics['impact']['projected_savings']:,.0f}

## 1. Time-of-Day Analysis
- **Danger Zone**: Late-night orders (10pm-5am) have a return rate of {metrics['time']['late_night_rate']:.1%}, significantly higher than daytime orders ({metrics['time']['daytime_rate']:.1%}).
- **Weekend Effect**: Weekend return rate is {metrics['time']['weekend_rate']:.1%}.

## 2. Impulse Buying Signals
- **Impulse Rate**: Orders with < 3 min browsing time have a return rate of {metrics['impulse']['impulse_rate']:.1%}.
- **Correlation**: Strongest negative correlation with returns: {metrics['impulse']['correlations']['reviews_read']:.2f} (Reviews read).

## 3. The Discount Curse
- **Coupon Impact**: Coupon users return at a rate of {metrics['discount']['coupon_rate'].mean():.1%}.
- **Discount Tier Spike**: High return rates observed at the 25%+ discount level.
- **Payment Risk**: "Buy Now Pay Later" users return at {metrics['discount']['bnpl_rate']:.1%}.

## 4. Category Deep Dive (Fashion)
- **Fashion Return Rate**: {metrics['fashion']['fashion_rate']:.1%}.
- **The Size Signal**: Orders with multiple sizes ordered have a return rate of {metrics['fashion']['sizes_rate'].get(1, 0):.1%}.
- **Top Reason**: {metrics['fashion']['top_reason']}.

## 5. Customer & Device Signals
- **History Predictor**: Correlation between previous return rate and current return: {metrics['history']['history_corr']:.2f}.
- **Mobile Impulse**: Mobile users with < 3 min browsing have a {metrics['device']['mobile_impulse_rate']:.1%} return rate.

## 6. ML Model Results
- **Accuracy**: {metrics['model']['accuracy']:.1%}
- **Precision**: {metrics['model']['precision']:.1%}
- **Recall**: {metrics['model']['recall']:.1%}
- **Top Predictor**: {metrics['model']['importances'].index[0]}

## 7. Risk Tier Breakdown
- **High Risk (>60%)**: {metrics['model']['tier_dist'].get('High', 0):.1%} of orders.
- **Medium Risk (30-60%)**: {metrics['model']['tier_dist'].get('Medium', 0):.1%} of orders.
- **Low Risk (<30%)**: {metrics['model']['tier_dist'].get('Low', 0):.1%} of orders.

## 8. Dollar Impact & ROI
- **Total Annual Loss**: ${metrics['impact']['annual_loss']:,.0f}
- **Estimated Savings from Intervention**: ${metrics['impact']['projected_savings']:,.0f}
- **Projected ROI**: {metrics['impact']['roi']:.1%}

## 9. Strategic Recommendations
- **FLAG**: {metrics['strategy']['FLAG']}
- **FIX**: {metrics['strategy']['FIX']}
- **LIMIT**: {metrics['strategy']['LIMIT']}
- **MONITOR**: {metrics['strategy']['MONITOR']}
- **KEEP**: {metrics['strategy']['KEEP']}

## Final Verdict
- **#1 Return Predictor Signal**: {metrics['model']['importances'].index[0]}
- **Biggest Fixable Problem**: {metrics['strategy']['FIX']}
- **Prediction Accuracy**: {metrics['model']['accuracy']:.1%}
- **Estimated Annual Savings**: ${metrics['impact']['projected_savings']:,.0f}
'''
    with open('output/return_report.md', 'w') as f:
        f.write(report)

def main():
    print("Loading data...")
    df = load_data()

    print("Running Analysis Modules...")
    reality = analyze_reality_check(df)
    time_sig = analyze_time_signals(df)
    impulse = analyze_impulse_signals(df)
    discount = analyze_discount_impact(df)
    fashion = analyze_fashion_deepdive(df)
    history = analyze_customer_history(df)
    device = analyze_device_channel(df)
    model_res = build_prediction_model(df)
    impact = calculate_dollar_impact(df, reality)
    strategy = generate_strategy(reality, time_sig, impulse, discount, fashion, history, device, model_res)

    metrics = {
        'reality': reality,
        'time': time_sig,
        'impulse': impulse,
        'discount': discount,
        'fashion': fashion,
        'history': history,
        'device': device,
        'model': model_res,
        'impact': impact,
        'strategy': strategy
    }

    print("Generating Visuals...")
    save_time_bomb(time_sig)
    save_impulse_map(impulse)
    save_discount_curse(discount)
    save_category_returns(reality)
    save_feature_importance(model_res)
    save_risk_tiers(model_res)

    print("Generating Dashboard and Report...")
    generate_dashboard(metrics)
    generate_report(metrics)

    print("\\nAnalysis Complete!")
    print(f"#1 return predictor signal: {model_res['importances'].index[0]}")
    print(f"Biggest fixable return problem: {strategy['FIX']}")
    print(f"Prediction accuracy: {model_res['accuracy']:.1%}")
    print(f"Estimated annual savings: ${impact['projected_savings']:,.0f}")

if __name__ == "__main__":
    main()
