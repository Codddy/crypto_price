import requests
import tkinter as tk
import threading
from datetime import datetime

crypto_symbols = ["BTC", "ETH", "LTC", "DOGE", "XRP"]
prices = {}

def get_crypto_price(crypto_symbol):
    base_url = "https://api.pro.coinbase.com"
    ticker_url = f"{base_url}/products/{crypto_symbol}-USD/ticker"
    
    response = requests.get(ticker_url)
    data = response.json()
    
    if 'price' in data:
        price = float(data['price'])
        return price
    else:
        return None

def update_prices():
    global prices
    
    for symbol in crypto_symbols:
        price = get_crypto_price(symbol)
        if price:
            if symbol in ["DOGE", "XRP"]:
                prices[symbol] = round(price, 6)
            else:
                prices[symbol] = price

    threading.Timer(5, update_prices).start()

def create_gui():
    window = tk.Tk()
    window.title("Crypto Price")
    
    window.geometry("300x300")
    window.resizable(False, False)

    labels = []
    for symbol in crypto_symbols:
        label = tk.Label(window, text=f"{symbol}: $0.00")
        label.pack(pady=10, anchor="w")
        labels.append(label)

    def update_labels():
        for i, symbol in enumerate(crypto_symbols):
            if symbol in prices:
                current_price = prices[symbol]
                if symbol in ["DOGE", "XRP"]:
                    label_text = f"{symbol}: ${current_price:.6f}"
                else:
                    label_text = f"{symbol}: ${current_price:.2f}"
                    
                if symbol in previous_prices:
                    previous_price = previous_prices[symbol]
                    if current_price > previous_price:
                        labels[i].config(text=label_text, fg="green")
                    elif current_price < previous_price:
                        labels[i].config(text=label_text, fg="red")
                    else:
                        labels[i].config(text=label_text, fg="black")
                else:
                    labels[i].config(text=label_text, fg="black")
                
                previous_prices[symbol] = current_price

                if symbol in previous_log_prices and current_price != previous_log_prices[symbol]:
                    log_price_change(symbol, previous_log_prices[symbol], current_price)

                previous_log_prices[symbol] = current_price

        window.after(5000, update_labels)

    previous_prices = {}
    previous_log_prices = {}
    update_labels()

    window.mainloop()

def log_price_change(symbol, previous_price, current_price):
    log_filename = "price_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_filename, "a") as file:
        file.write(f"{timestamp} - {symbol}: {previous_price} -> {current_price}\n")

if __name__ == "__main__":
    update_prices()

    create_gui()