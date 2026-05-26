A full end-to-end business intelligence system analyzing an entire year of pizza restaurant sales data. This project combines SQL data engineering with Tableau executive dashboards to deliver actionable insights on revenue, product mix, and demand patterns.
▌ Project Overview
Domain	Food & Beverage / Retail Analytics
Tools Used	SQL (MySQL), Tableau, Microsoft Excel
Dataset	pizza_sales.csv — annual transaction records
Key Files	Pizza_Sales.twbx, Pizza_Sales_Best&Worst_Sellers, pizza_sales_queries.docx
Deliverable	Executive Tableau BI Dashboard + SQL Query Scripts
▌ Business Problem
•	The restaurant needed a data-driven view of its annual operations to understand which products drive revenue, when peak demand occurs, and which menu items should be promoted or discontinued.
▌ What I Did
•	Authored structured SQL scripts with multi-table joins, subqueries, GROUP BY aggregations, and window functions to clean and transform raw transaction logs into analytical datasets.: SQL Data Engineering
•	Built a Tableau workbook (Pizza_Sales.twbx) displaying headline KPIs: $817.9K Total Revenue, 21,350 Total Orders, 49,574 Total Pizzas Sold, and $38.31 Average Order Value.: Executive KPI Dashboard
•	Built hourly and weekly time-series models — identified peak demand windows at 12–1 PM and 4–7 PM, and a critical inventory spike in Week 48.: Demand Pattern Analysis
•	Engineered category and sizing breakdown matrices — Classic Pizza led with 10,859 orders ($220K revenue); Large Pizzas dominated at 45.89% of total volume.: Product Mix Segmentation
•	Designed a ranked visual isolating The Thai Chicken Pizza as #1 revenue contributor ($43.43K) and The Brie Carre Pizza as the lowest-volume underperformer.: Best & Worst Sellers Dashboard
▌ Key Insights
•	Friday and Saturday evenings are the highest revenue windows — optimal for staffing and promotions.
•	Classic and Supreme categories together account for over 50% of all revenue.
•	The bottom 5 pizzas represent an opportunity for menu rationalization or repositioning.
▌ SQL Query Examples
-- Total Revenue
SELECT ROUND(SUM(total_price), 2) AS Total_Revenue FROM pizza_sales;
-- Best Sellers by Revenue
SELECT pizza_name, SUM(total_price) AS revenue FROM pizza_sales GROUP BY pizza_name ORDER BY revenue DESC LIMIT 5;
▌ Files in This Project
📄 pizza_sales.csv  —  Raw annual transaction dataset
📄 pizza_sales_queries.docx  —  Complete SQL query scripts
📄 Pizza_Sales.twbx  —  Main Tableau executive dashboard
📄 Pizza_Sales_Best&Worst_Sellers  —  Ranked product performance dashboard
📄 Pizza_Sales_Home_Dashboard  —  Summary home view dashboard
