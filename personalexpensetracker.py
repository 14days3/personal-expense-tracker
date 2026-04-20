#initialize stuff
import json
import os
from datetime import datetime
import textwrap
entries = []
def save_to_file():
    #add an input asking the user to name their file
    file_name = input("Input the file name to save this file as: ").strip()
    if file_name.endswith(".json"):
        file_name += ".json"
    try:
        with open(file_name, "x") as f:
            json.dump(entries, f, indent=4)
            print("Account saved successfully!")
    except FileExistsError as e:
        print(f"failed to save file {e}.")
        return menu()

def load_from_file():
    #add an input asking the user the name of the file they want to save
    global entries
    file_name = input("Input the file name to load: ").strip()
    if file_name.endswith(".json"):
        file_name += ".json"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            entries = json.load(f)
            print("Account loaded successfully!")
    else:
        print("Entry does not exist.")
        entries = []

def menu():
#add option to remove an entry
    while True:
        print("(1) Add Entry\n(2) View current account\n(3) Delete an entry\n(4) Import\n(5) Export\n(6) Delete account\n(7) Change Account\n(8) Exit")
        try:
            user = int(input("Welcome to the Expense Tracker app, enter a number below to perform any of the actions listed: "))
            if user == 1:
                entry()
            elif user == 2:
                print_table()
            elif user == 3:
                remove_entry()
            elif user == 4:
                load_from_file()
            elif user == 5:
                save_to_file()
            elif user == 6:
                delete_account()
            elif user == 7:
                entries.clear()
                print("Table has been cleared.")
            elif user == 8:
                exit()
            else:
                continue
        except ValueError:
            print("Please only enter the numbers listed above.")


def entry():
    #initialize variables so I don't get the fucking warnings
    category = None
    particulars = None
    income = None
    expense = None
    try:
        entry_choice = int(input("Enter (1) if your entry will be money out, (2) if your entry will be money in: "))
    except ValueError:
        print("Please only enter either 1 or 2.")
        return
#dates anf stuff (ill never get a date ong)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    user_date = input(f"Date [{current_date}](press Enter to keep the default date or follow the format): ").strip()
    date = user_date if user_date else current_date
    category = input("Category: ")
    date_convert = datetime.strptime(date, "%Y-%m-%d %H:%M")
    if entry_choice == 1:
        particulars = input("Particulars: ")
        expense = int(input("Expense: "))
        income = "----"
    elif entry_choice == 2:
        particulars = input("Particulars: ")
        income = int(input("Income: "))
        expense = "----"


    entry_data = {
        "date": date,
        "particulars": particulars,
        "expense": expense,
        "income": income,
        "category": category,
    }
    entries.append(entry_data)
    print("Entry added successfully!")

#add text wrapping on the particulars smh
def print_table():
    entries.sort(key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d %H:%M"))

    col_width = 20

    print("\n" + "=" * 120)
    print(f"{'#':<5} {'Date':<16} {'Category':<15} {'Particulars':<20} {'Out':>10} {'In':>10}")
    print("-" * 120)

    for i, e in enumerate(entries):
        wrapped_particulars = textwrap.wrap(e["particulars"], width=col_width)

        print(f"{i:<5} {e['date']:<16} {e['category']:<15} {wrapped_particulars[0]:<20} {str(e['expense']):>10} {str(e['income']):>10}")

        for line in wrapped_particulars[1:]:
            print(f"{'':<5} {'':<16} {'':<15} {line:<20} {'':>10} {'':>10}")

    print("=" * 120)

def remove_entry():
    if not entries:
        print("No entry to remove.")
        return
    print_table()
    try:
        index = int(input("Enter the number of the entry that you want to delete: "))
        if 0 <= index < len(entries):
            removed = entries.pop(index)
            print(f"Successfully removed entry number {index}")
        else:
            print("Invalid index!")
    except ValueError:
        print("Please type a number of an existing entry within the table!")

def delete_account():
    file_name = input("Input the file name to remove: ").strip()
    confirmation = input("Do you really wish to delete this account? (Yes) or (No): ").lower()
    if confirmation == "yes":
        entries.clear()
        try:
            os.remove(file_name)
            print("Account has been wiped.")
        except FileNotFoundError:
            print(f"File does not exist")
        return
    elif confirmation == "no":
        return
    else:
        print("Please only enter either (Yes) or (No)")

menu()
