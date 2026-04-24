import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector

# ================= DATABASE ================= #

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="D$ai1919",
    database="todo_app"
)
cursor = db.cursor()

current_user_id = None
selected_task_id = None
selected_date = ""
selected_task_description = ""

# ================= UI CONSTANTS ================= #

BG_MAIN = "#1e1e2f"
BG_CARD = "#252836"
ACCENT = "#6a5acd"
GREEN = "#4caf50"
RED = "#f44336"
GRAY = "#555555"
TEXT_LIGHT = "#ffffff"
TEXT_MUTED = "#aaaaaa"

FONT_TITLE = ("Segoe UI Semibold", 26)
FONT_SUB = ("Segoe UI", 13)
FONT_TEXT = ("Segoe UI", 14)
FONT_BTN = ("Segoe UI Semibold", 13)

# ================= AUTH FUNCTIONS ================= #

def login():
    global current_user_id
    user = username_entry.get().strip()
    pwd = password_entry.get().strip()

    cursor.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (user, pwd)
    )
    result = cursor.fetchone()

    if result:
        current_user_id = result[0]
        login_window.destroy()
        load_tasks()
        root.deiconify()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def register():
    user = username_entry.get().strip()
    pwd = password_entry.get().strip()

    if not user or not pwd:
        messagebox.showwarning("Error", "All fields required")
        return

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s,%s)",
            (user, pwd)
        )
        db.commit()
        messagebox.showinfo("Success", "Account created successfully")
    except:
        messagebox.showerror("Error", "Username already exists")

# ================= TASK FUNCTIONS ================= #

def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute(
        "SELECT id, task, task_date, description, is_important FROM tasks WHERE user_id=%s ORDER BY is_important DESC, id DESC",
        (current_user_id,)
    )

    for i, (tid, task, date, desc, is_important) in enumerate(cursor.fetchall(), start=1):
        star = "⭐ " if is_important else ""
        listbox.insert(tk.END, f"{star}{i}. {task}   |   📅 {date}")

def add_task():
    global selected_date

    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Error", "Task cannot be empty")
        return
    if not selected_date:
        messagebox.showwarning("Error", "Select a date")
        return

    cursor.execute(
        "INSERT INTO tasks (user_id, task, task_date) VALUES (%s,%s,%s)",
        (current_user_id, task, selected_date)
    )
    db.commit()

    clear_inputs()
    load_tasks()

def select_task(event):
    global selected_task_id, selected_date, selected_task_description

    try:
        index = listbox.curselection()[0]
        cursor.execute(
            "SELECT id, task, task_date, description FROM tasks WHERE user_id=%s ORDER BY is_important DESC, id DESC",
            (current_user_id,)
        )
        tasks = cursor.fetchall()

        selected_task_id, task_text, task_date, description = tasks[index]
        selected_task_description = description if description else ""

        task_entry.delete(0, tk.END)
        task_entry.insert(0, task_text)

        selected_date = task_date
        date_label.config(text=f"📅 {selected_date}", fg=GREEN)
        
        # Show task details popup
        show_task_details()
    except:
        pass

def edit_task():
    if selected_task_id is None:
        messagebox.showwarning("Error", "Select a task to edit")
        return

    new_task = task_entry.get().strip()
    if not new_task:
        messagebox.showwarning("Error", "Task cannot be empty")
        return
    if not selected_date:
        messagebox.showwarning("Error", "Select a date")
        return

    cursor.execute(
        "UPDATE tasks SET task=%s, task_date=%s WHERE id=%s",
        (new_task, selected_date, selected_task_id)
    )
    db.commit()

    clear_inputs()
    load_tasks()

def delete_task():
    global selected_task_id

    if selected_task_id is None:
        messagebox.showwarning("Error", "Select a task to delete")
        return

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (selected_task_id,)
    )
    db.commit()

    clear_inputs()
    load_tasks()

def deselect_task():
    clear_inputs()

# ================= TASK DETAILS POPUP ================= #

def show_task_details():
    global selected_task_description
    
    if selected_task_id is None:
        return
    
    details_win = tk.Toplevel(root)
    details_win.title("Task Details")
    details_win.geometry("500x400")
    details_win.configure(bg=BG_MAIN)
    details_win.resizable(False, False)
    
    card = tk.Frame(details_win, bg=BG_CARD)
    card.pack(expand=True, fill="both", padx=20, pady=20)
    
    tk.Label(card, text="📝 Task Details",
             font=FONT_TITLE, bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=10)
    
    tk.Label(card, text="Task Name:",
             font=FONT_SUB, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", padx=10, pady=(10, 0))
    
    task_display = tk.Label(card, text=task_entry.get(),
                           font=FONT_TEXT, bg=BG_MAIN, fg=TEXT_LIGHT,
                           wraplength=450, justify="left")
    task_display.pack(fill="x", padx=10, pady=5)
    
    tk.Label(card, text="Description:",
             font=FONT_SUB, bg=BG_CARD, fg=TEXT_LIGHT).pack(anchor="w", padx=10, pady=(10, 0))
    
    desc_text = tk.Text(card, font=FONT_TEXT, width=60, height=8,
                        bg=BG_MAIN, fg=TEXT_LIGHT,
                        insertbackground="white", relief="flat")
    desc_text.pack(fill="both", padx=10, pady=5, expand=True)
    desc_text.insert("1.0", selected_task_description)
    
    def save_details():
        global selected_task_description
        selected_task_description = desc_text.get("1.0", tk.END).strip()
        cursor.execute(
            "UPDATE tasks SET description=%s WHERE id=%s",
            (selected_task_description, selected_task_id)
        )
        db.commit()
        messagebox.showinfo("Success", "Task details saved")
        details_win.destroy()
    
    button_frame = tk.Frame(card, bg=BG_CARD)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="💾 Save",
              bg=GREEN, fg="white",
              font=FONT_BTN, relief="flat",
              command=save_details).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ Close",
              bg=GRAY, fg="white",
              font=FONT_BTN, relief="flat",
              command=details_win.destroy).pack(side="left", padx=5)

def toggle_important():
    if selected_task_id is None:
        messagebox.showwarning("Error", "Select a task first")
        return
    
    cursor.execute(
        "SELECT is_important FROM tasks WHERE id=%s",
        (selected_task_id,)
    )
    result = cursor.fetchone()
    is_important = result[0] if result else 0
    
    new_status = 1 if is_important == 0 else 0
    cursor.execute(
        "UPDATE tasks SET is_important=%s WHERE id=%s",
        (new_status, selected_task_id)
    )
    db.commit()
    
    messagebox.showinfo("Success", "Task marked as " + ("important" if new_status else "normal"))
    load_tasks()


def clear_inputs():
    global selected_task_id, selected_date, selected_task_description
    selected_task_id = None
    selected_date = ""
    selected_task_description = ""
    listbox.selection_clear(0, tk.END)
    task_entry.delete(0, tk.END)
    date_label.config(text="No date selected", fg=TEXT_MUTED)

# ================= CALENDAR ================= #

def open_calendar():
    cal_win = tk.Toplevel(root)
    cal_win.title("Select Date")
    cal_win.geometry("320x340")
    cal_win.configure(bg=BG_CARD)

    cal = Calendar(
        cal_win,
        selectmode="day",
        date_pattern="dd-mm-yyyy",
        background=BG_CARD,
        foreground=TEXT_LIGHT,
        headersbackground=ACCENT,
        headersforeground=TEXT_LIGHT,
        selectbackground=GREEN
    )
    cal.pack(pady=15)

    def pick_date():
        global selected_date
        selected_date = cal.get_date()
        date_label.config(text=f"📅 {selected_date}", fg=GREEN)
        cal_win.destroy()

    tk.Button(
        cal_win, text="✔ Select Date",
        bg=GREEN, fg="white",
        font=FONT_BTN,
        relief="flat",
        command=pick_date
    ).pack(pady=10)

# ================= LOGIN UI ================= #

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("450x450")
login_window.configure(bg=BG_MAIN)

login_card = tk.Frame(login_window, bg=BG_CARD)
login_card.pack(expand=True)

tk.Label(login_card, text="📝 Smart To-Do App",
         font=FONT_TITLE, bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=15)

tk.Label(login_card, text="Login or Register",
         font=FONT_SUB, bg=BG_CARD, fg=TEXT_MUTED).pack(pady=5)

def styled_entry(parent, show=None):
    e = tk.Entry(parent, font=FONT_TEXT, width=28,
                 bg=BG_MAIN, fg=TEXT_LIGHT,
                 insertbackground="white",
                 relief="flat", show=show)
    e.pack(pady=10)
    return e

username_entry = styled_entry(login_card)
password_entry = styled_entry(login_card, show="*")

tk.Button(login_card, text="🔐 Login",
          bg=GREEN, fg="white",
          font=FONT_BTN, width=20,
          relief="flat", command=login).pack(pady=10)

tk.Button(login_card, text="🆕 Register",
          bg=ACCENT, fg="white",
          font=FONT_BTN, width=20,
          relief="flat", command=register).pack()

# ================= MAIN APP ================= #

root = tk.Tk()
root.title("Smart To-Do List")
root.geometry("1200x800")
root.state('zoomed')  # Maximize window
root.resizable(True, True)
root.configure(bg=BG_MAIN)
root.withdraw()

card = tk.Frame(root, bg=BG_CARD)
card.pack(pady=30)

tk.Label(card, text="📝 My Tasks",
         font=FONT_TITLE, bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=15)

task_entry = tk.Entry(card, font=FONT_TEXT, width=55,
                      bg=BG_MAIN, fg=TEXT_LIGHT,
                      insertbackground="white", relief="flat")
task_entry.pack(pady=10)

date_frame = tk.Frame(card, bg=BG_CARD)
date_frame.pack(pady=8)

tk.Button(date_frame, text="📅 Choose Date",
          bg=ACCENT, fg="white",
          font=FONT_BTN, relief="flat",
          command=open_calendar).pack(side="left", padx=10)

date_label = tk.Label(date_frame, text="No date selected",
                      bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SUB)
date_label.pack(side="left")

btn_frame = tk.Frame(card, bg=BG_CARD)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="➕ Add",
          bg=GREEN, fg="white",
          width=14, font=FONT_BTN,
          relief="flat", command=add_task).grid(row=0, column=0, padx=6)

tk.Button(btn_frame, text="✏ Edit",
          bg=ACCENT, fg="white",
          width=14, font=FONT_BTN,
          relief="flat", command=edit_task).grid(row=0, column=1, padx=6)

tk.Button(btn_frame, text="⭐ Important",
          bg="#FFD700", fg="black",
          width=14, font=FONT_BTN,
          relief="flat", command=toggle_important).grid(row=0, column=2, padx=6)

tk.Button(btn_frame, text="🗑 Delete",
          bg=RED, fg="white",
          width=14, font=FONT_BTN,
          relief="flat", command=delete_task).grid(row=0, column=3, padx=6)

tk.Button(btn_frame, text="❌ Deselect",
          bg=GRAY, fg="white",
          width=14, font=FONT_BTN,
          relief="flat", command=deselect_task).grid(row=0, column=4, padx=6)

list_frame = tk.Frame(card, bg=BG_CARD)
list_frame.pack(pady=20, fill="both", expand=True, padx=20)

scroll = tk.Scrollbar(list_frame)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(
    list_frame, width=100, height=18,
    bg=BG_MAIN, fg=TEXT_LIGHT,
    font=FONT_TEXT,
    selectbackground=ACCENT,
    relief="flat",
    yscrollcommand=scroll.set
)
listbox.pack(fill="both", expand=True)
scroll.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", select_task)

login_window.mainloop()
root.mainloop()
