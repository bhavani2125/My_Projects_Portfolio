# Returns Intelligence Executive Report

## Executive Summary
- **Overall Return Rate**: 25.9%
- **Annual Return Cost**: $996,379
- **Model Accuracy**: 77.2%
- **Projected Annual Savings**: $166,374

## 1. Time-of-Day Analysis
- **Danger Zone**: Late-night orders (10pm-5am) have a return rate of 33.7%, significantly higher than daytime orders (22.0%).
- **Weekend Effect**: Weekend return rate is 27.8%.

## 2. Impulse Buying Signals
- **Impulse Rate**: Orders with < 3 min browsing time have a return rate of 50.4%.
- **Correlation**: Strongest negative correlation with returns: -0.06 (Reviews read).

## 3. The Discount Curse
- **Coupon Impact**: Coupon users return at a rate of 27.2%.
- **Discount Tier Spike**: High return rates observed at the 25%+ discount level.
- **Payment Risk**: "Buy Now Pay Later" users return at 36.0%.

## 4. Category Deep Dive (Fashion)
- **Fashion Return Rate**: 47.0%.
- **The Size Signal**: Orders with multiple sizes ordered have a return rate of 71.0%.
- **Top Reason**: Wrong Size.

## 5. Customer & Device Signals
- **History Predictor**: Correlation between previous return rate and current return: 0.12.
- **Mobile Impulse**: Mobile users with < 3 min browsing have a 55.2% return rate.

## 6. ML Model Results
- **Accuracy**: 77.2%
- **Precision**: 62.5%
- **Recall**: 29.5%
- **Top Predictor**: time_browsing_minutes

## 7. Risk Tier Breakdown
- **High Risk (>60%)**: 21.7% of orders.
- **Medium Risk (30-60%)**: 6.8% of orders.
- **Low Risk (<30%)**: 71.5% of orders.

## 8. Dollar Impact & ROI
- **Total Annual Loss**: $996,379
- **Estimated Savings from Intervention**: $166,374
- **Projected ROI**: 1669.8%

## 9. Strategic Recommendations
- **FLAG**: Orders with >60% risk score, especially Mobile+Impulse and Late-Night Fashion.
- **FIX**: Fashion category (Rate: 47.0%) - Improve size guides.
- **LIMIT**: Buy Now Pay Later and 25%+ discount tiers showing high return spikes.
- **MONITOR**: Customers with previous_return_rate > 30%.
- **KEEP**: Desktop users with high browse time and high reviews read.

## Final Verdict
- **#1 Return Predictor Signal**: time_browsing_minutes
- **Biggest Fixable Problem**: Fashion category (Rate: 47.0%) - Improve size guides.
- **Prediction Accuracy**: 77.2%
- **Estimated Annual Savings**: $166,374
