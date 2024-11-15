import unittest
import os
import csv
from io import StringIO

class TestExpenseFunctions(unittest.TestCase):

    def setUp(self):
        self.filepath = "test_expenses.csv"
        self.fields = ["Expense", "Description", "Category", "Date"]
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        with open(self.filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)

    def test_data_entry(self):
        expense_data = ["50.00", "Groceries", "Food", "2024-11-15"]
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(expense_data)

        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2)  # Check that there are two rows in the file
            self.assertEqual(rows[1], expense_data)  # Verify the added data is correct

    def test_data_display(self):
        # Assuming your display function prints the data to the console
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["100.00", "Rent", "Housing", "2024-11-01"])

        # Simulate display
        output = StringIO()
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                output.write(f'{row}\n')

        output.seek(0)
        displayed_data = output.getvalue()
        self.assertIn("100.00", displayed_data)  # Check if Rent expense is displayed

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


if __name__ == '__main__':
    unittest.main()
