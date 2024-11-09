import mysql.connector
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import pandas as pd

# Establish MySQL connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jaya@2003",
        database="StudentsManagement"
    )
    mycursor = mydb.cursor()
    print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    messagebox.showerror("Error", f"Error connecting to database: {err}")
    exit()

# Function to clear all entry fields
def clear_entry_fields():
    entry_name.delete(0, END)
    entry_roll.delete(0, END)
    entry_semester.delete(0, END)
    entry_branch.delete(0, END)
    entry_contact.delete(0, END)
    entry_address.delete(0, END)
    entry_gender.delete(0, END)
    entry_dateofbirth.delete(0, END)
    entry_search.delete(0, END)

# Function to add a student
def add_student():
    try:
        name = entry_name.get()
        roll_number = entry_roll.get()
        semester = entry_semester.get()
        branch = entry_branch.get()
        contact = entry_contact.get()
        address = entry_address.get()
        gender = entry_gender.get()
        dateofbirth = entry_dateofbirth.get()

        # Check for empty fields
        if not (name and roll_number and semester and branch and contact and address and gender and dateofbirth):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Convert dob to the correct format
        try:
            dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format. Use YYYY-MM-DD.")
            return

        # Check for duplicate roll number
        mycursor.execute("SELECT * FROM student WHERE roll_number = %s", (roll_number,))
        if mycursor.fetchone() is not None:
            messagebox.showerror("Error", "Roll number already exists.")
            return

        # Insert into the database
        sql = "INSERT INTO student (name, roll_number, semester, branch, contact, address, gender, dateofbirth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, roll_number, semester, branch, contact, address, gender, dateofbirth)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Student added successfully.")
        display_students()  # Refresh the list of students
        clear_entry_fields()  # Clear entry fields after adding
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error adding student: {err}")

# Function to display all students
def display_students():
    try:
        # Clear previous entries
        for item in listbox.get_children():
            listbox.delete(item)
        # Fetch all students
        mycursor.execute("SELECT name, roll_number, semester, branch, contact, address, gender, dateofbirth FROM student")
        students = mycursor.fetchall()
        for student in students:
            listbox.insert("", "end", values=student)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error displaying students: {err}")

# Function to update a student's record
def update_student():
    try:
        selected_item = listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update.")
            return

        name = entry_name.get()
        roll_number = entry_roll.get()
        semester = entry_semester.get()
        branch = entry_branch.get()
        contact = entry_contact.get()
        address = entry_address.get()
        gender = entry_gender.get()
        dateofbirth = entry_dateofbirth.get()

        current_data = listbox.item(selected_item)['values']
        current_roll = current_data[1]  # Assuming roll_number is the second column

        # Check for empty fields
        if not (name and roll_number and semester and branch and contact and address and gender and dateofbirth):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Convert dob to the correct format
        try:
            dateofbirth = datetime.strptime(dateofbirth, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format. Use YYYY-MM-DD.")
            return

        # Update database
        sql = "UPDATE student SET name = %s, roll_number = %s, semester = %s, branch = %s, contact = %s, address = %s, gender = %s, dateofbirth = %s WHERE roll_number = %s"
        val = (name, roll_number, semester, branch, contact, address, gender, dateofbirth, current_roll)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Student updated successfully.")
        display_students()  # Refresh the list of students
        clear_entry_fields()  # Clear entry fields after updating
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error updating student: {err}")

# Function to clear all records
def clear_all():
    try:
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all records?")
        if confirm:
            mycursor.execute("DELETE FROM student")
            mydb.commit()
            messagebox.showinfo("Success", "All records cleared.")
            display_students()  # Refresh the list of students
            clear_entry_fields()  # Clear entry fields after clearing all records
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error clearing records: {err}")

# Function to delete a specific student
def delete_student():
    try:
        selected_item = listbox.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete.")
            return

        roll_number = listbox.item(selected_item)['values'][1]  # Assuming roll_number is the second column

        # Delete from database
        sql = "DELETE FROM student WHERE roll_number = %s"
        val = (roll_number,)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Student deleted successfully.")
        display_students()  # Refresh the list of students
        clear_entry_fields()  # Clear entry fields after deletion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error deleting student: {err}")

# Function to search for a student
def search_student(): 
    try:
        search_term = entry_search.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term.")
            return

        # Search in the database
        sql = "SELECT name, roll_number, semester, branch, contact, address, gender, dateofbirth FROM student WHERE name LIKE %s OR roll_number LIKE %s"
        val = ('%' + search_term + '%', '%' + search_term + '%')
        mycursor.execute(sql, val)
        students = mycursor.fetchall()

        print(students)  # Debugging line to see the retrieved data in the console

        listbox.delete(*listbox.get_children())  # Clear previous results
        for student in students:
            listbox.insert("", "end", values=student)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", f"Error searching student: {err}")


        
# Function for exporting data to excel
def export_to_excel():
    try:
        mycursor.execute("SELECT name, roll_number, semester, branch, contact, address, gender, dateofbirth FROM student")
        students = mycursor.fetchall()

        # Create a DataFrame from the fetched data
        df = pd.DataFrame(students, columns=["Name", "Roll Number", "Semester", "Branch", "Contact", "Address", "Gender", "DateOfBirth"])

        # Save the DataFrame to an Excel file
        filename = "students_data.xlsx"
        df.to_excel(filename, index=False)

        messagebox.showinfo("Success", f"Data exported to {filename} successfully.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Error exporting data: {e}")        

# Function to display all student details
def display_all_details():
    display_students()

# Create the main window
win = tk.Tk()
win.geometry("1200x700+0+0")
win.title("Students Data Management System")

# Title label
title_label = tk.Label(win, text="Students Data Management System", font=("Arial", 30, "bold"), bd=12, relief=tk.GROOVE, bg="lightgrey")
title_label.pack(fill=tk.X)

# Detail frame for input fields
detail_frame = tk.LabelFrame(win, text="Enter Details", font=("Arial", 20), bd=12, relief=tk.GROOVE, bg="lightgrey")
detail_frame.place(x=20, y=120, width=420, height=520)

# Data frame for displaying students
data_frame = tk.Frame(win, bd=12, bg="lightgrey", relief=tk.GROOVE)
data_frame.place(x=445, y=120, width=820, height=520)

# Labels for input fields
labels = ["Name", "Roll Number", "Semester", "Branch", "Contact", "Address", "Gender", "DateOfBirth"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(detail_frame, text=label, bg="lightgrey", font=("Arial", 17)).grid(row=i, column=0, padx=2, pady=2)
    entries[label.lower()] = tk.Entry(detail_frame, bd=7)
    entries[label.lower()].grid(row=i, column=1, padx=2, pady=2)

entry_name = entries["name"]
entry_roll = entries["roll number"]
entry_semester = entries["semester"]
entry_branch = entries["branch"]
entry_contact = entries["contact"]
entry_address = entries["address"]
entry_gender = entries["gender"]
entry_dateofbirth = entries["dateofbirth"]

# Buttons for various operations
btn_frame = tk.Frame(detail_frame, bd=7, relief=tk.GROOVE)
btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

buttons = [
    ("Add Student", add_student),
    ("Update Student", update_student),
    ("Delete Student", delete_student),
    ("Clear All Records", clear_all),
    ("Export to Excel", export_to_excel),
    ("Display All",display_all_details) 
]



for i, (text, command) in enumerate(buttons):
    tk.Button(detail_frame, text=text, command=command, font=("Arial", 15, "bold"),
              bd=5, relief=tk.GROOVE).grid(row=8 + i // 2, column=i % 2, padx=5, pady=5)



# Search section
label_search = tk.Label(win, text="Search", font=("Arial", 17))
label_search.place(x=475, y=75)
entry_search = tk.Entry(win, bd=7, width=30)
entry_search.place(x=570, y=75)
btn_search = tk.Button(win, text="Search", command=search_student, font=("Arial", 14, "bold"),
                       bd=5, relief=tk.GROOVE)
btn_search.place(x=900, y=70)

# Listbox to display students
columns = ("name", "roll_number", "semester", "branch", "contact", "address", "gender", "dateofbirth")
listbox = ttk.Treeview(data_frame, columns=columns, show='headings')

for col in columns:
    listbox.heading(col, text=col.capitalize())
    listbox.column(col, width=100, anchor=tk.CENTER)

listbox.pack(fill=tk.BOTH, expand=1)

# Function to show selected student details
def show_selected_student_details():
    selected_item = listbox.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a student.")
        return
    student_details = listbox.item(selected_item)['values']
    messagebox.showinfo("Student Details", 
                        f"Name: {student_details[0]}\n"
                        f"Roll Number: {student_details[1]}\n"
                        f"Semester: {student_details[2]}\n"
                        f"Branch: {student_details[3]}\n"
                        f"Contact: {student_details[4]}\n"
                        f"Address: {student_details[5]}\n"
                        f"Gender: {student_details[6]}\n"
                        f"DateOfBirth: {student_details[7]}")

# Button to show selected student details
btn_show_details = tk.Button(data_frame, text="Show Details", command=show_selected_student_details,
                             font=("Arial", 15, "bold"), bd=7)
btn_show_details.pack(pady=10)

# Run the main loop
win.mainloop()









