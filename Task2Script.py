import csv
import os
import datetime
import collections
import pandas
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import precision_score, recall_score
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

               
def regression_data_preperation():
    sorted_monthly = weekly_and_monthly_spending(show_output=False)
    months = list(sorted_monthly.keys())
    months_numerical = [i + 1 for i in range(len(months))]
    expenses = [sorted_monthly[month] for month in months]
    dataframe = pandas.DataFrame({'Months':months_numerical, 'Expenses':expenses})
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
     model.fit(x, y)
     y_pred = model.predict(x_test)
     mae = mean_absolute_error(y_test, y_pred)
     next_month = pandas.DataFrame({'Months': [len(dataframe) + 1]})
     next_expense = model.predict(next_month)
     print(f"Based on your past spending, your projected budget for next month is: ${next_expense[0][0]:.2f}. (Mean Absolute Error: ${mae:.2f})")

print("Hello! Welcome to your Personal Finance Assistant. How can I help?")
while True:
    choice = int(input("1: Add Expense, 2: View Report, 3: Predict Future Expenses, 4: Exit, 5: help"))
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
         print("Goodbye!")
         break
    elif choice == 5:
         print("This is a finance assistant program. Choosing 1 will allow you to add expenses aka. what you have spent your money on, with 5the data inlcluding how much money, what you spent it on, in what category, and when. Choosing 2 will display all the entries so far in the log. It will also display your monthly and yearly spending. Choosing 3 will take the money you've spent throughout the last months and use that to make a linear regression model that will predict how much your budget will be for the upcoming month. It will also display the mean absolute error is for the calculation.")
    else:
         print("Invalid choice. Please try again.")