import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib

# Helper function to center window on screen
def center_window(window, width, height):
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set window geometry and position
    window.geometry(f"{width}x{height}+{x}+{y}")

# Database connection class for MySQL operations
class DatabaseManager:
    def __init__(self):
        # MySQL connection credentials
        self.host = "localhost"
        self.user = "root"
        self.password = "D$ai1919"
        self.database = "idea_manager"
        self.connection = None
        
        # Initialize database
        self.init_database()

    # Create connection to MySQL server
    def get_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            return self.connection
        except Error as err:
            messagebox.showerror("Database Error", f"Connection failed: {err}")
            return None

    # Initialize database and create tables if not exist
    def init_database(self):
        try:
            # Connect to MySQL without selecting database first
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            conn.close()
            
            # Now connect to the database and create tables
            self.connection = self.get_connection()
            if self.connection:
                cursor = self.connection.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create ideas table with foreign key to users
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ideas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        idea_text LONGTEXT NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)
                
                self.connection.commit()
                cursor.close()
        except Error as err:
            messagebox.showerror("Database Error", f"Initialization failed: {err}")

    # Execute query with parameters
    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                cursor.close()
                return True
            except Error as err:
                messagebox.showerror("Database Error", f"Query failed: {err}")
                return False
        return False

    # Fetch single row from database
    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                return result
            except Error as err:
                messagebox.showerror("Database Error", f"Fetch failed: {err}")
        return None

    # Fetch all rows from database
    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                return results
            except Error as err:
                messagebox.showerror("Database Error", f"Fetch failed: {err}")
        return []

    # Close database connection
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Login Window Class - Handles user authentication and registration
class LoginWindow:
    def __init__(self, root):
        # Initialize login window with styling
        self.root = root
        self.root.title("💡 Idea Manager - Login")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        # Center window on screen
        center_window(self.root, 500, 600)
        self.current_user = None
        
        # Define color scheme matching main app
        self.bg_color = "#0f0f1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#00ffff"
        self.accent_secondary = "#ff00ff"
        self.btn_color = "#00ccff"
        self.card_bg = "#1a1a2e"
        self.root.configure(bg=self.bg_color)
        
        # Initialize database manager
        self.db = DatabaseManager()
        
        # Show login UI
        self.create_login_ui()

    # Hash password for secure storage
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Create login UI with premium styling
    def create_login_ui(self):
        # Header section
        header_frame = tk.Frame(self.root, bg="#0a0a14", height=100)
        header_frame.pack(fill=tk.X)
        
        inner_header = tk.Frame(header_frame, bg=self.card_bg, height=95)
        inner_header.pack(fill=tk.X, padx=0, pady=3)
        
        # Title
        title_label = tk.Label(
            inner_header,
            text="✨ IDEA MANAGER ✨",
            font=("Segoe UI", 24, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        title_label.pack(pady=15)
        
        subtitle = tk.Label(
            inner_header,
            text="Secure Login Portal",
            font=("Segoe UI", 10, "italic"),
            bg=self.card_bg,
            fg=self.accent_secondary
        )
        subtitle.pack(pady=(0, 10))

        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Login form frame
        form_frame = tk.Frame(main_frame, bg=self.card_bg, relief=tk.FLAT, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Username label and input
        username_label = tk.Label(
            form_frame,
            text="👤 Username",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        username_label.pack(anchor=tk.W, padx=20, pady=(20, 8))

        self.username_input = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#0f0f1e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=2
        )
        self.username_input.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.username_input.bind("<Return>", lambda e: self.login())

        # Password label and input
        password_label = tk.Label(
            form_frame,
            text="🔒 Password",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        password_label.pack(anchor=tk.W, padx=20, pady=(0, 8))

        self.password_input = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            bg="#0f0f1e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            show="•",
            relief=tk.FLAT,
            bd=2
        )
        self.password_input.pack(fill=tk.X, padx=20, pady=(0, 25))
        self.password_input.bind("<Return>", lambda e: self.login())

        # Button section
        button_frame = tk.Frame(form_frame, bg=self.card_bg)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Login button
        login_btn = tk.Button(
            button_frame,
            text="🚀 LOGIN",
            command=self.login,
            bg=self.btn_color,
            fg=self.bg_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground=self.accent_color
        )
        login_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        # Register button
        register_btn = tk.Button(
            button_frame,
            text="📝 REGISTER",
            command=self.show_register,
            bg=self.accent_secondary,
            fg=self.fg_color,
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#ff33ff"
        )
        register_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Login function with validation
    def login(self):
        # Get input values
        username = self.username_input.get().strip()
        password = self.password_input.get().strip()

        # Validate input
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter username and password!")
            return

        # Query database for user
        user = self.db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        
        if user:
            hashed_password = self.hash_password(password)
            if user['password'] == hashed_password:
                self.current_user = username
                messagebox.showinfo("Success", f"Welcome back, {username}! 🎉")
                self.root.destroy()
                # Launch main app
                launch_main_app(username, self.db)
            else:
                messagebox.showerror("Login Error", "Invalid password!")
        else:
            messagebox.showerror("Login Error", "Username not found!")

    # Show registration form
    def show_register(self):
        # Clear login form
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        
        # Create new register window
        register_win = tk.Toplevel(self.root)
        register_win.title("Register New Account")
        register_win.geometry("400x350")
        register_win.configure(bg=self.bg_color)
        
        # Header
        header = tk.Label(
            register_win,
            text="Create Account",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        header.pack(pady=20)

        # Frame for inputs
        input_frame = tk.Frame(register_win, bg=self.bg_color)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        # Username input
        tk.Label(
            input_frame,
            text="New Username:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(anchor=tk.W, pady=(0, 5))

        new_username = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=2
        )
        new_username.pack(fill=tk.X, pady=(0, 15))

        # Password input
        tk.Label(
            input_frame,
            text="New Password:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(anchor=tk.W, pady=(0, 5))

        new_password = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            show="•",
            relief=tk.FLAT,
            bd=2
        )
        new_password.pack(fill=tk.X, pady=(0, 15))

        # Confirm password input
        tk.Label(
            input_frame,
            text="Confirm Password:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(anchor=tk.W, pady=(0, 5))

        confirm_password = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            show="•",
            relief=tk.FLAT,
            bd=2
        )
        confirm_password.pack(fill=tk.X, pady=(0, 20))

        # Register button
        def register_account():
            username = new_username.get().strip()
            password = new_password.get().strip()
            confirm = confirm_password.get().strip()

            # Validate
            if not username or not password:
                messagebox.showerror("Error", "Please fill all fields!")
                return

            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            # Check if username exists in database
            existing_user = self.db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
            if existing_user:
                messagebox.showerror("Error", "Username already exists!")
                return

            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return

            # Create account in database
            hashed_pass = self.hash_password(password)
            if self.db.execute_query(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_pass)
            ):
                messagebox.showinfo("Success", f"Account '{username}' created! Now login.")
                register_win.destroy()
            else:
                messagebox.showerror("Error", "Failed to create account!")

        reg_btn = tk.Button(
            input_frame,
            text="✅ CREATE ACCOUNT",
            command=register_account,
            bg=self.accent_secondary,
            fg=self.fg_color,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2"
        )
        reg_btn.pack(fill=tk.X, pady=10)

# Main Application Class - Handles the entire app structure and functionality

class IdeaManager:
    def __init__(self, root, current_user, db):
        # Initialize the main window with styling
        self.root = root
        self.current_user = current_user
        self.db = db
        self.root.title(f"💡 Idea Manager - {current_user}'s Vault")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        # Center window on screen
        center_window(self.root, 1000, 750)
        
        # Define premium color scheme with modern gradient vibes
        self.bg_color = "#0f0f1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#00ffff"
        self.accent_secondary = "#ff00ff"
        self.btn_color = "#00ccff"
        self.hover_color = "#00ffff"
        self.card_bg = "#1a1a2e"
        self.card_border = "#00ffff"
        self.root.configure(bg=self.bg_color)
        
        # File path for storing ideas as JSON using username
        self.ideas_file = f"ideas_{current_user}.json"
        # Load existing ideas from file
        self.ideas = self.load_ideas()
        
        # Create the UI layout
        self.create_ui()

    # Load ideas from MySQL database for current user
    def load_ideas(self):
        # Get user ID from database
        user = self.db.fetch_one("SELECT id FROM users WHERE username = %s", (self.current_user,))
        if user:
            user_id = user['id']
            # Fetch all ideas for this user ordered by date
            ideas = self.db.fetch_all(
                "SELECT * FROM ideas WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            # Convert to list of dictionaries with required fields
            result = []
            for idea in ideas:
                result.append({
                    'id': idea['id'],
                    'text': idea['idea_text'],
                    'category': idea['category'],
                    'date': idea['created_at'].strftime("%Y-%m-%d %H:%M")
                })
            return result
        return []

    # Save idea to MySQL database
    def save_idea(self, idea_text, category):
        # Get user ID
        user = self.db.fetch_one("SELECT id FROM users WHERE username = %s", (self.current_user,))
        if user:
            user_id = user['id']
            # Insert idea into database
            return self.db.execute_query(
                "INSERT INTO ideas (user_id, idea_text, category) VALUES (%s, %s, %s)",
                (user_id, idea_text, category)
            )
        return False

    # Delete idea from database by ID
    def delete_idea_from_db(self, idea_id):
        return self.db.execute_query(
            "DELETE FROM ideas WHERE id = %s",
            (idea_id,)
        )

    # Create the entire user interface with header, input section, and ideas list
    def create_ui(self):
        # Premium header section with gradient effect simulation
        header_frame = tk.Frame(self.root, bg="#0a0a14", height=80)
        header_frame.pack(fill=tk.X)
        
        # Inner header with accent color border
        inner_header = tk.Frame(header_frame, bg=self.card_bg, height=75)
        inner_header.pack(fill=tk.X, padx=0, pady=3)
        
        # Title label with premium styling
        title_label = tk.Label(
            inner_header,
            text="✨ IDEA MANAGER ✨",
            font=("Segoe UI", 22, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        title_label.pack(pady=10)
        
        # User info and logout button row
        info_frame = tk.Frame(inner_header, bg=self.card_bg)
        info_frame.pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # User label
        user_label = tk.Label(
            info_frame,
            text=f"👤 Logged in as: {self.current_user}",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.accent_secondary
        )
        user_label.pack(side=tk.LEFT, expand=True)
        
        # Logout button
        logout_btn = tk.Button(
            info_frame,
            text="🚪 LOGOUT",
            command=self.logout,
            bg="#ff1744",
            fg=self.fg_color,
            font=("Segoe UI", 10, "bold"),
            relief=tk.RAISED,
            padx=15,
            pady=5,
            cursor="hand2",
            bd=1
        )
        logout_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Subtitle with tagline
        subtitle = tk.Label(
            inner_header,
            text="🚀 Capture • Organize • Innovate",
            font=("Segoe UI", 9, "italic"),
            bg=self.card_bg,
            fg=self.accent_secondary
        )
        subtitle.pack(pady=(0, 8))

        # Main container for input and list sections
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Input Section - For adding new ideas with premium styling
        input_label = tk.Label(
            main_frame,
            text="✏️ Your Next Big Idea",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        input_label.pack(anchor=tk.W, pady=(0, 10))

        # Text input field with neon border effect
        input_border = tk.Frame(main_frame, bg=self.accent_color, highlightthickness=0)
        input_border.pack(fill=tk.BOTH, expand=False, pady=(0, 12))
        
        self.idea_input = scrolledtext.ScrolledText(
            input_border,
            height=5,
            width=85,
            font=("Courier New", 11),
            bg="#1a1a2e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=2
        )
        self.idea_input.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.idea_input.bind("<Control-Return>", lambda e: self.add_idea())

        # Category selection with premium styling
        category_frame = tk.Frame(main_frame, bg=self.bg_color)
        category_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Left section for preset category
        category_left = tk.Frame(category_frame, bg=self.bg_color)
        category_left.pack(side=tk.LEFT, fill=tk.X, expand=False, padx=(0, 20))
        
        category_label = tk.Label(
            category_left,
            text="📌 Category:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        category_label.pack(side=tk.LEFT, padx=(0, 12))

        # Preset categories with modern styling
        self.category_var = tk.StringVar(value="General")
        categories = ["General", "Tech", "Business", "Creative", "Personal"]
        category_combo = ttk.Combobox(
            category_left,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )
        category_combo.pack(side=tk.LEFT)

        # Right section for custom category
        category_right = tk.Frame(category_frame, bg=self.bg_color)
        category_right.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        # Text box for custom category with styling
        custom_label = tk.Label(
            category_right,
            text="📝 Custom Category:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_secondary
        )
        custom_label.pack(side=tk.LEFT, padx=(0, 12))

        self.custom_category = tk.Entry(
            category_right,
            width=25,
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=2
        )
        self.custom_category.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Button section with premium styling and effects
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 20))

        # Add button with neon glow effect
        self.add_btn = tk.Button(
            button_frame,
            text="➕ ADD IDEA",
            command=self.add_idea,
            bg=self.btn_color,
            fg=self.bg_color,
            font=("Segoe UI", 11, "bold"),
            relief=tk.RAISED,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground=self.hover_color,
            activeforeground=self.bg_color,
            bd=1
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 15))
        self.add_btn.bind("<Enter>", lambda e: self.glow_button(self.add_btn, True))
        self.add_btn.bind("<Leave>", lambda e: self.glow_button(self.add_btn, False))

        # Clear all ideas button with danger styling
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ CLEAR ALL",
            command=self.clear_all,
            bg="#ff1744",
            fg=self.fg_color,
            font=("Segoe UI", 11, "bold"),
            relief=tk.RAISED,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground="#ff5252",
            activeforeground=self.fg_color,
            bd=1
        )
        clear_btn.pack(side=tk.LEFT)
        clear_btn.bind("<Enter>", lambda e: self.glow_button(clear_btn, True))
        clear_btn.bind("<Leave>", lambda e: self.glow_button(clear_btn, False))

        # Ideas List Section - Display all stored ideas
        list_label = tk.Label(
            main_frame,
            text="📚 Your Brilliant Ideas",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        list_label.pack(anchor=tk.W, pady=(20, 12))

        # Scrollable frame to hold all ideas
        self.ideas_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.ideas_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas with scrollbar for better UI management
        canvas = tk.Canvas(self.ideas_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ideas_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display all prewritten ideas
        self.display_ideas()

    # Add a new idea to the list and save to file
    def add_idea(self):
        # Get text from input field
        idea_text = self.idea_input.get("1.0", tk.END).strip()
        
        # Use custom category if provided, otherwise use dropdown selection
        custom_cat = self.custom_category.get().strip()
        category = custom_cat if custom_cat else self.category_var.get()

        # Validate input
        if not idea_text:
            messagebox.showwarning("Input Error", "Please enter an idea!")
            return

        # Save to database
        if self.save_idea(idea_text, category):
            # Reload ideas from database
            self.ideas = self.load_ideas()
            
            # Clear input and refresh display
            self.idea_input.delete("1.0", tk.END)
            self.custom_category.delete(0, tk.END)
            self.category_var.set("General")
            self.display_ideas()
            messagebox.showinfo("Success", "Idea added successfully! 💡")
        else:
            messagebox.showerror("Error", "Failed to add idea!")

    # Display all ideas with delete functionality and premium styling
    def display_ideas(self):
        # Clear previous display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Show message if no ideas exist
        if not self.ideas:
            empty_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
            empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            
            empty_label = tk.Label(
                empty_frame,
                text="🚀 No ideas yet. Time to innovate! 💡",
                font=("Segoe UI", 13, "bold"),
                bg=self.bg_color,
                fg=self.accent_secondary,
                pady=20
            )
            empty_label.pack()
            
            hint_label = tk.Label(
                empty_frame,
                text="Your brilliant ideas are waiting to be captured...",
                font=("Segoe UI", 10, "italic"),
                bg=self.bg_color,
                fg="#888888"
            )
            hint_label.pack()
            return

        # Create grid layout with 2 columns
        cols = 2
        current_row_frame = None
        cards_in_row = 0
        
        # Display each idea as a card with styling
        for index, idea in enumerate(self.ideas):
            # Create new row frame every 2 cards
            if cards_in_row == 0:
                current_row_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
                current_row_frame.pack(fill=tk.X, pady=8, padx=2)
                cards_in_row = 0
            
            # Create card in current row
            self.create_idea_card(index, idea, current_row_frame)
            cards_in_row += 1
            
            # Reset counter after 2 cards
            if cards_in_row >= cols:
                cards_in_row = 0

    # Create individual idea card with premium styling and visual effects
    def create_idea_card(self, index, idea, parent_frame):
        # Outer border frame for neon effect
        border_frame = tk.Frame(parent_frame, bg=self.accent_color, highlightthickness=0)
        border_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=5)

        # Inner card frame with gradient-like background
        card_frame = tk.Frame(border_frame, bg=self.card_bg, relief=tk.FLAT, bd=0, width=380, height=280)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        card_frame.pack_propagate(False)

        # Top section with category badge
        top_frame = tk.Frame(card_frame, bg=self.accent_color, height=35)
        top_frame.pack(fill=tk.X)

        # Category badge with styling
        category_label = tk.Label(
            top_frame,
            text=f"  📌 {idea['category']}  ",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg=self.bg_color,
            padx=10,
            pady=6
        )
        category_label.pack(side=tk.LEFT)
        
        # View button to pop up the idea note
        view_btn = tk.Button(
            top_frame,
            text="  📝 VIEW  ",
            command=lambda: self.show_idea_popup(idea),
            bg="#00bfa5",
            fg=self.bg_color,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#1dd1a1"
        )
        view_btn.pack(side=tk.RIGHT, padx=4, pady=6)
        
        # Delete button in top right
        delete_btn = tk.Button(
            top_frame,
            text="  ✕  ",
            command=lambda: self.delete_idea(index),
            bg="#ff1744",
            fg=self.fg_color,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#ff5252"
        )
        delete_btn.pack(side=tk.RIGHT, padx=8, pady=6)

        # Content section with idea text
        content_frame = tk.Frame(card_frame, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Idea text with premium font - truncated for card display
        idea_preview = idea['text'][:150] + "..." if len(idea['text']) > 150 else idea['text']
        text_label = tk.Label(
            content_frame,
            text=idea_preview,
            font=("Segoe UI", 10),
            bg=self.card_bg,
            fg=self.fg_color,
            justify=tk.LEFT,
            wraplength=700
        )
        text_label.pack(anchor=tk.W, pady=(0, 12), fill=tk.X)

        # Footer with timestamp
        footer_frame = tk.Frame(card_frame, bg="#0f0f1e", height=30)
        footer_frame.pack(fill=tk.X)

        # Timestamp label with accent color
        date_label = tk.Label(
            footer_frame,
            text=f"  ⏰ {idea['date']}  ",
            font=("Segoe UI", 9),
            bg="#0f0f1e",
            fg=self.accent_secondary
        )
        date_label.pack(side=tk.LEFT, padx=8, pady=7)

    # Delete a specific idea by index
    def delete_idea(self, index):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this idea?"):
            idea_id = self.ideas[index]['id']
            if self.delete_idea_from_db(idea_id):
                # Reload from database
                self.ideas = self.load_ideas()
                self.display_ideas()
                messagebox.showinfo("Success", "Idea deleted!")
            else:
                messagebox.showerror("Error", "Failed to delete idea!")

    # Show idea in a popup window
    def show_idea_popup(self, idea):
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"📝 {idea['category']} - Idea Note")
        popup.geometry("700x500")
        popup.configure(bg=self.bg_color)
        popup.resizable(True, True)
        
        # Center the popup window
        center_window(popup, 700, 500)
        
        # Header with category
        header_frame = tk.Frame(popup, bg=self.accent_color, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text=f"📌 Category: {idea['category']}",
            font=("Segoe UI", 15, "bold"),
            bg=self.accent_color,
            fg=self.bg_color,
            padx=20,
            pady=15
        )
        header_label.pack(anchor=tk.W)
        
        # Main content area
        content_frame = tk.Frame(popup, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Label for text area
        text_label = tk.Label(
            content_frame,
            text="📝 Idea Details:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        text_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Idea text with scrollable area (editable)
        text_border = tk.Frame(content_frame, bg=self.accent_color)
        text_border.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        text_area = scrolledtext.ScrolledText(
            text_border,
            height=18,
            width=80,
            font=("Segoe UI", 10),
            bg="#0f0f1e",
            fg=self.fg_color,
            insertbackground=self.accent_color,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Insert idea text
        text_area.insert("1.0", idea['text'])
        
        # Footer with timestamp and close button
        footer_frame = tk.Frame(popup, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        date_label = tk.Label(
            footer_frame,
            text=f"⏰ Created: {idea['date']}",
            font=("Segoe UI", 9, "italic"),
            bg=self.bg_color,
            fg=self.accent_secondary
        )
        date_label.pack(side=tk.LEFT, expand=True)
        
        close_btn = tk.Button(
            footer_frame,
            text="✕ CLOSE",
            command=popup.destroy,
            bg="#ff1744",
            fg=self.fg_color,
            font=("Segoe UI", 10, "bold"),
            relief=tk.RAISED,
            padx=20,
            pady=7,
            cursor="hand2",
            activebackground="#ff5252",
            bd=1
        )
        close_btn.pack(side=tk.RIGHT)

    # Clear all ideas with confirmation
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete ALL ideas? This cannot be undone!"):
            # Get user ID and delete all their ideas
            user = self.db.fetch_one("SELECT id FROM users WHERE username = %s", (self.current_user,))
            if user and self.db.execute_query("DELETE FROM ideas WHERE user_id = %s", (user['id'],)):
                self.ideas.clear()
                self.display_ideas()
                messagebox.showinfo("Success", "All ideas cleared!")
            else:
                messagebox.showerror("Error", "Failed to clear ideas!")

    # Logout function - return to login screen
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Relaunch login window
            root = tk.Tk()
            login_app = LoginWindow(root)
            root.mainloop()
    def glow_button(self, button, is_hovering):
        if is_hovering:
            button.config(relief=tk.RAISED, bd=2)
        else:
            button.config(relief=tk.FLAT, bd=0)

    # Legacy hover effects compatibility
    def on_hover(self, button):
        self.glow_button(button, True)

    # Restore button color when mouse leaves
    def on_leave(self, button):
        self.glow_button(button, False)

# Launch main app with current user
def launch_main_app(username, db):
    root = tk.Tk()
    app = IdeaManager(root, username, db)
    root.mainloop()

# Initialize and run the application
if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()
