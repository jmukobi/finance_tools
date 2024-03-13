"""
Jacob's Lifelong Financial Planning :)
"""

#Import

import seaborn as sns
import matplotlib.pyplot as plt

#Define constants

BIRTH_YEAR = 2002
STARTING_YEAR = 2025
DIE_YEAR = 2102

STARTING_INCOME = 80000
YOY_INCOME_GROWTH = 1.02
YOY_INVESTMENT_RETURN = 1.07

# Define financial goals

GOALS = {
    #"Aircraft": {"age": 33, "total_value": 500000, "down_payment": 100000, "monthly_payment": 3200, "loan_term": 20},
    "Wedding": {"age": 30, "total_value": 10000, "down_payment": 10000, "monthly_payment": 0, "loan_term": 0},
    "Children": {"age": 37, "total_value": 1080000, "down_payment": 0, "monthly_payment": 5000, "loan_term": 18},
    "Home": {"age": 35, "total_value": 1000000, "down_payment": 100000, "monthly_payment": 3000, "loan_term": 30},
    "Retirement": {"age": 65, "total_value": 2000000, "down_payment": 0, "monthly_payment": 2000000/(35*12), "loan_term": 0},
    #"Mom's Yacht": {"age": 32, "total_value": 300000, "down_payment": 60000, "monthly_payment": 2500, "loan_term": 20},
    "Kid's College": {"age": 40, "total_value": 1000000, "down_payment": 0, "monthly_payment": 5000, "loan_term": 4},
}

# Define monthly expenses at each stage of life

"""
stage 1: 22 - house purchase
stage 2: house purchase - retirement
stage 3: retirement - death
"""

EXPENSES = {
    "Stage 1":{
        "Rent": 2000,
        "Food": 200,
        "Transportation": 100,
        "Recreation": 600,
        "Miscellaneous": 200,
        },
    "Stage 2":{
        "Rent": 0,
        "Food": 300,
        "Transportation": 200,
        "Recreation": 600,
        "Miscellaneous": 300,
        },
    "Stage 3":{
        "Rent": 0,
        "Food": 400,
        "Transportation": 300,
        "Recreation": 600,
        "Miscellaneous": 400,
        },
}

class Finance:
    def __init__(self, income, expense_dict, starting_year, financial_goals):
        self.income = income
        self.balance = 0
        self.expenses = 12*sum(expense_dict["Stage 1"].values())
        self.starting_year = starting_year
        self.financial_goals = financial_goals
        self.income_tax = 0
        self.balances = []
        self.expense_history = []
        self.income_history = []
        self.saving_history = []

    def update_income_and_expenses(self, year):
        # Update income

        #increment income
        
        self.income *= YOY_INCOME_GROWTH

        # subtract taxes

        self.income_tax = self.calculate_income_tax(self.income)
        
        # no income after retirement
        
        if year - BIRTH_YEAR >= self.financial_goals["Retirement"]["age"]:
            self.income = 0
        
        # Update expenses
            
        # Get expenses based on stage of life
            
        if year - BIRTH_YEAR < self.financial_goals["Home"]["age"]:    
            self.expenses = 12*sum(EXPENSES["Stage 1"].values())
        elif year - BIRTH_YEAR < self.financial_goals["Retirement"]["age"]:
            self.expenses = 12*sum(EXPENSES["Stage 2"].values())
        else:
            self.expenses = 12*sum(EXPENSES["Stage 3"].values())

        # Add loan payments
        
        loan_payments = 0
        for goal in self.financial_goals:
            if self.financial_goals[goal]["age"] <= year - BIRTH_YEAR and self.financial_goals[goal]["loan_term"] > year - BIRTH_YEAR - self.financial_goals[goal]["age"]:
                loan_payments += self.financial_goals[goal]["monthly_payment"] * 12
        
        self.expenses += loan_payments

        self.expenses += self.income_tax
    
    def calculate_income_tax(self, gross_income):
        # Calculate federal and california income tax
        
        # Tax brackets
        
        brackets = [9875, 40125, 85525, 163300, 207350, 518400]
        federal_rates = [0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]
        california_brackets = [8544, 20255, 31969, 44377, 56085, 286492, 343788, 572980, 1000000]
        california_rates = [0.01, 0.02, 0.04, 0.06, 0.08, 0.093, 0.103, 0.113, 0.123]
        
        # Calculate tax
        
        tax = 0
        
        for i, bracket in enumerate(brackets):
            if gross_income > bracket:
                tax = federal_rates[i] * gross_income

        california_tax = 0
        for i, bracket in enumerate(california_brackets):
            if gross_income > bracket:
                california_tax = california_rates[i] * gross_income
        
        tax += california_tax
        return tax


    def update_yearly_balance(self):
        # Calculate savings

        savings = self.income - self.expenses
        
        # Add income
        
        self.balance += savings
        
        # Add investment returns
        
        self.balance *= YOY_INVESTMENT_RETURN
        
        # Add to history
        
        self.expense_history.append(self.expenses)
        self.income_history.append(self.income)
        self.balances.append(self.balance)
        self.saving_history.append(savings)

    def simulate_life(self):
        # Loop through each year

        for year in range(STARTING_YEAR, DIE_YEAR):
            self.update_income_and_expenses(year)
            self.update_yearly_balance()

    def graph_life(self):
        sns.set_style("whitegrid")
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Plot balance
        ax1.plot(range(STARTING_YEAR, DIE_YEAR), self.balances, color="green" if min(self.balances) > 0 else "red", label="Balance")
        ax1.set_ylabel("Balance ($)")
        ax1.set_title("Total Balance Over Time")
        
        # Plot income, expenses, and savings
        ax2.plot(range(STARTING_YEAR, DIE_YEAR), self.expense_history, color="orange", label="Expenses")
        ax2.plot(range(STARTING_YEAR, DIE_YEAR), self.income_history, color="blue", label="Income")
        ax2.plot(range(STARTING_YEAR, DIE_YEAR), self.saving_history, color="green", label="Money Saved")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("$")
        ax2.set_title("Income, Expenses, and Savings Over Time")
        ax2.legend()
        
        # Plot vertical lines at each goal
        for goal in self.financial_goals:
            ax1.axvline(x=self.financial_goals[goal]["age"] + BIRTH_YEAR, color="grey", linestyle="--")
            ax1.text(self.financial_goals[goal]["age"] + BIRTH_YEAR + .25, min(self.balances), goal, rotation=90, fontsize=10)
            ax2.axvline(x=self.financial_goals[goal]["age"] + BIRTH_YEAR, color="grey", linestyle="--")
            ax2.text(self.financial_goals[goal]["age"] + BIRTH_YEAR + .25, min(self.saving_history), goal, rotation=90, fontsize=10)
        
        # Display y-axis labels without scientific notation
        ax1.ticklabel_format(style='plain', axis='y')
        ax2.ticklabel_format(style='plain', axis='y')
        
        # Display y-axis labels with commas
        ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
        
        # Add age labels to x-axis
        age_labels = [year - BIRTH_YEAR for year in range(STARTING_YEAR, DIE_YEAR, 5)]
        ax2.set_xticks(range(STARTING_YEAR, DIE_YEAR, 5))
        ax2.set_xticklabels(age_labels)
        
        # Show plot
        plt.show()


def main():
    # Create a Finance object

    income = STARTING_INCOME
    expense_dict = EXPENSES
    financial_goals = GOALS
    finance = Finance(income, expense_dict, 2024, financial_goals)
    
    # Simulate life

    finance.simulate_life()
    
    # Print final balance

    print(f"Final Balance: ${finance.balances[-1]:,.2f}")
    
    # Graph life

    finance.graph_life()
    

main()