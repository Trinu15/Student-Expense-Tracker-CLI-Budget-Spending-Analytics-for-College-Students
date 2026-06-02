from datetime import datetime
from collections import defaultdict
import csv
import os

CSV_FILE = "expenses.csv"

expenses = []
monthly_budget = 1000.0

def load_expenses():
    global expenses
    if not os.path.exists(CSV_FILE):
        sample = [
            ["2026-06-01", 120, "food"],
            ["2026-06-02", 50, "travel"],
            ["2026-06-03", 199, "recharge"]
        ]
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category"])
            writer.writerows(sample)

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        expenses = [
            {"date": row["date"], "amount": float(row["amount"]), "category": row["category"]}
            for row in reader
        ]

def save_expenses():
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "amount", "category"])
        for e in expenses:
            writer.writerow([e["date"], e["amount"], e["category"]])

def add_expense():
    try:
        date = input("Date (YYYY-MM-DD): ")
        datetime.strptime(date, "%Y-%m-%d")

        amount = float(input("Amount: ₹"))
        if amount <= 0:
            print("Amount must be positive.")
            return

        category = input("Category (food/travel/recharge/other): ").lower()
        if category not in ["food", "travel", "recharge", "other"]:
            category = "other"

        expenses.append({
            "date": date,
            "amount": amount,
            "category": category
        })

        save_expenses()
        print("Expense added successfully.")
        check_budget()

    except ValueError:
        print("Invalid input.")

def view_expenses():
    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "-" * 50)
    print(f"{'ID':<5}{'DATE':<15}{'CATEGORY':<15}{'AMOUNT'}")
    print("-" * 50)

    for i, e in enumerate(expenses, start=1):
        print(f"{i:<5}{e['date']:<15}{e['category']:<15}₹{e['amount']}")

def total_spending():
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal Spending: ₹{total:.2f}")

def highest_category():
    totals = defaultdict(float)

    for e in expenses:
        totals[e["category"]] += e["amount"]

    category = max(totals, key=totals.get)
    print(f"\nHighest Spending Category: {category} (₹{totals[category]:.2f})")

def category_report():
    totals = defaultdict(float)

    for e in expenses:
        totals[e["category"]] += e["amount"]

    print("\nCategory Report")
    print("-" * 30)

    for cat, amount in totals.items():
        print(f"{cat:<15} ₹{amount:.2f}")

def delete_expense():
    view_expenses()

    try:
        idx = int(input("\nEnter expense ID to delete: "))

        if 1 <= idx <= len(expenses):
            expenses.pop(idx - 1)
            save_expenses()
            print("Expense deleted.")
        else:
            print("Invalid ID.")
    except ValueError:
        print("Invalid input.")

def set_budget():
    global monthly_budget
    try:
        monthly_budget = float(input("Enter monthly budget: ₹"))
        print(f"Budget set to ₹{monthly_budget:.2f}")
    except ValueError:
        print("Invalid amount.")

def check_budget():
    total = sum(e["amount"] for e in expenses)

    if total > monthly_budget:
        print(f"WARNING: Budget exceeded by ₹{total - monthly_budget:.2f}")

def main():
    load_expenses()

    while True:
        print("\n===== STUDENT EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spending")
        print("4. Highest Spending Category")
        print("5. Category Report")
        print("6. Delete Expense")
        print("7. Set Budget")
        print("8. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_spending()
        elif choice == "4":
            highest_category()
        elif choice == "5":
            category_report()
        elif choice == "6":
            delete_expense()
        elif choice == "7":
            set_budget()
        elif choice == "8":
            print("Thank you for using Expense Tracker.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
