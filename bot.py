import json

from datetime import datetime

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "finance_data.json")

def load_data():
    """"Зчитує дані з файлу при запуску програми."""
    if not os.path.exists(DATA_FILE):
        return {"budget": 0.0, "expenses": []}
    
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # Якщо файл порожній, просто повертаємо стандартні дані
            return {"budget": 0.0, "expenses": []}
        
def save_data(data):
    """Зберігає поточні дані у файл JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def print_help():
    """Виводить список доступних команд."""
    print("\n--- Доступні команди ---")
    print("1. допомога - Показати цей список.")
    print("2. встановити бюджет - Встановити загальний бюджет.")
    print("3. додати витрату - Записати нову витрату.")
    print("4. показати витрати - Вивести всі збережені витрати.")
    print("5. фільтр дата - Показати витрати за конкретну дату.")
    print("6. фільтр період - Показати витрати за період між двома датами.")
    print("7. фільтр категорія - Показати витрати за певною категорією.")
    print("8. залишок - Переглянути залишок бюджету.")
    print("9. звіт за категоріями - Загальна сума витрат по кожній категорії.")
    print("10. вийти - Завершити роботу програми.")
    print("------------------------\n")

def set_budget(data):
    """Встановлює новий бюджет користувача."""
    try:
        amount = float(input("Введіть суму бюджету: "))
        data["budget"] = amount
        save_data(data)
        print(f"Бюджет успішно встановлено: {amount} грн.")
    except ValueError:
        print("Помилка: введіть числове значення.")

def add_expense(data):
    """Додає нову витрату та перевіряє перевищення бюджету."""
    try:
        amount = float(input("Введіть суму витрати: "))
        category = input("Введіть категорію (наприклад, Їжа, Транспорт): ").strip()
        date_str = input("Введіть дату (РРРР-ММ-ДД): ").strip()
        
        # Перевірка формату дати
        datetime.strptime(date_str, "%Y-%m-%d")
        
        comment = input("Введіть короткий коментар (необов'язково): ").strip()
        
        expense = {
            "amount": amount,
            "category": category,
            "date": date_str,
            "comment": comment
        }
        
        data["expenses"].append(expense)
        save_data(data)
        print("Витрату успішно додано!")
        
        
        total_expenses = sum(item["amount"] for item in data["expenses"])
        if total_expenses > data["budget"]:
            print(f"⚠️ УВАГА! Ви перевищили встановлений бюджет! Ваш бюджет: {data['budget']}, Витрати: {total_expenses}")
            
    except ValueError:
        print("Помилка: сума має бути числом, а дата у форматі РРРР-ММ-ДД.")

def show_expenses(expenses):
    """Виводить список переданих витрат."""
    if not expenses:
        print("Список витрат порожній.")
        return
        
    print("\n--- Список витрат ---")
    for i, exp in enumerate(expenses, 1):
        comment = f" ({exp['comment']})" if exp['comment'] else ""
        print(f"{i}. Дата: {exp['date']} | Категорія: {exp['category']} | Сума: {exp['amount']} грн{comment}")
    print("---------------------\n")

def filter_by_date(data):
    date_str = input("Введіть дату для пошуку (РРРР-ММ-ДД): ").strip()
    filtered = [exp for exp in data["expenses"] if exp["date"] == date_str]
    show_expenses(filtered)

def filter_by_period(data):
    try:
        start_date = input("Введіть початкову дату (РРРР-ММ-ДД): ").strip()
        end_date = input("Введіть кінцеву дату (РРРР-ММ-ДД): ").strip()
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        filtered = [
            exp for exp in data["expenses"] 
            if start <= datetime.strptime(exp["date"], "%Y-%m-%d") <= end
        ]
        show_expenses(filtered)
    except ValueError:
         print("Помилка: неправильний формат дати.")

def filter_by_category(data):
    category = input("Введіть категорію для пошуку: ").strip().lower()
    filtered = [exp for exp in data["expenses"] if exp["category"].lower() == category]
    show_expenses(filtered)

def show_balance(data):
    """Виводить залишок від встановленого бюджету."""
    total_expenses = sum(item["amount"] for item in data["expenses"])
    balance = data["budget"] - total_expenses
    print(f"\nВаш бюджет: {data['budget']} грн")
    print(f"Загальні витрати: {total_expenses} грн")
    print(f"Залишок: {balance} грн\n")

def category_report(data):
    """Підраховує загальну суму витрат по кожній категорії."""
    report = {}
    for exp in data["expenses"]:
        cat = exp["category"]
        report[cat] = report.get(cat, 0) + exp["amount"]
        
    print("\n--- Звіт за категоріями ---")
    if not report:
        print("Витрат немає.")
    else:
        for cat, total in report.items():
            print(f"{cat}: {total} грн")
    print("---------------------------\n")

def main():
    """Головний цикл програми."""
    print("Привіт! Я твій бот 'Фінансовий трекер студента'.")
    data = load_data()
    
    while True:
        command = input("Введіть команду (або 'допомога' для списку): ").strip().lower()
        
        if command == "допомога":
            print_help()
        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data["expenses"])
        elif command == "фільтр дата":
            filter_by_date(data)
        elif command == "фільтр період":
            filter_by_period(data)
        elif command == "фільтр категорія":
            filter_by_category(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт за категоріями":
            category_report(data)
        elif command == "вийти":
            print("Збереження даних... До зустрічі!")
            break
        else:
            print("Невідома команда. Введіть 'допомога' для списку доступних команд.")

if __name__ == "__main__":
    main()