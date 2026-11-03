import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import date, datetime

# ================= CONFIGURATION =================

APP_TITLE = "Employee Management System"
DATA_FILE = "employees.json"
ATTENDANCE_FILE = "attendance.json"

BG = "#F4F6FA"
SIDEBAR = "#17243A"
PRIMARY = "#356AE6"
WHITE = "#FFFFFF"
TEXT = "#263449"
MUTED = "#7B8798"

DEPARTMENTS = [
    "IT", "HR", "Finance", "Marketing",
    "Sales", "Operations", "Administration"
]

# ================= DATA STORAGE =================

def load_json(filename, default):
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


employees = load_json(DATA_FILE, [])
attendance = load_json(ATTENDANCE_FILE, {})


# ================= MAIN APPLICATION =================

class EmployeeManagementSystem:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x720")
        self.root.minsize(950, 600)
        self.root.configure(bg=BG)

        self.selected_id = None

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

    # ================= STYLES =================

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=35,
            fieldbackground=WHITE,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#E9EEF8",
            foreground=TEXT,
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCE7FF")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=("Arial", 10)
        )

    # ================= LAYOUT =================

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="EMS",
            font=("Arial", 27, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="Employee Management",
            font=("Arial", 10),
            bg=SIDEBAR,
            fg="#AAB8CF"
        ).pack(pady=(0, 35))

        self.add_nav_button("Dashboard", self.show_dashboard)
        self.add_nav_button("Add Employee", self.show_add_employee)
        self.add_nav_button("Employee List", self.show_employee_list)
        self.add_nav_button("Attendance", self.show_attendance)
        self.add_nav_button("Export CSV", self.export_csv)

        tk.Frame(self.sidebar, bg=SIDEBAR).pack(
            expand=True, fill="both"
        )

        tk.Label(
            self.sidebar,
            text="Python Tkinter Project\nVersion 1.0",
            bg=SIDEBAR,
            fg="#AAB8CF",
            font=("Arial", 9),
            justify="center"
        ).pack(pady=20)

        self.main_area = tk.Frame(self.root, bg=BG)
        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

    def add_nav_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text="   " + text,
            command=command,
            font=("Arial", 11),
            bg=SIDEBAR,
            fg=WHITE,
            activebackground=PRIMARY,
            activeforeground=WHITE,
            relief="flat",
            anchor="w",
            padx=20,
            pady=13,
            cursor="hand2"
        )
        button.pack(fill="x", padx=10, pady=3)

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle):
        header = tk.Frame(self.main_area, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 20))

        tk.Label(
            header,
            text=title,
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=5)

    def create_button(self, parent, text, command, color=PRIMARY):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=9,
            cursor="hand2"
        )

    # ================= DASHBOARD =================

    def show_dashboard(self):
        self.clear_main()
        self.create_header(
            "Dashboard",
            "Welcome to Employee Management System"
        )

        total = len(employees)
        departments = len(set(
            e.get("department", "") for e in employees
        ) - {""})

        today = date.today().strftime("%d-%m-%Y")
        present = sum(
            1 for emp in employees
            if attendance.get(today, {}).get(emp["id"]) == "Present"
        )

        absent = sum(
            1 for emp in employees
            if attendance.get(today, {}).get(emp["id"]) == "Absent"
        )

        stats = [
            ("Total Employees", total, PRIMARY),
            ("Departments", departments, "#16A085"),
            ("Present Today", present, "#27AE60"),
            ("Absent Today", absent, "#E67E22")
        ]

        card_frame = tk.Frame(self.main_area, bg=BG)
        card_frame.pack(fill="x", padx=25)

        for title, value, color in stats:
            card = tk.Frame(
                card_frame,
                bg=WHITE,
                padx=20,
                pady=20,
                highlightbackground="#E4E9F0",
                highlightthickness=1
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=6
            )

            tk.Label(
                card,
                text=title,
                bg=WHITE,
                fg=MUTED,
                font=("Arial", 10)
            ).pack(anchor="w")

            tk.Label(
                card,
                text=str(value),
                bg=WHITE,
                fg=color,
                font=("Arial", 25, "bold")
            ).pack(anchor="w", pady=(10, 0))

        recent_frame = tk.Frame(
            self.main_area,
            bg=WHITE,
            padx=20,
            pady=15
        )
        recent_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        tk.Label(
            recent_frame,
            text="Recent Employees",
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", pady=(0, 15))

        columns = ("ID", "Name", "Department", "Designation", "Salary")

        tree = ttk.Treeview(
            recent_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        tree.pack(fill="both", expand=True)

        for emp in employees[-10:][::-1]:
            tree.insert("", "end", values=(
                emp.get("id", ""),
                emp.get("name", ""),
                emp.get("department", ""),
                emp.get("designation", ""),
                emp.get("salary", 0)
            ))

    # ================= ADD EMPLOYEE =================

    def show_add_employee(self):
        self.selected_id = None
        self.show_employee_form()

    def show_employee_form(self, employee=None):
        self.clear_main()

        editing = employee is not None

        self.create_header(
            "Update Employee" if editing else "Add Employee",
            "Enter employee information below"
        )

        form = tk.Frame(
            self.main_area,
            bg=WHITE,
            padx=30,
            pady=25
        )
        form.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        self.entries = {}

        fields = [
            ("Employee ID", "id"),
            ("Full Name", "name"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("Designation", "designation"),
            ("Salary", "salary"),
            ("Joining Date (DD-MM-YYYY)", "joining_date")
        ]

        for index, (label, key) in enumerate(fields):
            row = index // 2
            col = index % 2

            cell = tk.Frame(form, bg=WHITE)
            cell.grid(
                row=row,
                column=col,
                padx=15,
                pady=12,
                sticky="ew"
            )

            tk.Label(
                cell,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(0, 7))

            entry = tk.Entry(
                cell,
                font=("Arial", 11),
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", ipady=7)

            if employee:
                entry.insert(0, str(employee.get(key, "")))

            if key == "id" and editing:
                entry.config(state="disabled")

            self.entries[key] = entry

        # Gender
        gender_cell = tk.Frame(form, bg=WHITE)
        gender_cell.grid(
            row=4,
            column=0,
            padx=15,
            pady=12,
            sticky="ew"
        )

        tk.Label(
            gender_cell,
            text="Gender",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 7))

        self.gender_var = tk.StringVar(
            value=employee.get("gender", "Male") if employee else "Male"
        )

        gender_box = ttk.Combobox(
            gender_cell,
            textvariable=self.gender_var,
            values=["Male", "Female", "Other"],
            state="readonly"
        )
        gender_box.pack(fill="x", ipady=5)

        # Department
        dept_cell = tk.Frame(form, bg=WHITE)
        dept_cell.grid(
            row=4,
            column=1,
            padx=15,
            pady=12,
            sticky="ew"
        )

        tk.Label(
            dept_cell,
            text="Department",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 7))

        self.department_var = tk.StringVar(
            value=employee.get("department", DEPARTMENTS[0])
            if employee else DEPARTMENTS[0]
        )

        dept_box = ttk.Combobox(
            dept_cell,
            textvariable=self.department_var,
            values=DEPARTMENTS,
            state="readonly"
        )
        dept_box.pack(fill="x", ipady=5)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        button_frame = tk.Frame(form, bg=WHITE)
        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=25
        )

        self.create_button(
            button_frame,
            "Update Employee" if editing else "Save Employee",
            self.save_employee
        ).pack(side="left", padx=8)

        self.create_button(
            button_frame,
            "Clear Form",
            self.clear_form,
            "#7B8798"
        ).pack(side="left", padx=8)

    def clear_form(self):
        for entry in self.entries.values():
            if str(entry.cget("state")) != "disabled":
                entry.delete(0, tk.END)

        self.gender_var.set("Male")
        self.department_var.set(DEPARTMENTS[0])

    def save_employee(self):

        data = {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

        data["gender"] = self.gender_var.get()
        data["department"] = self.department_var.get()

        for key in ["id", "name", "email", "phone",
                    "designation", "salary", "joining_date"]:

            if not data[key]:
                messagebox.showerror(
                    "Validation Error",
                    f"Please enter {key.replace('_', ' ').title()}."
                )
                return

        if not data["salary"].replace(".", "", 1).isdigit():
            messagebox.showerror(
                "Invalid Salary",
                "Please enter a valid salary."
            )
            return

        if not data["id"].isalnum():
            messagebox.showerror(
                "Invalid ID",
                "Employee ID must contain only letters and numbers."
            )
            return

        if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        if not data["phone"].isdigit() or len(data["phone"]) != 10:
            messagebox.showerror(
                "Invalid Phone",
                "Enter a valid 10-digit phone number."
            )
            return

        try:
            datetime.strptime(data["joining_date"], "%d-%m-%Y")
            salary = float(data["salary"])
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid salary and joining date (DD-MM-YYYY)."
            )
            return

        data["salary"] = salary

        existing = next(
            (e for e in employees if e["id"] == data["id"]),
            None
        )

        if self.selected_id is None:
            if existing:
                messagebox.showerror(
                    "Duplicate ID",
                    "This Employee ID already exists."
                )
                return

            employees.append(data)
            messagebox.showinfo(
                "Success",
                "Employee added successfully!"
            )

        else:
            if existing and existing["id"] != self.selected_id:
                messagebox.showerror(
                    "Duplicate ID",
                    "Employee ID already exists."
                )
                return

            for index, emp in enumerate(employees):
                if emp["id"] == self.selected_id:
                    employees[index] = data
                    break

            messagebox.showinfo(
                "Success",
                "Employee updated successfully!"
            )

        save_json(DATA_FILE, employees)
        self.selected_id = None
        self.show_employee_list()

    # ================= EMPLOYEE LIST =================

    def show_employee_list(self):
        self.clear_main()

        self.create_header(
            "Employee List",
            "Manage all registered employees"
        )

        top = tk.Frame(self.main_area, bg=BG)
        top.pack(fill="x", padx=30, pady=(0, 15))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            top,
            textvariable=self.search_var,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )
        search_entry.insert(0, "")

        self.create_button(
            top,
            "Search",
            self.search_employee
        ).pack(side="left", padx=8)

        self.create_button(
            top,
            "Reset",
            self.show_employee_list,
            "#7B8798"
        ).pack(side="left")

        actions = tk.Frame(self.main_area, bg=BG)
        actions.pack(side="bottom", fill="x", padx=30, pady=(10, 20))

        self.create_button(
            actions, "Edit Selected", self.edit_employee
        ).pack(side="left", padx=5)

        self.create_button(
            actions, "Delete Selected", self.delete_employee, "#D9534F"
        ).pack(side="left", padx=5)

        self.create_button(
            actions, "View Details", self.view_employee
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.main_area, bg=WHITE)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 10)
        )

        columns = (
            "ID", "Name", "Department",
            "Designation", "Phone", "Salary"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.populate_table()

    def populate_table(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = employees if records is None else records

        for emp in records:
            self.tree.insert("", "end", values=(
                emp.get("id", ""),
                emp.get("name", ""),
                emp.get("department", ""),
                emp.get("designation", ""),
                emp.get("phone", ""),
                emp.get("salary", 0)
            ))

    def search_employee(self):
        query = self.search_var.get().strip().lower()

        if not query:
            self.populate_table()
            return

        results = [
            emp for emp in employees
            if query in emp.get("id", "").lower()
            or query in emp.get("name", "").lower()
        ]

        self.populate_table(results)

        if not results:
            messagebox.showinfo(
                "Search",
                "No matching employees found."
            )

    def get_selected_employee(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select an employee first."
            )
            return None

        employee_id = self.tree.item(selected[0])["values"][0]

        return next(
            (e for e in employees if e["id"] == employee_id),
            None
        )

    def edit_employee(self):
        emp = self.get_selected_employee()

        if emp:
            self.selected_id = emp["id"]
            self.show_employee_form(emp)

    def delete_employee(self):
        emp = self.get_selected_employee()

        if not emp:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {emp['name']}?"
        )

        if confirm:
            employees.remove(emp)

            for day in attendance:
                attendance[day].pop(emp["id"], None)

            save_json(DATA_FILE, employees)
            save_json(ATTENDANCE_FILE, attendance)

            messagebox.showinfo(
                "Deleted",
                "Employee deleted successfully."
            )

            self.show_employee_list()

    def view_employee(self):
        emp = self.get_selected_employee()

        if not emp:
            return

        details = "\n".join(
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in emp.items()
        )

        messagebox.showinfo(
            "Employee Details",
            details
        )

    # ================= ATTENDANCE =================

    def show_attendance(self):
        self.clear_main()

        self.create_header(
            "Attendance Management",
            "Mark employee attendance for today"
        )

        today = date.today().strftime("%d-%m-%Y")

        frame = tk.Frame(self.main_area, bg=WHITE, padx=20, pady=20)
        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        tk.Label(
            frame,
            text=f"Attendance Date: {today}",
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 15))

        table_container = tk.Frame(frame, bg=WHITE)

        columns = ("ID", "Name", "Department", "Status")
        tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def mark_attendance(status):
            selected = tree.selection()

            if not selected:
                messagebox.showwarning(
                    "Selection Required",
                    "Select an employee first."
                )
                return

            employee_id = tree.item(selected[0])["values"][0]

            attendance.setdefault(today, {})
            attendance[today][employee_id] = status

            save_json(ATTENDANCE_FILE, attendance)

            values = list(tree.item(selected[0])["values"])
            values[3] = status
            tree.item(selected[0], values=values)

            messagebox.showinfo(
                "Attendance",
                f"Attendance marked as {status}."
            )

        buttons = tk.Frame(frame, bg=WHITE)
        buttons.pack(side="bottom", pady=(15, 0))

        self.create_button(
            buttons,
            "Mark Present",
            lambda: mark_attendance("Present"),
            "#27AE60"
        ).pack(side="left", padx=8)

        self.create_button(
            buttons,
            "Mark Absent",
            lambda: mark_attendance("Absent"),
            "#D9534F"
        ).pack(side="left", padx=8)

        table_container.pack(fill="both", expand=True)

        for emp in employees:
            status = attendance.get(today, attendance.get(date.today().isoformat(), {})).get(
                emp["id"], "Not Marked"
            )

            tree.insert("", "end", values=(
                emp["id"],
                emp["name"],
                emp["department"],
                status
            ))

    # ================= EXPORT CSV =================

    def export_csv(self):
        if not employees:
            messagebox.showwarning(
                "No Data",
                "There are no employee records to export."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="employee_records.csv"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "id", "name", "email", "phone",
                        "gender", "department", "designation",
                        "salary", "joining_date"
                    ]
                )

                writer.writeheader()
                writer.writerows(employees)

            messagebox.showinfo(
                "Export Successful",
                "Employee records exported successfully!"
            )

        except OSError as error:
            messagebox.showerror(
                "Export Error",
                str(error)
            )


# ================= RUN APPLICATION =================

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
