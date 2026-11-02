import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from dateutil.relativedelta import relativedelta  # pip install python-dateutil αν χρειάζεται

class TruckTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Οδηγός Φορτηγού - Έσοδα/Έξοδα/Σέρβις")
        self.root.geometry("900x700")
        
        self.data_file = "truck_data.csv"
        self.df = self.load_data()
        self.filtered_df = self.df.copy()
        
        self.create_widgets()
        self.refresh_tree()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            return pd.read_csv(self.data_file)
        return pd.DataFrame(columns=['date', 'type', 'category', 'amount', 'description'])
    
    def save_data(self):
        self.df.to_csv(self.data_file, index=False)
    
    def add_entry(self):
        try:
            date = self.date_entry.get()
            typ = self.type_var.get()
            category = self.category_entry.get()
            amount = float(self.amount_entry.get() or 0)
            desc = self.desc_entry.get()
            
            new_row = pd.DataFrame({'date': [date], 'type': [typ], 'category': [category], 
                                    'amount': [amount], 'description': [desc]})
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save_data()
            self.filter_table()
            self.clear_entries()
            messagebox.showinfo("Επιτυχία", "Καταχώρηση προστέθηκε!")
        except ValueError:
            messagebox.showerror("Σφάλμα", "Ποσό πρέπει να είναι αριθμός!")
    
    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.type_var.set("income")
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
    
    def filter_table(self):
        filter_type = self.filter_var.get()
        if filter_type == "Όλα":
            self.filtered_df = self.df.copy()
        else:
            self.filtered_df = self.df[self.df['type'] == filter_type].copy()
        self.refresh_tree()
    
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, row in self.filtered_df.iterrows():
            self.tree.insert("", "end", values=(row['date'], row['type'], row['category'], f"{row['amount']:.2f}€", row['description']))
    
    def show_summary(self):
        try:
            months_back = int(self.months_var.get().split()[0])
            summary_type = self.summary_type_var.get()
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # Υπολογισμός περιόδου
            end_date = datetime(year, month, 1) + relativedelta(months=months_back)
            start_date = end_date - relativedelta(months=months_back)
            
            period_data = self.df[
                (pd.to_datetime(self.df['date']) >= start_date) & 
                (pd.to_datetime(self.df['date']) < end_date)
            ].copy()
            
            if summary_type != "Όλα":
                period_data = period_data[period_data['type'] == summary_type]
            
            income = period_data[period_data['type'] == 'income']['amount'].sum()
            # Έξοδα = expense + service
            expenses_data = period_data[period_data['type'].isin(['expense', 'service'])]
            total_expenses = expenses_data['amount'].sum()
            service_count = len(period_data[period_data['type'] == 'service'])
            
            profit = income - total_expenses
            
            msg = f"Σύνοψη {months_back} μήνα/ων ({start_date.strftime('%m/%Y')} - {end_date.strftime('%m/%Y')}):\n\n"
            if summary_type in ["income", "Όλα"]:
                msg += f"Έσοδα: {income:.2f}€\n"
            if summary_type in ["expense", "service", "Όλα"]:
                msg += f"Συνολικά Έξοδα (με σερβις): {total_expenses:.2f}€\n"
            if summary_type in ["service", "Όλα"]:
                msg += f"Σέρβις: {service_count} φορές (συμπεριλαμβάνονται στα έξοδα)\n"
            if summary_type in ["Όλα"]:
                msg += f"\nΚαθαρό Κέρδος: {profit:.2f}€"
            
            messagebox.showinfo("Σύνοψη", msg)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Πρόβλημα: {str(e)}")

    
    def create_widgets(self):
        # Φόρμα εισαγωγής (πάνω)
        form_frame = ttk.LabelFrame(self.root, text="Νέα Καταχώρηση")
        form_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(form_frame, text="Ημερομηνία:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Τύπος:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.type_var = tk.StringVar(value="income")
        ttk.Combobox(form_frame, textvariable=self.type_var, values=["income", "expense", "service"], state="readonly", width=8).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Κατηγορία:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = tk.Entry(form_frame, width=15)
        self.category_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        tk.Label(form_frame, text="Ποσό:").grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame, width=10)
        self.amount_entry.grid(row=1, column=4, padx=5, pady=5)
        
        tk.Label(form_frame, text="Περιγραφή:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(form_frame, width=40)
        self.desc_entry.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="ew")
        
        tk.Button(form_frame, text="Προσθήκη", command=self.add_entry).grid(row=3, column=0, columnspan=5, pady=10)
        
        # Φίλτρο πίνακα
        filter_frame = ttk.LabelFrame(self.root, text="Φίλτρο Πίνακα")
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(filter_frame, text="Εμφάνιση:").pack(side="left")
        self.filter_var = tk.StringVar(value="Όλα")
        ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Όλα", "income", "expense", "service"], 
                     state="readonly", width=10).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Εφαρμογή Φίλτρου", command=self.filter_table).pack(side="left", padx=5)
        
        # Πίνακας
        table_frame = ttk.LabelFrame(self.root, text="Καταχωρήσεις")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ('Ημερομηνία', 'Τύπος', 'Κατηγορία', 'Ποσό', 'Περιγραφή')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True)
        
        # Σύνοψη (νέα εμφάνιση)
        summary_frame = ttk.LabelFrame(self.root, text="Σύνοψη Περιόδου")
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        # Μήνας/Έτος
        tk.Label(summary_frame, text="Μήνας:").grid(row=0, column=0, sticky="w", padx=5)
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        ttk.Combobox(summary_frame, textvariable=self.month_var, values=[str(i) for i in range(1,13)], width=5, state="readonly").grid(row=0, column=1, padx=5)
        
        tk.Label(summary_frame, text="Έτος:").grid(row=0, column=2, sticky="w", padx=5)
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        ttk.Spinbox(summary_frame, from_=2020, to=2030, textvariable=self.year_var, width=8).grid(row=0, column=3, padx=5)
        
        # Περίοδος μηνών
        tk.Label(summary_frame, text="Μήνες πίσω:").grid(row=0, column=4, sticky="w", padx=5)
        self.months_var = tk.StringVar(value="1 μήνας")
        ttk.Combobox(summary_frame, textvariable=self.months_var, 
                     values=["1 μήνας", "2 μήνες", "3 μήνες", "4 μήνες", "5 μήνες", "6 μήνες", "12 μήνες"], 
                     state="readonly", width=10).grid(row=0, column=5, padx=5)
        
        # Τύπος συνοψης
        tk.Label(summary_frame, text="Τύπος:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.summary_type_var = tk.StringVar(value="Όλα")
        ttk.Combobox(summary_frame, textvariable=self.summary_type_var, values=["Όλα", "income", "expense", "service"], 
                     state="readonly", width=10).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
        
        tk.Button(summary_frame, text="Δείξε Σύνοψη", command=self.show_summary).grid(row=1, column=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckTracker(root)
    root.mainloop()
