# Personal Finance Assistant with Budget Prediction
This CMD line interface helps users track their expenses and predict future spending using a ML model.

## ML Pipeline
1. Data Collection: Expenses are entered manually and saved in a CSV file.
2. Data Analysis: The data is processed to calculate weekly and monthly totals.
3. Prediction: A linear regression model is used to predict the user's expenses for the next month based on past data.

## Requirements
- Python 3.11+
- pandas
- numpy
- scikit-learn
- pytest (for testing)

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/finance-assistant.git
cd finance-assistant
pip install -r requirements.txt
