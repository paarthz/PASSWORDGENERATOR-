import tkinter as tk
from tkinter import filedialog
import random
import string

def generate_secure_password(length=12, security_level='medium', custom_charset=None):
    if length < 4:
        raise ValueError("Password length should be at least 4 characters to include all character types.")

    if security_level == 'low':
        all_characters = 'abcdefghijklmnopqrstuvwxyz'  + '0123456789'
    elif security_level == 'medium':
        all_characters = 'abcdefghijklmnopqrstuvwxyz' + '0123456789' + '!@#$%^&*()'
    elif security_level == 'high':
        all_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + '0123456789' + '!@#$%^&*()'
    elif security_level == 'custom' and custom_charset:
        all_characters = custom_charset
    else:
        raise ValueError("Invalid security level or custom character set not provided")

    password = [
        random.choice(all_characters)
        for _ in range(length)
    ]

    random.shuffle(password)
    return ''.join(password)

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")

        self.label = tk.Label(master, text="Enter the number of passwords to generate (1-10):")
        self.label.pack()

        self.num_passwords_entry = tk.Entry(master)
        self.num_passwords_entry.insert(0, "5")  # Default value
        self.num_passwords_entry.pack()

        self.length_label = tk.Label(master, text="Enter the password length:")
        self.length_label.pack()

        self.length_entry = tk.Entry(master)
        self.length_entry.insert(0, "16")  # Default value
        self.length_entry.pack()

        self.security_label = tk.Label(master, text="Select password security level:")
        self.security_label.pack()

        self.security_level = tk.StringVar(value='medium')
        self.low_radio = tk.Radiobutton(master, text="Low", variable=self.security_level, value='low', command=self.toggle_custom_charset)
        self.low_radio.pack()
        self.medium_radio = tk.Radiobutton(master, text="Medium", variable=self.security_level, value='medium', command=self.toggle_custom_charset)
        self.medium_radio.pack()
        self.high_radio = tk.Radiobutton(master, text="High", variable=self.security_level, value='high', command=self.toggle_custom_charset)
        self.high_radio.pack()
        self.custom_radio = tk.Radiobutton(master, text="Custom", variable=self.security_level, value='custom', command=self.toggle_custom_charset)
        self.custom_radio.pack()

        self.custom_charset_label = tk.Label(master, text="Enter custom character set:")
        self.custom_charset_label.pack()
        self.custom_charset_entry = tk.Entry(master)
        self.custom_charset_entry.pack()
        self.custom_charset_entry.configure(state='disabled')

        self.save_button = tk.Button(master, text="Save to File", command=self.save_to_file, state='disabled')
        self.save_button.pack()

        self.show_button = tk.Button(master, text="Show Passwords", command=self.show_passwords)
        self.show_button.pack()

        self.passwords_text = tk.Text(master, height=10, width=50)
        self.passwords_text.pack()

    def toggle_custom_charset(self):
        if self.security_level.get() == 'custom':
            self.custom_charset_entry.configure(state='normal')
        else:
            self.custom_charset_entry.configure(state='disabled')

    def save_to_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_name:
            return  # User canceled operation

        with open(file_name, 'w') as file:
            file.write(self.passwords_text.get(1.0, tk.END))

    def show_passwords(self):
        self.passwords_text.delete(1.0, tk.END)
        try:
            num_passwords = int(self.num_passwords_entry.get())
            if num_passwords < 1 or num_passwords > 10:
                raise ValueError
        except ValueError:
            self.passwords_text.insert(tk.END, "Please enter a valid number between 1 and 10.\n")
            self.save_button.config(state='disabled')
            return

        try:
            password_length = int(self.length_entry.get())
            if password_length < 4:
                raise ValueError
        except ValueError:
            self.passwords_text.insert(tk.END, "Please enter a valid password length of at least 4.\n")
            self.save_button.config(state='disabled')
            return

        security_level = self.security_level.get()
        custom_charset = self.custom_charset_entry.get() if security_level == 'custom' else None

        if security_level == 'custom' and not custom_charset:
            self.passwords_text.insert(tk.END, "Please enter a custom character set.\n")
            self.save_button.config(state='disabled')
            return

        for _ in range(num_passwords):
            try:
                password = generate_secure_password(password_length, security_level, custom_charset)
                self.passwords_text.insert(tk.END, f"{password}\n")
            except ValueError as e:
                self.passwords_text.insert(tk.END, f"Error: {str(e)}\n")
                break

        self.save_button.config(state='normal')

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
