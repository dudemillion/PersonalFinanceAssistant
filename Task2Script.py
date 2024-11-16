import csv
import os
import datetime
import collections
import pandas
import numpy
import plotly.express
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
data = []
fields = ["Expense", "Description", "Category", "Date"]
pandasdata = pandas.read_csv("expenses_2024.csv")
with open("expenses_2024.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.path.getsize("expenses_2024.csv") == 0:
            writer.writerow(fields)
def weekly_and_monthly_spending(show_output=True):
    weekly = collections.defaultdict(float)
    monthly = collections.defaultdict(float)
    with open("expenses_2024.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for y in reader:
            date = datetime.datetime.strptime(y["Date"], "%Y-%m-%d")
            week = date.strftime("%Y-%U")
            month = date.strftime("%Y-%m")
            expense = float(y["Expense"])
            weekly[week] += expense
            monthly[month] += expense
        sorted_weekly = dict(sorted(weekly.items()))
        sorted_monthly = dict(sorted(monthly.items()))
        if show_output:
            print("\nWeekly Spending:")
            for week, amount in sorted_weekly.items():
                print(f"Week {week}: ${amount:.2f}")
    
            print("\nMonthly Spending:")
            for month, amount in sorted_monthly.items():
                print(f"Month {month}: ${amount:.2f}")
    sorted_monthly = dict(sorted(monthly.items()))
    return sorted_monthly    
def monthly_speding_with_category():
     averageexpense = 0
     expenses = []
     months = []
     categories = []
     with open("expenses_2024.csv", "r") as csvfile:
          reader = csv.reader(csvfile)
          next(reader)
          for row in reader:
               expenses.append(float(row[0]))
               months.append(row[3].split("-")[1])
               categories.append(row[2])
     return expenses, months, categories
def regression_data_preperation():
    sorted_monthly = weekly_and_monthly_spending(show_output=False)
    months = list(sorted_monthly.keys())
    months_numerical = [i + 1 for i in range(len(months))]
    expenses = [sorted_monthly[month] for month in months]
    dataframe = pandas.DataFrame({'Months':months_numerical, 'Expenses':expenses})
    return dataframe
def regression_data_preperation_with_categories():
     expenses, months, categories = monthly_speding_with_category()
     label_encoder = LabelEncoder()
     category_encoded = label_encoder.fit_transform(categories)
     print(category_encoded)
     months_numerical = [int(month) for month in months]
     dataframe = pandas.DataFrame({'Months': months, 'Expenses': expenses, 'Categories': category_encoded})
     return dataframe
def precision_recall_metrics():
     dataframe = regression_data_preperation()
     x = dataframe[['Months']]
     y = dataframe[['Expenses']]
     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=False)
     model = LinearRegression()
     model.fit(x_train, y_train)
     y_pred = model.predict(x_test)
     margin = 0.1
     y_test = y_test.values.flatten()
     y_pred = y_pred.flatten()
     y_true_binary = (y_test > 0).astype(int)
     y_pred_binary = ((y_test * (1 - margin) <= y_pred) & (y_pred <= y_test * (1 + margin))).astype(int)
     precision = precision_score(y_true_binary, y_pred_binary)
     recall = recall_score(y_true_binary, y_pred_binary)
     return print(f"Precision: {precision:.2f}"), print(f"Recall: {recall:.2f}")
def expense_prediction(): 
     dataframe = regression_data_preperation()
     x = dataframe[['Months']]
     y = dataframe[['Expenses']]
     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=False)
     model = LinearRegression()
     model.fit(x_train, y_train)
     y_pred = model.predict(x_test)
     mae = mean_absolute_error(y_test, y_pred)
     next_month = pandas.DataFrame({'Months': [len(dataframe) + 1]})
     next_expense = model.predict(next_month)
     print(f"Based on your past spending, your projected budget for next month is: ${next_expense[0][0]:.2f}. (Mean Absolute Error: ${mae:.2f})")
     expenses = []
     years = []
     with open ("expenses_2024.csv", "r") as csvfile:
          reader = csv.reader(csvfile)
          next(reader)
          for row in reader:
               expenses.append(float(row[0]))
               years.append(row[3].split("-")[0])
     figure = plotly.express.scatter(x=expenses, y=years)
     figure.show()
def expense_prediction_category():
    dataframe = regression_data_preperation_with_categories()
    label_encoder = LabelEncoder()
    categories = ["Entertainment", "Food", "Housing", "Insurance", "Transportation", "Utilities", "Other"]
    category_mapping = dict(zip(label_encoder.fit_transform(categories), categories))
    category_models = {}
    for category_num, category_name in category_mapping.items():
        category_data = dataframe[dataframe['Categories'] == category_num]
        if len(category_data) == 0:
            print(f"no data for category {category_name}.")
            continue
        x = category_data[['Months']]
        y = category_data[['Expenses']]
        model = LinearRegression(positive=True)
        model.fit(x, y)
        next_month = pandas.DataFrame({'Months': [len(dataframe) + 1]})
        next_expense = model.predict(next_month)
        print(f"Predicted expense for next month ({category_name} Category): ${next_expense[0][0]:.2f}")
        category_models[category_name] = model
print("Hello! Welcome to your Personal Finance Assistant. How can I help?")
while True:
    choice = int(input("1: Add Expense, 2: View Report, 3: Predict Future Expenses, 4: Predict Future Expenses Based on Category, 5: Help 6: Exit"))
    if choice == 1:
        expense = input("Alright, How much money have you spent?")
        description = input("What did you spend it on?")
        category = input("In what category? (Utilities, Entertainment, Food, Banking(Debt/Savings), Transportation, Insurance, Housing, Education, Subscriptions, Other)")
        date = input("When? (Use yyyy-mm-dd).")
        data = [expense, description, category, date]
        with open("expenses_2024.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        print("Data added!")
        pandasdata = pandas.read_csv("expenses_2024.csv")
    elif choice == 2:
         print(pandasdata)
         weekly_and_monthly_spending()
    elif choice == 3:
         expense_prediction()
         precision_recall_metrics()
    elif choice == 4:
         expense_prediction_category()
    elif choice == 5:
         print("This is a finance assistant program. Choosing 1 will allow you to add expenses aka. what you have spent your money on, with 5the data inlcluding how much money, what you spent it on, in what category, and when. Choosing 2 will display all the entries so far in the log. It will also display your monthly and yearly spending. Choosing 3 will take the money you've spent throughout the last months and use that to make a linear regression model that will predict how much your budget will be for the upcoming month. It will also display the mean absolute error is for the calculation. Choosing 4 will allow to do the same thing, but you can input a category to specifically forecast a category.")
    elif choice == 6:
         print("Goodbye!")
         break
    else:
         print("Invalid choice. Please try again.")