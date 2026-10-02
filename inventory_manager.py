import json

#Input prompt, input validation, and return valid integer/"quit" signal
def get_valid_input():
    order = ""
    product = input("Enter product name (or type 'quit' to exit):").title()
    if product.lower() == "quit":
        return "quit"
    elif not product.isalpha():
        print("Please enter a valid product name.")
        return None
    qty = input("Enter stock quantity (or type 'quit' to exit): ")
    if qty.lower() == "quit":
        return "quit"
    try:
        qty = int(qty)
        if qty < 0:
            print("Please enter a positive number.")
            return None
        return product, qty
    except ValueError:
        print("Please enter a valid number.")
        return None

#Load inventory from json file
def load_inventory(filename):
    try:
        with open(filename, 'r') as file:
            inv = json.load(file)
        print(f"{filename} found.")
        print("Inventory loaded successfully.\n")
    #Empty list if file not found
    except FileNotFoundError:
        inv = []
    return inv

#Save inventory to json file
def save_inventory(filename, orders):
    print("\nSaving inventory...")
    with open(filename, 'w') as file:
        json.dump(orders, file, indent=2)
    print(f"Inventory saved successfully to {filename}.")

#Show existing inventory
def display_all(inventory):
    print("\nCurrent Inventory")
    print("-------------------------------------------")
    for order in inventory:
        print(f"ID:{order['ID']}|Name:{order['Name']}|Price:${order['Price']:.2f}|Stock:{order['Stock']}")
    print("-------------------------------------------\n")

#Add new product to inventory
def add_product(cart, order):
    print(f"\nNew Product Added:\n{order}\n")
    cart.append(order)
    return cart

#Search for product in inventory
def search_product(inventory, product):
    for order in inventory:
        if order['Name'].lower() == product.lower():
            return order
    return None

#Alert if total stock exceeds 500 units
def inventory_cap(inventory, product, qty, cap=500):
    pass

#print menu options
def menu_page(menu):
    print("---------MENU---------")
    for i, option in enumerate(menu.keys(), start=1):
        print(f"{i}. {option}")
    print("----------------------\n")
    while True:
        option = input(f"Enter option (1-{len(menu)}): ").strip()
        if option.isdigit() and 1 <= int(option) <= len(menu):
            return list(menu.keys())[int(option) - 1]
        else:
            print("Invalid option. Please select a valid option.")

#Manager main program function
def manager():
    file = "inventory.json"
    #Title
    print("============================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("============================\n")
    # Load inventory from file
    inventory = load_inventory(file)
    #User menu options
    menu = {
        "Display All Products": lambda: display_all(inventory),
        "Add New Product": lambda: print("Not implemented yet."),
        "Update Stock": lambda: print("Not implemented yet."),
        "Search Product": lambda: print("Not implemented yet."),
        "Save Inventory": lambda: save_inventory(file, inventory),
        "Exit": None
    }
    #Menu
    while True:
        option = menu_page(menu)
        if option == "Exit":
            save_inventory(file, inventory)
            print("\nThank you for using the Inventory Management System.")
            print("Program terminated.")
            return
        menu[option]()
    
#Run main program
manager()