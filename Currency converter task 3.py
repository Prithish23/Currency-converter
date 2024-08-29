import requests
import tkinter as tk
from tkinter import messagebox

# Function to get real-time exchange rates
def get_exchange_rate(api_key, base_currency):
    url = f"https://v6.exchangerate-api.com/v6/f7a90bc979588133986913d9/latest/USD"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error: Unable to fetch data, status code: {response.status_code}")
    
    data = response.json()
    
    # Debugging: Print the raw data returned from the API
    print("API Response:", data)

    if "error" in data:
        raise Exception(f"API Error: {data['error-type']}")
    
    return data["conversion_rates"]

# Function to convert currency
def convert_currency(amount, base_currency, target_currency):
    exchange_rates = get_exchange_rate(api_key, base_currency)
    exchange_rate = exchange_rates.get(target_currency)
    
    if exchange_rate is None:
        raise ValueError(f"Invalid target currency: {target_currency}")
    
    print(f"Exchange Rate for {target_currency}: {exchange_rate}")  # Debugging
    
    return amount * exchange_rate

# Function that handles the conversion and displays the result
def on_convert():
    try:
        amount = float(amount_entry.get())
        base_currency = base_currency_var.get()
        target_currency = target_currency_var.get()
        
        print(f"Converting {amount} {base_currency} to {target_currency}")  # Debugging
        
        converted_amount = convert_currency(amount, base_currency, target_currency)
        
        print(f"Converted Amount: {converted_amount}")  # Debugging
        
        result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to swap the base and target currencies and update the result
def swap_currencies():
    current_base_currency = base_currency_var.get()
    current_target_currency = target_currency_var.get()
    
    # Swap the values
    base_currency_var.set(current_target_currency)
    target_currency_var.set(current_base_currency)
    
    # Automatically convert after swapping
    on_convert()

# Initialize the main window
root = tk.Tk()
root.title("Currency Converter")
root.geometry("500x550")
root.resizable(False, False)
root.configure(bg="#344955")

# API key (replace with your actual API key)
api_key = 'f7a90bc979588133986913d9'

# Currency options
currency_options = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY"]

# Title Label
title_label = tk.Label(root, text="Currency Converter", font=("Helvetica", 24, "bold"), bg="#344955", fg="#F9AA33")
title_label.pack(pady=20)

# Amount Entry
amount_label = tk.Label(root, text="Amount:", font=("Helvetica", 18), bg="#344955", fg="white")
amount_label.pack(pady=10)
amount_entry = tk.Entry(root, font=("Helvetica", 18), justify='center')
amount_entry.pack(pady=10)

# Base Currency Dropdown
base_currency_label = tk.Label(root, text="Base Currency:", font=("Helvetica", 18), bg="#344955", fg="white")
base_currency_label.pack(pady=10)
base_currency_var = tk.StringVar(root)
base_currency_var.set(currency_options[0])  # Default value
base_currency_menu = tk.OptionMenu(root, base_currency_var, *currency_options)
base_currency_menu.config(font=("Helvetica", 18), bg="white", fg="black")
base_currency_menu.pack(pady=10)

# Target Currency Dropdown
target_currency_label = tk.Label(root, text="Target Currency:", font=("Helvetica", 18), bg="#344955", fg="white")
target_currency_label.pack(pady=10)
target_currency_var = tk.StringVar(root)
target_currency_var.set(currency_options[1])  # Default value
target_currency_menu = tk.OptionMenu(root, target_currency_var, *currency_options)
target_currency_menu.config(font=("Helvetica", 18), bg="white", fg="black")
target_currency_menu.pack(pady=10)

# Swap Button
swap_button = tk.Button(root, text="Swap Currencies", font=("Helvetica", 14, "bold"), bg="#F9AA33", fg="white", command=swap_currencies)
swap_button.pack(pady=10)

# Convert Button
convert_button = tk.Button(root, text="Convert", font=("Helvetica", 18, "bold"), bg="#F9AA33", fg="white", command=on_convert)
convert_button.pack(pady=20)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 20, "bold"), bg="#344955", fg="white")
result_label.pack(pady=20)

# Run the main loop
root.mainloop()

