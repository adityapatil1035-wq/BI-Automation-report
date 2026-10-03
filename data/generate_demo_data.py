import csv
import random
import os
from datetime import datetime, timedelta

def generate_demo_dataset(output_path: str, num_records: int = 1200):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    categories = {
        "Electronics": ["Smartphone Pro Max", "Wireless Noise-Canceling Headphones", "4K Ultra Monitor 32-inch", "Mechanical Gaming Keyboard", "Smartwatch Series X", "Ergonomic Wireless Mouse"],
        "Furniture": ["Ergonomic Executive Chair", "Standing Height-Adjustable Desk", "Modern Bookshelf 5-Tier", "Leather Recliner Sofa", "Nordic Dining Table"],
        "Office Supplies": ["Premium Notebook Pack", "Gel Pen Box (Set of 12)", "Heavy Duty Stapler", "Desktop Document Organizer", "Whiteboard Marker Kit"],
        "Clothing": ["Performance Thermal Jacket", "Slim Fit Denim Jeans", "Breathable Running Shoes", "Cotton Oxford Shirt", "Winter Knit Beanie"]
    }
    
    regions = ["North", "South", "East", "West", "Central"]
    cities = {
        "North": ["Delhi", "Chandigarh", "Jaipur", "Lucknow"],
        "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi"],
        "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati"],
        "West": ["Mumbai", "Ahmedabad", "Pune", "Surat"],
        "Central": ["Bhopal", "Indore", "Nagpur", "Raipur"]
    }
    
    segments = ["Consumer", "Corporate", "Home Office", "Enterprise"]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 8, 31)
    date_range_days = (end_date - start_date).days

    records = []
    
    for i in range(1, num_records + 1):
        order_id = f"ORD-{2024 + (i % 3)}-{10000 + i}"
        random_days = random.randint(0, date_range_days)
        order_date = start_date + timedelta(days=random_days)
        
        customer_num = random.randint(101, 450)
        customer_id = f"CUST-{customer_num}"
        customer_name = f"Customer_{customer_num}"
        customer_segment = random.choice(segments)
        
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        region = random.choice(regions)
        city = random.choice(cities[region])
        
        quantity = random.randint(1, 15)
        
        # Price mapping
        base_prices = {
            "Electronics": (80.0, 1200.0),
            "Furniture": (150.0, 850.0),
            "Office Supplies": (10.0, 75.0),
            "Clothing": (25.0, 180.0)
        }
        
        low_p, high_p = base_prices[category]
        unit_price = round(random.uniform(low_p, high_p), 2)
        unit_cost = round(unit_price * random.uniform(0.55, 0.75), 2)
        
        discount_pct = random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25]) if random.random() > 0.4 else 0.0
        
        sales = round(quantity * unit_price * (1 - discount_pct), 2)
        cost = round(quantity * unit_cost, 2)
        profit = round(sales - cost, 2)
        
        # Inject occasional anomaly spike or drop for testing anomaly detection
        if i in [150, 420, 780, 1050]:
            sales = round(sales * 4.5, 2)
            profit = round(profit * 5.0, 2)
        elif i in [230, 610, 940]:
            profit = -round(abs(cost * 0.4), 2)  # Negative profit / loss anomaly

        # Inject some missing values intentionally in non-critical rows to test data cleaning
        if i % 180 == 0:
            discount_pct = ""  # missing discount
        if i % 250 == 0:
            customer_segment = ""  # missing segment

        records.append({
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Customer ID": customer_id,
            "Customer Name": customer_name,
            "Segment": customer_segment,
            "Category": category,
            "Product": product,
            "Region": region,
            "City": city,
            "Quantity": quantity,
            "Sales": sales,
            "Cost": cost,
            "Profit": profit,
            "Discount": discount_pct
        })
        
    # Sort by date
    records.sort(key=lambda x: x["Order Date"])
    
    headers = list(records[0].keys())
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Successfully generated {num_records} demo records at {output_path}")

if __name__ == "__main__":
    generate_demo_dataset("c:/Users/aadir/OneDrive/Desktop/BI Report Automation/data/retail_sales_demo.csv")
