from tkinter import Tk, Button, Label, Toplevel, PhotoImage, StringVar, ttk
from PIL import Image, ImageTk
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt

class Cryptocurrency_Flow_Investigation:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1430x750")
        self.root.title("Cryptocurrency Flow Investigation")

        # Load the background image
        img = Image.open("C:/Users/Sairam Gudeli/Desktop/NEW WEBSITE/bback.jpg")
        img = img.resize((1430, 750), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(img)

        background_label = Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        text_label = ttk.Label(root, text="Cryptocurrency Flow Investigation", font=("Time Of Roman", 40))
        text_label.pack()

        # List of cryptocurrencies to populate the Combobox
        crypto_list = ["Bitcoin", "Ethereum", "Litecoin", "USD", "Binancecoin", "Ripple", "Solana", "Cardano",
                  "Polkadot", "Dogecoin", "Tron", "Chainlink", "Polygon", "Shiba", "Dai",
                  "bitcoincash", "Cosmos",]

        # Combobox for selecting cryptocurrency
        self.crypto_var = StringVar()

        crypto_combobox = ttk.Combobox(self.root, textvariable=self.crypto_var, values=crypto_list)
        crypto_combobox.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.05)

        button1 = Button(self.root, text="Button 1", bg="blue", fg="white", width=20, height=2, command=self.button1_click)
        button1.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

        button2 = Button(self.root, text="Button 2", bg="blue", fg="white", width=20, height=2, command=self.button2_click)
        button2.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

        button3 = Button(self.root, text="Button 3", bg="blue", fg="white", width=20, height=2, command=self.button3_click)
        button3.place(relx=0.1, rely=0.7, relwidth=0.2, relheight=0.1)

        # ... (remaining buttons)

    def button1_click(self):
        selected_crypto = self.crypto_var.get()
        print(f"Button 1 clicked - Tracking {selected_crypto}")
        self.track_crypto_price(selected_crypto)

    def button2_click(self):
        print("Button 2 clicked")
        self.show_rules_details()

    def button3_click(self):
        print("Button 3 clicked")

    # ... (remaining button click methods)

    def show_rules_details(self):
        new_window = Toplevel(self.root)
        new_window.title("Law and Rules")
        new_window.geometry("800x600")

        label_text = "Summary of Cryptocurrency Regulation in India (2024):\n\n" \
                     "1. VDAs as Legal Tender:\n" \
                     "   • VDAs are not expressly regulated or prohibited.\n" \
                     "   • Individuals and entities allowed to hold, invest, and transact VDAs under existing laws.\n" \
                     "   • Government does not recognize cryptocurrencies as legal tender but acknowledges their dual nature.\n" \
                     "   • 2020 Supreme Court judgment highlights the evolving global understanding of VDAs.\n\n" \
                     "2. Sales Regulation:\n" \
                     "   • Legacy legislation triggers in certain circumstances.\n" \
                     "   • Regulatory mechanism based on VDA use case, treated as commodities/assets in some scenarios.\n" \
                     "   • Advertising guidelines set by the Advertising Standards Council of India in 2022.\n\n" \
                     "3. Taxation:\n" \
                     "   • Income from VDA trade subject to both direct (income tax) and indirect (GST) taxation.\n" \
                     "   • Finance Act 2022 introduces a 30% tax on income from VDA transfers.\n" \
                     "   • Guidelines for Exchanges and P2P transactions regarding withholding tax and GST.\n\n" \
                     "4. Money Transmission Laws and AML Requirements:\n" \
                     "   • RBI circulars regulate entities handling VDAs, following KYC, AML, and CFT requirements.\n" \
                     "   • Supreme Court overturns the ban on regulated entities dealing with VDAs.\n" \
                     "   • PMLA scope expanded to cover various VDA-related aspects, emphasizing regulatory oversight.\n" \
                     "   • CERT-In issues directions for virtual asset service providers, exchange providers, and custodian wallet providers to maintain KYC and transaction records for five years.\n\n" \
                     "5. Central Bank Digital Currency (CBDC):\n" \
                     "   • RBI initiates the e-Rupee CBDC pilot, broadening the definition of 'bank note' to include digital forms.\n\n" \
                     "6. RBI on Macro-Financial Risks:\n" \
                     "   • RBI addresses risks associated with VDAs, proposing three policy approaches: prohibition, containment, and regulation.\n" \
                     "   • Global coordination needed for evaluating risks, especially in Emerging Markets and Developing Economies."

        label = Label(new_window, text=label_text, font=("Time Of Roman", 12), justify='left', bg='white')
        label.pack(pady=20)

    def track_crypto_price(self, crypto):
        while True:
            crypto_data = self.get_crypto_data(crypto)
            if crypto_data:
                price = self.get_crypto_price(crypto_data)
                if price is not None:
                    print(f"The current price of {crypto} is ${price}")
                else:
                    print(f"Error retrieving price for {crypto}")
            else:
                print(f"Error retrieving data for {crypto}")
            time.sleep(60)

    def get_crypto_data(self, crypto):
        url = f"https://api.coingecko.com/api/v3/coins/{crypto.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error retrieving data for {crypto}: {response.status_code}")
            return None

    def get_crypto_price(self, crypto_data):
        # Check if 'market_data' is present in the response
        if 'market_data' in crypto_data:
            # Check if 'current_price' is present in the 'market_data'
            if 'current_price' in crypto_data['market_data']:
                # Access the 'usd' price directly
                price = crypto_data['market_data']['current_price']['usd']
                return price

        # If any of the expected keys is not present, print an error message
        print(f"Error: Unable to retrieve current price for {crypto_data['name']}")
        return None

    def display_price_history(self, crypto, days=30, interval="daily"):
        url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days={days}&interval={interval}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            prices = data['prices']

            dates = [item[0] for item in prices]
            dates = [datetime.fromtimestamp(date / 1000.0).strftime('%Y-%m-%d') for date in dates]

            prices = [item[1] for item in prices]

            plt.plot(dates, prices)
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title(f'Price History of {crypto}')
            plt.show()
        else:
            print(f"Error retrieving price history for {crypto}: {response.status_code}")

    def live_track_and_show_history(self, crypto, show_history=True):
        crypto_data = self.get_crypto_data(crypto)
        if crypto_data:
            print(f"The current price of {crypto} is ${self.get_crypto_price(crypto_data)}")

            if show_history:
                self.display_price_history(crypto)

if __name__ == "__main__":
    root = Tk()
    obj = Cryptocurrency_Flow_Investigation(root)
    root.mainloop()
