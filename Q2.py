# Employee Registration Form using Tkinter

import tkinter as tk

def submit_data():
    """Function to display entered employee details in console"""
    print("---- Employee Details ----")
    print(f"Name: {name_var.get()}")
    print(f"Employee ID: {eid_var.get()}")
    print(f"Department: {dept_var.get()}")
    print(f"Designation: {design_var.get()}")
    print("---------------------------\n")
    
    # Optional: show success message in GUI
    tk.Label(root, text="Data Submitted Successfully!", fg="green").pack()

# Create main window
root = tk.Tk()
root.title("Employee Registration Form")
root.geometry("400x300")

# String variables for each input field
name_var = tk.StringVar()
eid_var = tk.StringVar()
dept_var = tk.StringVar()
design_var = tk.StringVar()

# Heading
tk.Label(root, text="Employee Registration Form", font=('Arial', 14, 'bold')).pack(pady=10)

# Input fields
tk.Label(root, text="Name:").pack()
tk.Entry(root, textvariable=name_var).pack(pady=3)

tk.Label(root, text="Employee ID:").pack()
tk.Entry(root, textvariable=eid_var).pack(pady=3)

tk.Label(root, text="Department:").pack()
tk.Entry(root, textvariable=dept_var).pack(pady=3)

tk.Label(root, text="Designation:").pack()
tk.Entry(root, textvariable=design_var).pack(pady=3)

# Submit button
tk.Button(root, text="Submit", command=submit_data, bg="lightblue", font=('Arial', 10, 'bold')).pack(pady=10)

# Exit button (optional)
tk.Button(root, text="Exit", command=root.quit, bg="lightcoral").pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
