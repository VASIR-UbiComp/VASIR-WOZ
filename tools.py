from data_classes import *

shopping_lists = {}

# Function to change volume
def change_volume(volume_level: int):
    global volume
    if 0 <= volume_level <= 10:
        volume = volume_level
        print("Volume changed to: " + str(volume))
    else:
        raise ValueError("Volume level must be between 0 and 10")

def add_medicine(
    name: str,
    pills_count: float,
    when_to_take_day,
    when_to_take_hours,
    when_to_take_minutes,
):
    when_to_take = []
    for i in range(len(when_to_take_hours)):
        when_to_take.append(
            Date(when_to_take_day[i], when_to_take_hours[i], when_to_take_minutes[i])
        )
    medicine = Medicine(name, pills_count, when_to_take)
    print(medicine)

def add_event(day: int, month: str, year: int, hour: int, minute: int, content: str, reminders: list = None):
    # Default reminders if none are provided
    if reminders is None:
        reminders = [
            {'days_before': 1, 'hours_before': 0, 'minutes_before': 0},
            {'days_before': 0, 'hours_before': 2, 'minutes_before': 0}
        ]
    
    # Create the event with the appropriate reminders
    event = Event(day, month, year, hour, minute, content, reminders)
    
    return event

def create_shopping_list(name: str, products: list):
    global shopping_lists
    if name in shopping_lists:
        raise ValueError(f"Lista zakupów o nazwie '{name}' już istnieje.")
    shopping_lists[name] = products
    print(f"Utworzono listę zakupów '{name}' z produktami: {products}")

def add_to_shopping_list(name: str, products: list):
    global shopping_lists
    if name not in shopping_lists:
        raise ValueError(f"Lista zakupów o nazwie '{name}' nie istnieje.")
    shopping_lists[name].extend(products)
    print(f"Dodano produkty do listy zakupów '{name}': {products}. Obecna lista: {shopping_lists[name]}")

def delete_from_shopping_list(name: str, products: list):
    global shopping_lists
    if name not in shopping_lists:
        raise ValueError(f"Lista zakupów o nazwie '{name}' nie istnieje.")
    for product in products:
        if product in shopping_lists[name]:
            shopping_lists[name].remove(product)
            print(f"Usunięto produkt '{product}' z listy zakupów '{name}'.")
        else:
            print(f"Produkt '{product}' nie znajduje się na liście zakupów '{name}'.")
    print(f"Zaktualizowana lista zakupów '{name}': {shopping_lists[name]}")

def list_shopping_lists():
    global shopping_lists
    if not shopping_lists:
        print("Brak dostępnych list zakupów.")
    else:
        for name, items in shopping_lists.items():
            print(f"Lista zakupów '{name}': {items}")
            


#notowanie budzetu na dany rok i miesiac 
def set_monthly_budget(month: int, year: int, amount: float):
    if 1 <= month <= 12 and year > 0 and amount >= 0:
        budget = {"month": month, "year": year, "amount": amount}
        print(f"Monthly budget set: {budget}")
        return budget
    else:
        raise ValueError("Niepoprawny miesiąc, data albo suma. Miesiąc powinien istnieć, rok i budzet powinny być wartością dodatnią.")
  
#add_income and add_spending need to lather fetch the budget from the database.
#Currently there is a problem with adding a spending or an income when the budget has not yet been set.
  
def add_spending(budget: dict, expense: float, description: str):
    if 'amount' in budget and budget['amount'] >= expense >= 0:
        budget['amount'] -= expense
        print(f"Added spending: {description}, amount: {expense}. Remaining budget: {budget['amount']}")
        return budget
    else:
        raise ValueError("Invalid expense amount or budget exceeded.")
    
def add_income(budget: dict, income: float, description: str): 
    if 'amount' in budget and income >= 0:
        budget['amount'] += income
        print(f"Added income: {description}, amount: {income}. New budget total: {budget['amount']}")
        return budget
    else:
        raise ValueError("Invalid income amount.")
    
  
#potem tez by sie przydalo dodac te przypomnienia jak juz asystent bedzie mial dostep do zegara
def add_recurring_spending(expense: float, description: str, recurrence: str):
    if recurrence != "monthly":
        raise ValueError("Currently, only monthly recurrence is supported.")

    recurring_expense = {"expense": expense, "description": description, "recurrence": recurrence}
    print(f"Recurring spending noted: {recurring_expense}")
    return recurring_expense

