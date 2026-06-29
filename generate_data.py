import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Parameters
num_products = 500
num_days = 90
categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty & Personal Care', 'Sports & Fitness']
brands = ['Brand_A', 'Brand_B', 'Brand_C', 'Brand_D', 'Brand_E', 'Brand_F', 'Brand_G']

# Generate Product Master Data
product_ids = [f'PROD_{i:04d}' for i in range(1, num_products + 1)]
product_data = {
    'ProductID': product_ids,
    'Category': np.random.choice(categories, num_products),
    'Brand': np.random.choice(brands, num_products),
    'BasePrice': np.random.uniform(100, 5000, num_products),
    'CostPrice': np.random.uniform(50, 3000, num_products),
    'StockQuantity': np.random.randint(10, 1000, num_products)
}
df_products = pd.DataFrame(product_data)
df_products['CostPrice'] = df_products['BasePrice'] * np.random.uniform(0.5, 0.8, num_products)

# Generate Daily Transactional/Scraping Data
dates = [datetime(2026, 1, 1) + timedelta(days=i) for i in range(num_days)]
rows = []

for date in dates:
    is_promo = (date.day >= 10 and date.day <= 15) or (date.day >= 25) 
    for _, prod in df_products.iterrows():
        discount_pct = np.random.uniform(0, 0.1)
        if is_promo:
            discount_pct += np.random.uniform(0.1, 0.3)
        
        selling_price = prod['BasePrice'] * (1 - discount_pct)
        base_sales = np.random.randint(0, 20)
        promo_lift = 2 if is_promo else 1
        sales_volume = int(base_sales * promo_lift * (1 + discount_pct * 2))
        
        quality_factor = np.random.uniform(0.6, 1.0)
        rating = np.clip(5 * quality_factor - (discount_pct * 0.5) + np.random.normal(0, 0.2), 1, 5)
        review_count = np.random.randint(0, 100) if sales_volume > 0 else 0
        return_rate = np.random.uniform(0.01, 0.15) if quality_factor < 0.8 else np.random.uniform(0.01, 0.05)

        rows.append({
            'Date': date,
            'ProductID': prod['ProductID'],
            'Category': prod['Category'],
            'Brand': prod['Brand'],
            'BasePrice': prod['BasePrice'],
            'SellingPrice': selling_price,
            'DiscountPct': discount_pct,
            'SalesVolume': sales_volume,
            'Rating': round(rating, 1),
            'ReviewCount': review_count,
            'ReturnRate': round(return_rate, 3),
            'StockValue': prod['StockQuantity'] * selling_price
        })

df_final = pd.DataFrame(rows)
df_final.to_csv('snapdeal_data.csv', index=False)
print("Dataset 'snapdeal_data.csv' generated successfully.")
