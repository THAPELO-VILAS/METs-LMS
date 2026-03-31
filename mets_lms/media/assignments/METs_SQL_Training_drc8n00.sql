
-- METs Academy SQL Training Script

-- 1. Total Sales
SELECT SUM(Sales) AS Total_Sales FROM sales_data;

-- 2. Sales by Region
SELECT Region, SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Region;

-- 3. Most Profitable Product
SELECT Product, SUM(Sales - Cost) AS Profit
FROM sales_data
GROUP BY Product
ORDER BY Profit DESC;

-- 4. Monthly Sales Trend
SELECT MONTH(Order_Date) AS Month, SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY MONTH(Order_Date)
ORDER BY Month;
