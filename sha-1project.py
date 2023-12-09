import tkinter as tk
from tkinter import messagebox,ttk
import threading

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(message):
    # Convert message to string if it's not already
    message_str = str(message)

    # Convert each character to 8-bit binary representation
    mes_bin = ''.join(bin(ord(i))[2:].zfill(8) for i in message_str)
    mes_len = len(mes_bin)

    mes_bin += '1'  # Append '1' bit as the start of padding

    if mes_len % 512 < 448:
        padd = 448 - (mes_len % 512)
    else:
        padd = 512 - (mes_len % 512) + 448  # Calculate overflow

    # Append '0' bits until congruent to 448 (mod 512)
    mes_bin += '0' * padd

    # Convert message length to binary
    msg_len_bin = bin(mes_len)[2:].zfill(64)

    # Append zeros followed by message length binary
    mes_bin += msg_len_bin

    # Process message in 512-bit chunks
    words = [0] * 80

    # Break message into 32-bit words (initial 16 words)
    for i in range(0, len(mes_bin), 32):
        words[i // 32] = int(mes_bin[i:i+32], 2)

    # Extend words to 80 words
    for i in range(16, 80):
        words.append(left_rotate(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1) & 0xFFFFFFFF)

    # Initialize variables
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Main loop
    for i in range(80):
        if 0 <= i <= 19:
            f = (h1 & h2) | ((~h1) & h3)
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = h1 ^ h2 ^ h3
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (h1 & h2) | (h1 & h3) | (h2 & h3)
            k = 0x8F1BBCDC
        else:
            f = h1 ^ h2 ^ h3
            k = 0xCA62C1D6

        temp = (left_rotate(h0, 5) + f + h4 + k + words[i]) & 0xFFFFFFFF
        h4 = h3
        h3 = h2
        h2 = left_rotate(h1, 30)
        h1 = h0
        h0 = temp

    # Update hash values for this chunk
    h0 = (h0 + 0x67452301) & 0xFFFFFFFF
    h1 = (h1 + 0xEFCDAB89) & 0xFFFFFFFF
    h2 = (h2 + 0x98BADCFE) & 0xFFFFFFFF
    h3 = (h3 + 0x10325476) & 0xFFFFFFFF
    h4 = (h4 + 0xC3D2E1F0) & 0xFFFFFFFF

    # Produce the final hash value
    final_hash = '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)
    return final_hash


#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------


# Your SHA-1 function and other code remain unchanged

def calculate_hash():
    text = entry_text.get()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    # Disable the Calculate button during hashing
    calculate_button.config(state=tk.DISABLED)

    progress_bar['value'] = 0  # Reset progress bar value

    def update_progress():
        progress = 0
        while progress <= 100:
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")  # Update the percentage label
            progress += 5  # Simulating progress
            root.update_idletasks()
            root.after(200)  # Adjust the timing for smooth progress
        finish_hashing()

    def finish_hashing():
        progress_bar['value'] = 100
        percent_label.config(text="100%")  # Ensure it displays 100% at the end
        hash_result = sha1(text)
        label_hash.config(text=f"Hash Value: {hash_result}")
        calculate_button.config(state=tk.NORMAL)  # Enable the button after hashing

    # Use threading to prevent the GUI from freezing during progress simulation
    threading.Thread(target=update_progress).start()

def copy_hash():
    hash_value = label_hash.cget("text").split(": ")[-1]  # Extracting the hash value from the label
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(hash_value)  # Copy the hash value to the clipboard
    root.update()  # Ensure the update takes place

    # Provide a visual confirmation to the user
    messagebox.showinfo("Success", "Hash value copied to clipboard!")


# GUI setup (unchanged)
root = tk.Tk()
root.title("SHA-1 Hash Calculator")
root.configure(bg='#FFD0D0')  # Set background color for the root window

frame = tk.Frame(root, bg='#FFD0D0')  # Set background color for the frame
frame.pack(padx=20, pady=20)

label_text = tk.Label(frame, text="Enter Text:", bg='#FFD0D0', fg='#080202')  # Set text and background color for label
label_text.pack()

entry_text = tk.Entry(frame, width=40)
entry_text.pack()

calculate_button = tk.Button(frame, text="Calculate Hash", command=calculate_hash, bg='#FF9EAA',fg='#080202')  # Set button colors
calculate_button.pack(pady=10)

copy_button = tk.Button(frame, text="Copy Hash", command=copy_hash, bg='#FF9EAA', fg='#080202')  # Set button colors
copy_button.pack(pady=5)

label_hash = tk.Label(frame, text="Hash Value: ", bg='#FFD0D0', fg='#080202')  # Set text and background color for label
label_hash.pack()

percent_label = tk.Label(frame, text="0%", bg='#FFD0D0', fg='#080202')  # Set text and background color for label
percent_label.pack()

style = ttk.Style()
style.theme_use('clam')  # Change the theme to access element options
style.configure("custom.Horizontal.TProgressbar", troughcolor='#FFD0D0', bordercolor='#3AA6B9', background='#3AA6B9')  # Configure progress bar colors

progress_bar = ttk.Progressbar(frame, orient='horizontal', length=200, mode='determinate', style="custom.Horizontal.TProgressbar")
progress_bar.pack(pady=10)

root.mainloop()