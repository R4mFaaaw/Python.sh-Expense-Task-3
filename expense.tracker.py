import argparse
import json
import os
from datetime import datetime

FILENAME = "expenses.json"

def load_expenses():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(FILENAME, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(description, amount):
    if amount <= 0:
        print("Error: Jumlah harus lebih dari 0.")
        return
    
    expenses = load_expenses()
    new_id = max([e['id'] for e in expenses], default=0) + 1
    
    new_expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

def list_expenses():
    expenses = load_expenses()
    print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<10}")
    for e in expenses:
        print(f"{e['id']:<4} {e['date']:<12} {e['description']:<20} ${e['amount']:<10}")

def delete_expense(expense_id):
    expenses = load_expenses()
    filtered = [e for e in expenses if e['id'] != expense_id]
    if len(filtered) == len(expenses):
        print(f"Error: ID {expense_id} tidak ditemukan.")
    else:
        save_expenses(filtered)
        print("Expense deleted successfully")

def show_summary(month=None):
    expenses = load_expenses()
    current_year = datetime.now().year
    
    if month:
        if not (1 <= month <= 12):
            print("Error: Bulan harus antara 1-12.")
            return
        
        filtered = [e for e in expenses if datetime.strptime(e['date'], "%Y-%m-%d").month == month 
                    and datetime.strptime(e['date'], "%Y-%m-%d").year == current_year]
        total = sum(e['amount'] for e in filtered)
        month_name = datetime(current_year, month, 1).strftime("%B")
        print(f"Total expenses for {month_name}: ${total}")
    else:
        total = sum(e['amount'] for e in expenses)
        print(f"Total expenses: ${total}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # List command
    subparsers.add_parser("list")

    # Delete command
    del_parser = subparsers.add_parser("delete")
    del_parser.add_argument("--id", type=int, required=True)

    # Summary command
    sum_parser = subparsers.add_parser("summary")
    sum_parser.add_argument("--month", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        show_summary(args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()