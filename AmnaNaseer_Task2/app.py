import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import database as db
import bmi_logic as logic

# Color Palette Constants
BG_COLOR = "#f8f9fa"       # Soft off-white background
CARD_BG = "#ffffff"        # Container white
TEXT_COLOR = "#212529"     # Dark charcoal text
PRIMARY_COLOR = "#3b82f6"  # Blue action color

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Health Tracker")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)

        # Initialize Database
        try:
            db.init_db()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database:\n{e}")

        # Apply Modern Native TTK Styling
        self.setup_styles()
        self.setup_ui()
        self.refresh_user_list()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Global Frame Backgrounds
        self.style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        self.style.configure("Card.TFrame", background=CARD_BG, relief="flat")
        
        # Section Headers
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), background=CARD_BG, foreground="#1e293b")
        self.style.configure("Field.TLabel", font=("Segoe UI", 10), background=CARD_BG, foreground="#64748b")

        # Custom Buttons
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background=PRIMARY_COLOR,
            foreground="#ffffff",
            borderwidth=0,
            padding=(12, 8)
        )
        self.style.map("Primary.TButton", background=[("active", "#2563eb")])

        self.style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            background="#e2e8f0",
            foreground="#334155",
            borderwidth=0,
            padding=(12, 8)
        )
        self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

        # Combobox and Entry styling
        self.style.configure("TCombobox", padding=5)
        self.style.configure("TEntry", padding=5)

    def setup_ui(self):
        # Top Container Card
        input_card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        input_card.pack(fill="x", padx=20, pady=15)

        # Header Title
        ttk.Label(input_card, text="Personal Details", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Inputs Form
        ttk.Label(input_card, text="Select User:", style="Field.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        self.user_combo = ttk.Combobox(input_card, font=("Segoe UI", 10))
        self.user_combo.grid(row=1, column=1, padx=(10, 20), pady=6, sticky="ew")

        ttk.Label(input_card, text="Weight (kg):", style="Field.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.weight_entry = ttk.Entry(input_card, font=("Segoe UI", 10))
        self.weight_entry.grid(row=2, column=1, padx=(10, 20), pady=6, sticky="ew")

        ttk.Label(input_card, text="Height (m):", style="Field.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        self.height_entry = ttk.Entry(input_card, font=("Segoe UI", 10))
        self.height_entry.grid(row=3, column=1, padx=(10, 20), pady=6, sticky="ew")

        # Buttons Panel
        btn_frame = ttk.Frame(input_card, style="Card.TFrame")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky="w")

        calc_btn = ttk.Button(btn_frame, text="Calculate & Save", style="Primary.TButton", command=self.handle_calculate)
        calc_btn.pack(side="left", padx=(0, 10))

        graph_btn = ttk.Button(btn_frame, text="View History Graph", style="Secondary.TButton", command=self.handle_show_graph)
        graph_btn.pack(side="left")

        # Right Dynamic Feedback Card
        self.result_card = tk.Label(
            input_card,
            text="Enter parameters\nto calculate",
            font=("Segoe UI", 11, "bold"),
            bg="#f1f5f9",
            fg="#475569",
            padx=20,
            pady=20,
            width=22,
            relief="flat"
        )
        self.result_card.grid(row=0, column=2, rowspan=5, padx=(20, 0), sticky="nsew")

        input_card.columnconfigure(1, weight=1)

        # Bottom Graph Container Card
        self.plot_card = ttk.Frame(self.root, style="Card.TFrame", padding=15)
        self.plot_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh_user_list(self):
        users = db.get_all_users()
        self.user_combo['values'] = users
        if users:
            self.user_combo.current(0)

    def handle_calculate(self):
        user_name = self.user_combo.get().strip()
        weight_raw = self.weight_entry.get()
        height_raw = self.height_entry.get()

        if not user_name:
            messagebox.showwarning("Input Error", "Please select or type a user name.")
            return

        try:
            weight, height = logic.validate_and_parse_inputs(weight_raw, height_raw)
        except ValueError as err:
            messagebox.showerror("Validation Error", str(err))
            return

        bmi, category, color = logic.calculate_bmi(weight, height)

        try:
            user_id = db.add_user(user_name)
            db.save_bmi_record(user_id, weight, height, bmi, category)
            self.refresh_user_list()
            self.user_combo.set(user_name)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save record:\n{e}")
            return

        # Update formatted result display
        self.result_card.config(
            text=f"USER: {user_name.upper()}\n\nBMI: {bmi}\n[{category}]",
            bg=color,
            fg="#ffffff"
        )

        self.handle_show_graph()

    def handle_show_graph(self):
        user_name = self.user_combo.get().strip()
        if not user_name:
            messagebox.showwarning("Selection Error", "Please select a user to view history.")
            return

        try:
            users = db.get_all_users()
            if user_name not in users:
                messagebox.showinfo("No Data", f"No saved records found for '{user_name}'.")
                return

            user_id = db.add_user(user_name)
            history = db.get_user_history(user_id)

            if not history:
                messagebox.showinfo("No Data", f"No records available for {user_name}.")
                return

            timestamps = [row["timestamp"] for row in history]
            bmi_values = [row["bmi"] for row in history]

            # Clear plot memory and canvas container
            plt.close('all')
            for widget in self.plot_card.winfo_children():
                widget.destroy()

            # Matplotlib Styling (Matches Tkinter Theme)
            fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
            fig.patch.set_facecolor(CARD_BG)
            ax.set_facecolor(CARD_BG)

            ax.plot(timestamps, bmi_values, marker='o', color='#3b82f6', linewidth=2.5, markersize=6)
            
            # Subtle indicator lines
            ax.axhline(18.5, color='#0284c7', linestyle=':', alpha=0.6, label="Underweight (<18.5)")
            ax.axhline(25.0, color='#d97706', linestyle=':', alpha=0.6, label="Overweight (≥25.0)")
            ax.axhline(30.0, color='#dc2626', linestyle=':', alpha=0.6, label="Obese (≥30.0)")

            ax.set_title(f"BMI History for {user_name}", fontsize=11, color="#1e293b", pad=12)
            ax.tick_params(axis='x', rotation=25, labelsize=8, labelcolor="#64748b")
            ax.tick_params(axis='y', labelsize=8, labelcolor="#64748b")
            
            # Clean borders (spines removal)
            for spine in ["top", "right", "left", "bottom"]:
                ax.spines[spine].set_visible(False)
            ax.grid(axis='y', linestyle='--', alpha=0.3)

            ax.legend(fontsize=8, loc="upper left", frameon=False)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_card)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Plotting Error", f"Failed to render chart:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()