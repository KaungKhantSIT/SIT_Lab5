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

#Process order and add to session cart 
def process_orders(cart, order):
    print(f"\nNew Order Added:\n{order}\n")
    cart.append(order)
    return cart

#Takes delivery amt & returns tax
def calculate_tax(amount):
    tax_rate = 0.1  # 10% tax rate
    taxed_total = amount * tax_rate
    return taxed_total

#Generate report of total units processed & failed entries
def generate_report(total_units, failed_attempts):
    report = f"Total Units Processed: {total_units}\n\
Number of Failed/Rejected Entries: {failed_attempts}"
    return report

#Load inventory from file
def load_inventory(filename):
    try:
        with open(filename, 'r') as file:
            inv = file.read().splitlines()
    except FileNotFoundError:
        inv = []
    return inv

#Save inventory to file
def save_inventory(filename,orders):
    with open(filename, 'a') as file:
        file.write('\n' + '\n'.join(orders))
    print(f"\nOrder(s) successfully saved to {filename}.")

#Show existing inventory
def show_inventory(inventory):
    print("Current Orders:\n")
    for order in inventory:
        print(order)
    print()

#Check total stock of product
def product_total(inventory, product):
    total = 0
    for order in inventory:
        name = order.split(',')[1].strip()
        qty = int(order.split(',')[2].strip())
        if name.lower() == product.lower():
            total += qty
    return total

#Alert if total stock exceeds 500 units
def inventory_cap(inventory, product, qty):
    total = product_total(inventory, product)
    total += qty
    if total > 500:  
        return True
    return False

#Auditor main program function
def auditor():
    file = "inventory.txt"
    total = 0
    failed = 0
    orders = []
    inventory = load_inventory(file)  # Load inventory from file
    show_inventory(inventory)  # Display current inventory
    index = int(inventory[-1].split(',')[0]) if inventory else 1001  # Get the last index from inventory or set to 1001 if empty
    while True:
        user_input = get_valid_input()
        if user_input == "quit":
            break
        elif user_input is None:
            failed += 1
        else:
            index += 1
            product, qty = user_input
            order = f"{index}, {product}, {qty}"
            #print(inventory_cap(inventory, product))
            if inventory_cap(inventory, product, qty):
                print(f"\nAlert: Total stock of {product} exceeding 500 units.")
                break
            process_orders(orders, order)
    if len(orders) > 0:
        save_inventory("inventory.txt", orders)  # Save inventory to file

#Run main program
auditor()