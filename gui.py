import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
from tkcalendar import DateEntry 
from datetime import datetime

import db_functions

class TableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Credits manager")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        root.resizable(False, False)
        self.root.configure(bg="#fbf2fc")

        self.create_start_window()

        self.style = ttk.Style()
        self.style.configure("Treeview", background="#FFDAB9", fieldbackground="#FFDAB9", font=("Comic Sans MS", 12))
        self.style.configure("TLabel", font=("Comic Sans MS", 12))

        self.connection, self.cursor = db_functions.create_connection()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to close the application?"):
            db_functions.close_connection(self.cursor, self.connection)
            self.root.destroy()

    def create_start_window(self):
        self.clear_window()

        title_label = tk.Label(self.root, text="Select a Table", font=("Comic Sans MS", 24), bg="#fbf2fc")
        title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        table1_button = tk.Button(self.root, text="Credits", command=lambda: self.show_table("CREDIT"), bg="#FFB3DE", font=("Comic Sans MS", 14))
        table2_button = tk.Button(self.root, text="Legal entities", command=lambda: self.show_table("UL"), bg="#FFB3DE", font=("Comic Sans MS", 14))
        table3_button = tk.Button(self.root, text="Fines", command=lambda: self.show_table("FINE"), bg="#FFB3DE", font=("Comic Sans MS", 14))

        table1_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        table2_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        table3_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def show_table(self, table_name):
        self.table_name = table_name
        self.data = db_functions.fetch_data(self.cursor, self.table_name)
        self.columns = db_functions.get_column_names(self.cursor, self.table_name)
        self.create_table_window()

    def create_table_window(self):
        self.clear_window()

        title_label = tk.Label(self.root, text="Table Data", font=("Comic Sans MS", 24), bg="#fbf2fc")
        title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.tree = ttk.Treeview(frame, columns=self.columns, show='headings', height=6)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        window_width = self.root.winfo_width()
        column_width = window_width // (len(self.columns) + 1)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_width)

        for i, item in enumerate(self.data):
            if i % 2 == 0:
                self.tree.insert("", "end", values=item, tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=item, tags=('oddrow',))

        self.tree.tag_configure('evenrow', background='#ffd1eb')
        self.tree.tag_configure('oddrow', background='#FFB3DE')

        delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_selected, bg="#FFB3DE", font=("Comic Sans MS", 14))
        delete_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        sort_label = tk.Label(self.root, text="Sort by:", font=("Comic Sans MS", 12), bg="#fbf2fc")
        sort_label.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

        self.sort_field = Combobox(self.root, values=self.columns)
        self.sort_field.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        sort_button = tk.Button(self.root, text="Sort", command=self.sort_data, bg="#FFB3DE", font=("Comic Sans MS", 14))
        sort_button.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

        update_button = tk.Button(self.root, text="Update Selected", command=self.update_selected, bg="#FFB3DE", font=("Comic Sans MS", 14))
        update_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        insert_button = tk.Button(self.root, text="Insert new", command=self.insert_data, bg="#FFB3DE", font=("Comic Sans MS", 14))
        insert_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        back_button = tk.Button(
            self.root,
            text="Back to Main Menu",
            command=self.go_to_start_window,
            bg="#FFB3DE",
            font=("Comic Sans MS", 14)
        )
        back_button.place(relx=1, rely=0, anchor=tk.NE)

        show_info_button = tk.Button(
            self.root,
            text="Show Info",
            command=self.show_info, 
            bg="#FFB3DE",
            font=("Comic Sans MS", 14)
        )
        show_info_button.place(relx=0, rely=0, anchor=tk.NW)

    def show_info(self):
        messagebox.showinfo("Author", "Ihnatchyk Ulyana Sergeevna\n3 course 11 group\n2024")


    def sort_data(self):
        selected_field = self.sort_field.get()
        self.data = db_functions.sort_by_field(self.cursor, self.table_name, selected_field)
        self.connection.commit()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, item in enumerate(self.data):
            if i % 2 == 0:
                self.tree.insert("", "end", values=item, tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=item, tags=('oddrow',))

    def update_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_row = self.tree.item(selected_item)['values']

            update_window = tk.Toplevel(self.root)
            update_window.title("Update Data")
            update_window.resizable(False, False)
            update_window.configure(bg="#fbf2fc")

            fields = []
            for col, value in zip(self.columns, selected_row):
                label = tk.Label(update_window, text=col, bg="#fbf2fc", font=("Comic Sans MS", 12))
                label.grid(row=len(fields), column=0, padx=10, pady=5)

                if col in ('LOAN_DATE', 'FINE_DATE', 'CREATEDATE'):
                    entry = DateEntry(
                        update_window,
                        width=12,
                        background='#FFB3DE',
                        foreground='black',
                        borderwidth=2,
                        selectbackground='#ffd1eb'
                    )
                    entry.delete(0, tk.END)  
                    entry.insert(0, value)  
                else:
                    entry = tk.Entry(update_window, font=("Comic Sans MS", 12))
                    entry.insert(0, str(value))  

                if col in ("ID", "CREDITID", "INN"):
                    entry.config(state='disabled')

                entry.grid(row=len(fields), column=1, padx=10, pady=5)
                fields.append((col, entry))

            update_button = tk.Button(
                update_window,
                text="Update",
                command=lambda selected_item=selected_item, fields=fields, update_window=update_window: self.update_data_in_db(self.cursor, self.table_name, selected_item, fields, update_window),
                bg="#FFB3DE", font=("Comic Sans MS", 14)
            )
            update_button.grid(row=len(fields), columnspan=2, padx=10, pady=10)
        else:
            messagebox.showwarning("Warning", "Select an item to update.")

    def update_data_in_db(self, cursor, table_name, selected_item, fields, update_window):
        id = self.tree.item(selected_item[0])['values'][0]
        updated_data = {}
        for field in fields:
            col, entry = field
            if col in ('LOAN_DATE', 'FINE_DATE', 'CREATEDATE'): 
                date = entry.get()
                date_object = datetime.strptime(date, "%m/%d/%y")
                formatted_date = date_object.strftime("%Y-%m-%d")
                updated_data[col] = formatted_date
            else:
                updated_data[col] = entry.get()
        for col, value in updated_data.items():
            db_functions.update_field(cursor, table_name, col, value, id)
            self.connection.commit()
        self.refresh_table()
        update_window.destroy()

    def refresh_table(self):
        self.data = db_functions.fetch_data(self.cursor, self.table_name)
        self.columns = db_functions.get_column_names(self.cursor, self.table_name)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, item in enumerate(self.data):
            if i % 2 == 0:
                self.tree.insert("", "end", values=item, tags=('evenrow',))
            else:
                self.tree.insert("", "end", values=item, tags=('oddrow',))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item_id in selected_item:
                item = self.tree.item(item_id)
                if self.table_name == 'CREDIT':   
                    id_value = item['values'][self.columns.index('CREDITID')]
                elif self.table_name == 'UL':   
                    id_value = item['values'][self.columns.index('INN')]
                elif self.table_name == 'FINE':   
                    id_value = item['values'][self.columns.index('ID')]
            self.tree.delete(selected_item)
            db_functions.delete_row(self.cursor, self.table_name, str(id_value))
            self.connection.commit()
            self.refresh_table()
        else:
            messagebox.showwarning("Warning", "Select an item to delete.")


    def insert_data(self):
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Insert Data")
        insert_window.configure(bg="#fbf2fc")
        insert_window.resizable(False, False)

        fields = []
        for col in self.columns:
            if col != 'ID':
                if col == 'CREDITID' and self.table_name == 'FINE':
                    label = tk.Label(insert_window, text=col, bg="#fbf2fc", font=("Comic Sans MS", 12))
                    label.grid(row=len(fields), column=0, padx=10, pady=5)
                    credit_ids = db_functions.fetch_credit_ids(self.cursor)
                    entry = Combobox(insert_window, values=credit_ids, font=("Comic Sans MS", 12))
                    entry.grid(row=len(fields), column=1, padx=10, pady=5)
                    entry.set("Select CREDITID") 
                    fields.append((col, entry))
                elif col == 'INN' and self.table_name == 'CREDIT':
                    label = tk.Label(insert_window, text=col, bg="#fbf2fc", font=("Comic Sans MS", 12))
                    label.grid(row=len(fields), column=0, padx=10, pady=5)
                    inn = db_functions.fetch_inn(self.cursor)
                    entry = Combobox(insert_window, values=inn, font=("Comic Sans MS", 12))
                    entry.grid(row=len(fields), column=1, padx=10, pady=5)
                    entry.set("Select INN") 
                    fields.append((col, entry))
                else:
                    if col != 'CREDITID':
                        if col in ('LOAN_DATE', 'FINE_DATE', 'CREATEDATE'): 
                            entry = DateEntry(
                            insert_window, 
                            width=12, 
                            background='#FFB3DE',     
                            foreground='black',     
                            borderwidth=2,
                            selectbackground='#ffd1eb'
                            )
                        else:
                            entry = tk.Entry(insert_window, font=("Comic Sans MS", 12))
                        label = tk.Label(insert_window, text=col, bg="#fbf2fc", font=("Comic Sans MS", 12))
                        label.grid(row=len(fields), column=0, padx=10, pady=5)
                        entry.grid(row=len(fields), column=1, padx=10, pady=5)
                        fields.append((col, entry))


        insert_button = tk.Button(insert_window, text="Insert", 
            command=lambda fields=fields, insert_window=insert_window: self.insert_data_to_db(fields, insert_window), 
            bg="#FFB3DE", font=("Comic Sans MS", 14))
        insert_button.grid(row=len(fields), columnspan=2, padx=10, pady=10)

    def insert_data_to_db(self, fields, insert_window):
        new_data = []
        for field in fields:
            col, entry = field
            if col in ('LOAN_DATE', 'FINE_DATE', 'CREATEDATE'): 
                date = entry.get()
                date_object = datetime.strptime(date, "%m/%d/%y")
                formatted_date = date_object.strftime("%Y-%m-%d")
                new_data.append(formatted_date)
            else:
                new_data.append(entry.get())

        db_functions.insert_row(self.cursor, self.table_name, new_data)
        self.connection.commit()
        self.refresh_table() 
        insert_window.destroy() 

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def go_to_start_window(self):
        self.create_start_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = TableApp(root)
    root.mainloop()