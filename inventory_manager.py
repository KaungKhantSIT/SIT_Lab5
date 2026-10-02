import json
import re

#Convert text to a non-negative int
def parse_qty(raw):
    try:
        qty = int(raw)
    except ValueError:
        raise ValueError("Please enter a valid number.")
    if qty < 0:
        raise ValueError("Please enter a non-negative number.")
    return qty

#Convert text to a price above $0, rounded to 2 decimals
def parse_price(raw):
    try:
        price = round(float(raw), 2)
    except ValueError:
        raise ValueError("Please enter a valid number.")
    if price <= 0:
        raise ValueError("Please enter a price above $0.")
    return price

#Check product ID format
def parse_id(raw,format=re.compile(r"P[0-9]{3,}")):
    pid = raw.upper()
    if not format.fullmatch(pid):
        raise ValueError("Please enter a valid product ID (e.g. P001).")
    return pid

#Prompt until input is validated using required parse function
def prompt_until_valid(prompt, parse):
    while True:
        raw = input(prompt).strip()
        try:
            return parse(raw)
        except ValueError as err:
            print(err)

#Load inventory from json file
def load_inventory(filename):
    try:
        with open(filename, 'r') as file:
            inv = json.load(file)
        print(f"{filename} found.")
        print("Inventory loaded successfully.\n")
    #Empty list if file not found
    except FileNotFoundError or json.JSONDecodeError:
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
    print("-------------------------------------------")

#Lookup product by ID
def find_by_id(inventory, pid):
    return next((p for p in inventory if p["ID"] == pid), None)
 
#Lookup product by Name
def find_by_name(inventory, name):
    return next((p for p in inventory if p["Name"].lower() == name.lower()), None)

#Add new product to inventory
def add_product(inventory):
    print("\nAdd New Product")
    #Prompt for Product ID
    while True:
        pid = prompt_until_valid("Product ID: ", parse_id)
        #Check if ID already exists
        if find_by_id(inventory, pid):
            print("Product ID already exists. Please enter a unique ID.")
        else:
            break
    #Prompt for Product Name
    while True:
        name = input("Product Name: ").strip()
        #Check that name is not empty
        if not name:
            print("Name cannot be empty.")
        #Check if product name already exists
        elif find_by_name(inventory, name):
            print("Product name already exists. Please enter a unique name.")
        else:
            break
    #Prompt for Price & Stock
    price = prompt_until_valid("Price($): ", parse_price)
    stock = prompt_until_valid("Stock Quantity: ", parse_qty)
    #Create and add product to inventory
    product = {
        "ID": pid,
        "Name": name,
        "Price": price,
        "Stock": stock
    }
    inventory.append(product)
    print("\nProduct added successfully!")

#Update stock of product
def update_stock(inventory):
    pid = prompt_until_valid("Enter Product ID: ", parse_id)
    product = find_by_id(inventory, pid)
    #Check if product exists
    if product is None:
        print("\nProduct Not Found")
        return
    #Update Stock
    print(f"Product Found:\nName: {product['Name']}\nCurrent Stock: {product['Stock']}\n")
    product["Stock"] = prompt_until_valid("New Stock Quantity: ", parse_qty)
    print("\nStock updated successfully!")

#Search and display product in inventory
def search_product(inventory):
    print("Search Product")
    pid = prompt_until_valid("Enter Product ID: ", parse_id)
    product = find_by_id(inventory, pid)
    if product is None:
        print("\nProduct Not Found")
    else:
        print("\nProduct Found")
        print("-------------------------------------------")
        print(f"ID:{product['ID']}\nName:{product['Name']}\nPrice:${product['Price']}\nStock:{product['Stock']}")
        print("-------------------------------------------")

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
        "Add New Product": lambda: add_product(inventory),
        "Update Stock": lambda: update_stock(inventory),
        "Search Product": lambda: search_product(inventory),
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
        input("\nPress Enter to return to the menu...")
    
#Run main program
if __name__ == "__main__":
    manager()