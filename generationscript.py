import pandas as pd
import random
from datetime import datetime, timedelta

# Define categories and percentages
categories = {
    "Utilities": 10,
    "Entertainment": 10,
    "Food": 15,
    "Banking (Debt/Savings)": 10,
    "Transportation": 10,
    "Insurance": 10,
    "Housing": 10,
    "Education": 5,
    "Subscriptions": 10,
    "Other": 10,
}

# Generate descriptions for each category
descriptions = {
    "Utilities": ["Electricity Bill", "Water Bill", "Gas Bill", "Internet Bill"],
    "Entertainment": ["Movie Night", "Concert", "Streaming Service"],
    "Food": ["Groceries", "Restaurant", "Coffee Shop", "Fast Food"],
    "Banking (Debt/Savings)": ["Savings Deposit", "Credit Card Payment"],
    "Transportation": ["Gas", "Public Transit", "Car Maintenance", "Ride Share"],
    "Insurance": ["Health Insurance", "Car Insurance", "Home Insurance"],
    "Housing": ["Mortgage", "Rent", "Property Maintenance"],
    "Education": ["School Fees", "Books", "Online Course"],
    "Subscriptions": ["Netflix", "Gym Membership", "Cloud Storage"],
    "Other": ["Unexpected Repair", "Gift", "Miscellaneous Purchase"],
}

# Helper function to generate random dates over 10 years
start_date = datetime(2014, 1, 1)
end_date = datetime(2024, 1, 1)
date_range = (end_date - start_date).days

def random_date():
    return start_date + timedelta(days=random.randint(0, date_range))

# Generate dataset
data = []
recurring_expenses = {
    "Netflix": ("Subscriptions", 15),
    "Mortgage": ("Housing", 1500),
    "Electricity Bill": ("Utilities", 100),
    "Gym Membership": ("Subscriptions", 30),
}

for i in range(12000):
    if random.random() < 0.1:  # 10% for unexpected (Other)
        category = "Other"
    else:
        category = random.choices(list(categories.keys()), weights=list(categories.values()), k=1)[0]
    
    # Add recurring expenses at fixed intervals (e.g., monthly)
    if i % 100 == 0:
        for desc, (cat, cost) in recurring_expenses.items():
            data.append({
                "Expense": cost,
                "Description": desc,
                "Category": cat,
                "Date": random_date().strftime("%Y-%m-%d")
            })
    
    description = random.choice(descriptions[category])
    expense = round(random.uniform(10, 500), 2) if category != "Other" else round(random.uniform(20, 100), 2)
    date = random_date().strftime("%Y-%m-%d")
    data.append({"Expense": expense, "Description": description, "Category": category, "Date": date})

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
csv_path = "expenses_2024.csv"
df.to_csv(csv_path, index=False)

csv_path
