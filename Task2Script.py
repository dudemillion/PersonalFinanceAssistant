import csv
import os
import datetime
import collections
import pandas
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
filepath = "expenses_2024.csv"
data = []
fields = ["Expense", "Description", "Category", "Date"]
pandasdata = pandas.read_csv(filepath)
with open(filepath, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        if os.path.getsize(filepath) == 0:
            writer.writerow(fields)
def weekly_and_monthly_spending():
    weekly = collections.defaultdict(float)
    monthly = collections.defaultdict(float)
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for y in reader:
            date = datetime.datetime.strptime(y["Date"], "%Y-%m-%d")
            week = date.strftime("%Y-%U")
            month = date.strftime("%Y-%m")
            expense = float(y["Expense"])
            weekly[week] += expense
            monthly[month] += expense
    sorted_monthly = dict(sorted(monthly.items()))
    return sorted_monthly

               
def regression_data_preperation():
    sorted_monthly = weekly_and_monthly_spending()
    months = list(sorted_monthly.keys())
    months_numerical = [i + 1 for i in range(len(months))]
    expenses = [sorted_monthly[month] for month in months]
    dataframe = pandas.DataFrame({'Months':months_numerical, 'Expenses':expenses})
    return dataframe
def expense_prediction():
     dataframe = regression_data_preperation()
     x = dataframe[['Months']]
     y = dataframe[['Expenses']]
     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=False)
     model = LinearRegression()
     model.fit(x, y)
     y_pred = model.predict(x_test)
     mae = mean_absolute_error(y_test, y_pred)
     next_month = numpy.array([[len(dataframe) + 1]])
     next_expense = model.predict(next_month)
     print(f"Based on your past spending, your projected budget for next month is: ${next_expense[0][0]:.2f}. (Mean Absolute Error: ${mae})")


while True:
    print("Hello! Welcome to your Personal Finance Assistant. How can I help?")
    choice = int(input("1: Add Expense, 2: View Report, 3: Predict Future Expenses, 4: Exit"))
    if choice == 1:
        expense = input("Alright, How much money have you spent?")
        description = input("What did you spend it on?")
        category = input("In what category? (Utilities, Entertainment, Food, Banking(Debt/Savings), Transportation, Insurance, Housing, Education, Subscriptions, Other)")
        date = input("When? (Use yyyy-mm-dd).")
        data = [expense, description, category, date]
        with open(filepath, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        print("Data added!")
    elif choice == 2:
         print(pandasdata)
         weekly_and_monthly_spending()
    elif choice == 3:
         expense_prediction()
    elif choice == 4:
         print("Goodbye!")
         break
    else:
         print("Invalid choice. Please try again.")