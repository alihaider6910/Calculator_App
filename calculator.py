import tkinter as tk
from tkinter import ttk
import math
import time

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Variable to store current calculation
        self.current = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Animation variables
        self.animation_running = False
        self.button_states = {}

        # Create display
        self.create_display()
        # Create buttons
        self.create_buttons()

    def create_display(self):
        display_frame = tk.Frame(self.root, bg="#f0f0f0")
        display_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 24),
            bg="#ffffff",
            anchor="e",
            padx=10
        )
        self.result_label.pack(expand=True, fill="both")

    def animate_button(self, button, original_color):
        if button in self.button_states and self.button_states[button]:
            return

        self.button_states[button] = True
        button.configure(bg="#e0e0e0")
        self.root.after(100, lambda: self.reset_button_color(button, original_color))

    def reset_button_color(self, button, original_color):
        button.configure(bg=original_color)
        self.button_states[button] = False

    def animate_display(self, new_value):
        if self.animation_running:
            return

        self.animation_running = True
        original_font = self.result_label.cget("font")
        self.result_label.configure(font=("Arial", 28))
        
        def reset_font():
            self.result_label.configure(font=original_font)
            self.animation_running = False

        self.root.after(100, reset_font)

    def create_buttons(self):
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Button layout
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 2), ('.', 4, 2), ('=', 4, 3)
        ]

        # Configure grid
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # Create and place buttons
        for button in buttons:
            if len(button) == 4:  # Special case for '0' button
                btn = tk.Button(
                    buttons_frame,
                    text=button[0],
                    font=("Arial", 14),
                    command=lambda x=button[0]: self.button_click(x)
                )
                btn.grid(row=button[1], column=button[2], columnspan=button[3],
                        sticky="nsew", padx=2, pady=2)
            else:
                btn = tk.Button(
                    buttons_frame,
                    text=button[0],
                    font=("Arial", 14),
                    command=lambda x=button[0]: self.button_click(x)
                )
                btn.grid(row=button[1], column=button[2],
                        sticky="nsew", padx=2, pady=2)

            # Style buttons and add hover effects
            if button[0] in ['+', '-', '×', '÷', '=']:
                btn.configure(bg="#ff9500", fg="white")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#ffaa33"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#ff9500"))
            elif button[0] in ['C', '±', '%']:
                btn.configure(bg="#a5a5a5", fg="white")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#b8b8b8"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#a5a5a5"))
            else:
                btn.configure(bg="#ffffff")
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#f0f0f0"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#ffffff"))

            # Add click animation
            original_color = btn.cget("bg")
            btn.bind("<Button-1>", lambda e, b=btn, c=original_color: self.animate_button(b, c))

    def button_click(self, value):
        if value == 'C':
            self.current = ""
            self.result_var.set("0")
            self.animate_display("0")
        elif value == '=':
            try:
                # Replace × with * and ÷ with / for calculation
                expression = self.current.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.result_var.set(result)
                self.current = str(result)
                self.animate_display(str(result))
            except:
                self.result_var.set("Error")
                self.current = ""
                self.animate_display("Error")
        elif value == '±':
            try:
                current_value = float(self.current)
                self.current = str(-current_value)
                self.result_var.set(self.current)
                self.animate_display(self.current)
            except:
                pass
        elif value == '%':
            try:
                current_value = float(self.current)
                self.current = str(current_value / 100)
                self.result_var.set(self.current)
                self.animate_display(self.current)
            except:
                pass
        else:
            self.current += value
            self.result_var.set(self.current)
            self.animate_display(self.current)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop() 