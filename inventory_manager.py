import json

#Check if quantity is a valid positive integer
def validate_qty(qty):
    try:
        qty = int(qty)
        if qty < 0:
            print("Please enter a positive number.")
            return False
        return True
    except ValueError:
        print("Please enter a valid number.")
        return False

#Check if entered ID is valid
def validate_id(ID):
    if not ID.startswith("P") or not ID[1:].isdigit():
        print("Please enter a valid product ID.")
        return False
    return True

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
    print("-------------------------------------------")

#Lookup product by ID or name
def lookup_product(inventory, search):
    for order in inventory:
        if order['ID'] == search or order['Name'].lower() == search.lower():
            return order
    return None

#Add new product to inventory
def add_product(inventory):
    print("\nAdd New Product")
    product = {}
    while True:
        product['ID'] = input("Product ID: ").strip().title()
        #ID Validation
        if validate_id(product['ID']):
            #Check if product ID already exists
            if lookup_product(inventory, product['ID']):
                print("Product ID already exists. Please enter a unique ID.")
            else:
                break
    while True:
        product['Name'] = input("Product Name: ").strip().title()
        #Check if product name already exists
        if lookup_product(inventory, product['Name']):
            print("Product name already exists. Please enter a unique name.")
        else:
            break
    product['Price'] = float(input("Price($): ").strip())
    while True:
        product['Stock'] = input("Stock Quantity: ").strip()
        if validate_qty(product['Stock']):
            product['Stock'] = int(product['Stock'])
            break
    inventory.append(product)
    return inventory

#Search and display product in inventory
def search_product(inventory):
    print("Search Product")
    while True:
        id = input("Enter Product ID: ").strip().title()
        if validate_id(id):
            break
    product = lookup_product(inventory, id)
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
        "Update Stock": lambda: print("Not implemented yet."),
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
manager()