import math
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True     

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def calculate_keys():
    try:
        bit_length = int(entry_bit_length.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the bit length.")
        progress_bar.stop()
        return
    
    P = generate_prime(bit_length)
    G = generate_prime(bit_length)

    b = 3
    a = 4

    X = pow(G, a, P)
    Y = pow(G, b, P)

    Ka = pow(Y, a, P)
    Kb = pow(X, b, P)

    label_result.config(text=f"Ka = {Ka}\nKb = {Kb}")
    progress_bar.stop()

def retry():
    messagebox.destroy()
    start_progressbar()

# GUI setup (unchanged from the previous code snippet)

def start_progressbar():
    progress_bar.pack(pady=10)
    progress_bar.start(interval=10)
    root.after(3000, calculate_keys)  # Simulating 3 seconds delay for the calculation

root = tk.Tk()
root.title("Diffie-Hellman Key Exchange")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label_bit_length = tk.Label(frame, text="Enter the bit length:")
label_bit_length.pack()

entry_bit_length = tk.Entry(frame)
entry_bit_length.pack()

calculate_button = tk.Button(frame, text="Calculate Keys", command=lambda: start_progressbar())
calculate_button.pack(pady=10)

label_result = tk.Label(frame, text="")
label_result.pack()

progress_bar = ttk.Progressbar(frame, orient='horizontal', length=200, mode='indeterminate')

root.mainloop()
