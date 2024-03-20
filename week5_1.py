import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CarParkPaymentSystem:
    def __init__(self):
        self.daily_total_payments = 0

    def calculate_check_digit(self, number):
        total = sum(int(digit) * (i + 1) for i, digit in enumerate(number))
        return total % 11

    def is_valid_frequent_number(self, number):
        if len(number) != 5 or not number[:-1].isdigit():
            return False
        return int(number[-1]) == self.calculate_check_digit(number[:-1])

    def calculate_price(self, day, arrival_hour, parking_hours, frequent_parking_number=None):
        # Constants
        prices = {
            "Sunday": 2.00,
            "Monday": 10.00,
            "Tuesday": 10.00,
            "Wednesday": 10.00,
            "Thursday": 10.00,
            "Friday": 10.00,
            "Saturday": 3.00
        }
        discount = 0.5 if arrival_hour >= 16 else 0.1
        if frequent_parking_number and self.is_valid_frequent_number(frequent_parking_number):
            discount += 0.4

        # Calculate total price
        total_price = 0
        for hour in range(parking_hours):
            hour_price = prices[day]
            if arrival_hour + hour >= 24:
                arrival_hour -= 24  # Reset to 0 after midnight
            if arrival_hour + hour >= 16:
                hour_price *= (1 - 0.5)
            else:
                hour_price *= (1 - discount)
            total_price += hour_price

        return total_price

    def process_payment(self, amount):
        self.daily_total_payments += amount

    def get_daily_total_payments(self):
        return self.daily_total_payments

    def reset_daily_total(self):
        self.daily_total_payments = 0

class CarParkPaymentGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Car Park Payment System')
        self.payment_system = CarParkPaymentSystem()
        self.create_widgets()

    def create_widgets(self):
        # Day Drop-down Menu
        tk.Label(self.master, text="Day:").grid(row=0, column=0)
        self.day_var = tk.StringVar()
        self.day_combobox = ttk.Combobox(self.master, textvariable=self.day_var, state="readonly")
        self.day_combobox['values'] = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
        self.day_combobox.grid(row=0, column=1)
        self.day_combobox.current(0)

        # Arrival Hour Drop-down Menu
        tk.Label(self.master, text="Arrival Hour:").grid(row=1, column=0)
        self.arrival_hour_var = tk.StringVar()
        self.arrival_hour_combobox = ttk.Combobox(self.master, textvariable=self.arrival_hour_var, state="readonly", width=5)
        self.arrival_hour_combobox['values'] = [str(hour) for hour in range(8, 24)]
        self.arrival_hour_combobox.grid(row=1, column=1)
        self.arrival_hour_combobox.current(0)

        # Parking Hours Drop-down Menu
        tk.Label(self.master, text="Parking Hours:").grid(row=2, column=0)
        self.parking_hours_var = tk.StringVar()
        self.parking_hours_combobox = ttk.Combobox(self.master, textvariable=self.parking_hours_var, state="readonly", width=5)
        self.parking_hours_combobox['values'] = [str(hour) for hour in range(1, 25)]
        self.parking_hours_combobox.grid(row=2, column=1)
        self.parking_hours_combobox.current(0)

        # Frequent Parking Number Entry
        tk.Label(self.master, text="Frequent Parking Number:").grid(row=3, column=0)
        self.frequent_parking_number_entry = tk.Entry(self.master)
        self.frequent_parking_number_entry.grid(row=3, column=1)

        # Calculate Button
        self.calculate_button = tk.Button(self.master, text="Calculate Price", command=self.calculate_price)
        self.calculate_button.grid(row=4, column=0, columnspan=2)

        # Total Payments Label
        self.total_payments_label = tk.Label(self.master, text="Daily Total Payments: 0")
        self.total_payments_label.grid(row=5, column=0, columnspan=2)

    def calculate_price(self):
        day = self.day_combobox.get()
        arrival_hour = int(self.arrival_hour_combobox.get())
        parking_hours = int(self.parking_hours_combobox.get())
        frequent_parking_number = self.frequent_parking_number_entry.get()

        price = self.payment_system.calculate_price(day, arrival_hour, parking_hours, frequent_parking_number)
        messagebox.showinfo("Price", f"The price to park is: {price:.2f}")
        self.payment_system.process_payment(price)
        self.total_payments_label.config(text=f"Daily Total Payments: {self.payment_system.get_daily_total_payments():.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarParkPaymentGUI(root)
    root.mainloop()
