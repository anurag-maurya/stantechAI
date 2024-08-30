WITH RecentOrders AS (
    SELECT 
        o.order_id, 
        o.customer_id, 
        oi.product_id, 
        oi.quantity, 
        oi.price_per_unit,
        p.category,
        o.order_date
    FROM 
        Orders o
    JOIN 
        Order_Items oi ON o.order_id = oi.order_id
    JOIN 
        Products p ON oi.product_id = p.product_id
    WHERE 
        o.order_date >= CURDATE() - INTERVAL 1 YEAR
),
CustomerSpending AS (
    SELECT 
        ro.customer_id, 
        SUM(ro.quantity * ro.price_per_unit) AS total_spent,
        ro.category,
        SUM(ro.quantity * ro.price_per_unit) OVER(PARTITION BY ro.customer_id, ro.category) AS category_spent
    FROM 
        RecentOrders ro
    GROUP BY 
        ro.customer_id, ro.category
),
TopCustomers AS (
    SELECT 
        cs.customer_id,
        MAX(cs.total_spent) AS total_spent,
        c.customer_name,
        c.email
    FROM 
        CustomerSpending cs
    JOIN 
        Customers c ON cs.customer_id = c.customer_id
    GROUP BY 
        cs.customer_id, c.customer_name, c.email
    ORDER BY 
        total_spent DESC
    LIMIT 5
),
CustomerCategories AS (
    SELECT
        cs.customer_id,
        cs.category,
        SUM(cs.category_spent) AS category_total_spent,
        ROW_NUMBER() OVER(PARTITION BY cs.customer_id ORDER BY SUM(cs.category_spent) DESC) AS rn
    FROM
        CustomerSpending cs
    GROUP BY
        cs.customer_id, cs.category
)
SELECT 
    tc.customer_id, 
    tc.customer_name, 
    tc.email, 
    tc.total_spent,
    cc.category AS most_purchased_category
FROM 
    TopCustomers tc
JOIN 
    CustomerCategories cc ON tc.customer_id = cc.customer_id AND cc.rn = 1
ORDER BY 
    tc.total_spent DESC;
