# This is iteration_4 of my program
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# User data file for storing login credentials and user data
USER_DATA_FILE = "users_v4.json"

# This class holds information for career path and its related interests and subjects
class Subject_recommandation:
    def __init__(self, career_name, interests, subjects):
        self.career_name = career_name         # Name of the career path
        self.interests = interests             # List of interests related to this career
        self.subjects = subjects               # List of recommended subjects for this career

    # Check how many of the student's interests match the career
    def match(self, student_interests):
        # Calculate number of matching interests by finding intersection between career interests and student interests
        score = len(set(self.interests).intersection(student_interests))
        return score


class User:
    def __init__(self, name):
        self.name = name                       # Store the user's name

    def greet(self):
        # Return a personalized greeting message
        return f"\nHi {self.name}, welcome to the Gradus!\n"


# Students' information
class Student(User):
    def __init__(self, name, interests):
        super().__init__(name)                 # Initialize the parent User class
        self.interests = interests             # Store the student's interests


# Matching the inputs with subjects
class Career_advisor:
    def __init__(self):
        # Initialize list of career recommendations with predefined career paths
        self.recommendations = [
            Subject_recommandation(
                "Engineering",
                interests=["math", "physics", "design"],
                subjects=["Physics", "Calculus", "Digital Technology"]
            ),
            Subject_recommandation(
                "Healthcare",
                interests=["biology", "chemistry", "helping people"],
                subjects=["Biology", "Chemistry", "Health Education"]
            ),
            Subject_recommandation(
                "Business",
                interests=["money", "marketing", "organising"],
                subjects=["Accounting", "Economics", "Business Studies"]
            ),
            Subject_recommandation(
                "Creative Arts",
                interests=["art", "music", "writing", "design"],
                subjects=["Art", "English", "Media Studies"]
            )
        ]

    # Check each career to see if it matches the student's interests
    def suggest(self, student):
        suggestions = []  # Create an empty list to store matched careers
        # Iterate through all career recommendations
        for rec in self.recommendations:
            # Calculate match score based on shared interests
            score = rec.match(student.interests)
            # If there's at least one matching interest, include this career
            if score >= 1:
                suggestions.append((rec.career_name, rec.subjects))
        return suggestions


# Login GUI class for user authentication
class LoginGUI:
    def __init__(self, root):
        self.root = root                       # Store the root window
        self.root.title("Career Pathway Advisor - Login")  # Set window title
        self.root.geometry("500x400")          # Set window size
        self.root.configure(bg="#f0f0f0")      # Set background color
        self.root.resizable(False, False)      # Disable window resizing
        
        # Center the window on screen
        self.center_window(500, 400)
        
        # Load existing user data from file
        self.load_user_data()
        
        # Create main frame for organizing UI elements
        self.main_frame = ttk.Frame(root, padding="30")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title label for the application
        title_label = ttk.Label(
            self.main_frame, 
            text="Career Pathway Advisor", 
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Subtitle label
        subtitle_label = ttk.Label(
            self.main_frame, 
            text="Login to Your Account", 
            font=("Arial", 14)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username input section
        ttk.Label(self.main_frame, text="Username:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        self.username_var = tk.StringVar()     # Variable to store username input
        self.username_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.username_var, 
            font=("Arial", 12),
            width=25
        )
        self.username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=10)
        
        # Password input section
        ttk.Label(self.main_frame, text="Password:", font=("Arial", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=10
        )
        self.password_var = tk.StringVar()     # Variable to store password input
        self.password_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.password_var, 
            font=("Arial", 12),
            width=25,
            show="*"                           # Mask password characters
        )
        self.password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=10)
        
        # Login button
        self.login_button = ttk.Button(
            self.main_frame, 
            text="Login", 
            command=self.login,
            style="Accent.TButton"
        )
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Registration section
        ttk.Label(self.main_frame, text="Don't have an account?", font=("Arial", 10)).grid(
            row=5, column=0, columnspan=2, pady=(10, 0)
        )
        self.register_button = ttk.Button(
            self.main_frame, 
            text="Register", 
            command=self.open_register,
            style="Secondary.TButton"
        )
        self.register_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Bind Enter key to login function for convenience
        self.root.bind('<Return>', lambda event: self.login())
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        style.configure("Secondary.TButton", font=("Arial", 10))
        
        # Set initial focus to username entry field
        self.username_entry.focus()
    
    # Center the window on screen
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Load user data from JSON file with support for both old and new formats
    def load_user_data(self):
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r') as f:
                    data = json.load(f)
                    # Handle both old format (just passwords) and new format (with subjects)
                    if isinstance(data, dict) and all(isinstance(v, dict) for v in data.values()):
                        self.users = data
                    else:
                        # Convert old format to new format
                        self.users = {}
                        for username, password in data.items():
                            self.users[username] = {
                                "password": password,
                                "subjects": []
                            }
                        self.save_user_data()  # Save in new format
            except (json.JSONDecodeError, Exception):
                self.users = {}
        else:
            self.users = {}
    
    # Save user data to JSON file
    def save_user_data(self):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    # Handle user login authentication
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        # Validate that username is not empty
        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return
            
        # Validate that password is not empty
        if not password:
            messagebox.showerror("Error", "Please enter your password.")
            return
        
        # Check if username exists in user database
        if username not in self.users:
            messagebox.showerror("Error", "Username does not exist.")
            return
        
        # Check if password matches stored password
        if self.users[username]["password"] != password:
            messagebox.showerror("Error", "Incorrect password.")
            return
        
        # Login successful, open main application
        self.open_main_app(username)
    
    # Open registration window
    def open_register(self):
        register_window = tk.Toplevel(self.root)  # Create new top-level window
        register_window.transient(self.root)      # Set as transient to main window
        register_window.grab_set()               # Make window modal
        RegisterGUI(register_window, self)       # Initialize registration GUI
    
    # Open main application after successful login
    def open_main_app(self, username):
        self.root.withdraw()  # Hide login window
        
        # Create main application window
        main_window = tk.Toplevel(self.root)
        # Set protocol for when window is closed
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.on_main_app_close(main_window))
        app = CareerAdvisorGUI(main_window, username, self)  # Pass self (LoginGUI instance)
    
    # Handle main application close event
    def on_main_app_close(self, main_window):
        main_window.destroy()
        self.root.deiconify()  # Show login window again
        # Clear login form for security
        self.username_var.set("")
        self.password_var.set("")
        self.username_entry.focus()  # Set focus back to username field


# Registration GUI class for creating new user accounts
class RegisterGUI:
    def __init__(self, root, login_app):
        self.root = root
        self.login_app = login_app  # Reference to parent login application
        self.root.title("Career Pathway Advisor - Register")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window(500, 500)
        
        # Create main frame for organizing UI elements
        self.main_frame = ttk.Frame(root, padding="30")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title label
        title_label = ttk.Label(
            self.main_frame, 
            text="Create New Account", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username input section
        ttk.Label(self.main_frame, text="Username:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        self.username_var = tk.StringVar()     # Variable to store username input
        self.username_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.username_var, 
            font=("Arial", 12),
            width=25
        )
        self.username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10)
        
        # Password input section
        ttk.Label(self.main_frame, text="Password:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        self.password_var = tk.StringVar()     # Variable to store password input
        self.password_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.password_var, 
            font=("Arial", 12),
            width=25,
            show="*"                           # Mask password characters
        )
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=10)
        
        # Confirm password input section
        ttk.Label(self.main_frame, text="Confirm Password:", font=("Arial", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=10
        )
        self.confirm_password_var = tk.StringVar()  # Variable to store confirmation password
        self.confirm_password_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.confirm_password_var, 
            font=("Arial", 12),
            width=25,
            show="*"                           # Mask password characters
        )
        self.confirm_password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=10)
        
        # Register button
        self.register_button = ttk.Button(
            self.main_frame, 
            text="Register", 
            command=self.register,
            style="Accent.TButton"
        )
        self.register_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Back to login section
        ttk.Label(self.main_frame, text="Already have an account?", font=("Arial", 10)).grid(
            row=5, column=0, columnspan=2, pady=(10, 0)
        )
        self.back_button = ttk.Button(
            self.main_frame, 
            text="Back to Login", 
            command=self.root.destroy,  # Close registration window
            style="Secondary.TButton"
        )
        self.back_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Bind Enter key to register function for convenience
        self.root.bind('<Return>', lambda event: self.register())
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        style.configure("Secondary.TButton", font=("Arial", 10))
        
        # Set initial focus to username entry field
        self.username_entry.focus()
    
    # Center the window on screen
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Handle user registration and validation
    def register(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Validate that username is not empty
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
            
        # Validate that password is not empty
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
            
        # Validate that confirmation password is not empty
        if not confirm_password:
            messagebox.showerror("Error", "Please confirm your password.")
            return
        
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        # Check password length requirement
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters long.")
            return
        
        # Check if username already exists
        if username in self.login_app.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        
        # Save new user data with empty subjects list
        self.login_app.users[username] = {
            "password": password,
            "subjects": []
        }
        self.login_app.save_user_data()
        
        # Show success message and close registration window
        messagebox.showinfo("Success", "Registration successful! You can now login.")
        self.root.destroy()


# Main Career Advisor GUI class with user authentication, NCEA tracking, and Frost AI Advisor
class CareerAdvisorGUI:
    def __init__(self, root, username, login_app):
        self.root = root
        self.username = username              # Store logged-in username
        self.login_app = login_app            # Save login_app reference for logout
        self.root.title(f"Career Pathway Advisor - Welcome {username}")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        self.advisor = Career_advisor()       # Create career advisor instance
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for each tab
        self.career_frame = ttk.Frame(self.notebook, padding="10")
        self.ncea_frame = ttk.Frame(self.notebook, padding="10")
        self.frost_frame = ttk.Frame(self.notebook, padding="10")
        
        self.notebook.add(self.career_frame, text="Career Suggestions")
        self.notebook.add(self.ncea_frame, text="NCEA Grade Tracker")
        self.notebook.add(self.frost_frame, text="Frost AI Advisor")
        
        # Initialize all tabs
        self.setup_career_tab()
        self.setup_ncea_tab()
        self.setup_frost_tab()
        
    # Setup the career suggestions tab
    def setup_career_tab(self):
        # Title label
        title_label = ttk.Label(
            self.career_frame, 
            text="Career Pathway Advisor", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Personalized welcome message
        welcome_label = ttk.Label(
            self.career_frame, 
            text=f"Welcome, {self.username}!",
            font=("Arial", 12)
        )
        welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Interests input section
        ttk.Label(self.career_frame, text="Your Interests:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.interests_text = tk.Text(        # Text area for entering interests
            self.career_frame, 
            height=4, 
            width=30,
            font=("Arial", 12)
        )
        self.interests_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        # Helper text for formatting interests
        ttk.Label(self.career_frame, text="Separate interests with commas", foreground="gray").grid(
            row=3, column=1, sticky=tk.W, pady=(0, 10)
        )
        
        # Submit button to get career suggestions
        self.submit_button = ttk.Button(
            self.career_frame, 
            text="Get Career Suggestions", 
            command=self.get_suggestions,
            style="Accent.TButton"
        )
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Results area to display career suggestions
        self.results_frame = ttk.LabelFrame(self.career_frame, text="Career Suggestions", padding="10")
        self.results_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Text widget to display career suggestions (initially disabled)
        self.results_text = tk.Text(
            self.results_frame, 
            height=15, 
            width=70,
            font=("Arial", 11),
            state=tk.DISABLED                  # Initially disabled to prevent editing
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results text area
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure weights for resizing
        self.career_frame.columnconfigure(1, weight=1)
        self.career_frame.rowconfigure(5, weight=1)
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        
    # Setup the NCEA subjects and grades tab
    def setup_ncea_tab(self):
        # Title
        title_label = ttk.Label(
            self.ncea_frame, 
            text="NCEA Grade Tracker", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(
            self.ncea_frame,
            text="Add your NCEA subjects and grades to track your academic progress",
            font=("Arial", 10),
            wraplength=600
        )
        instructions.grid(row=1, column=0, columnspan=4, pady=(0, 20))
        
        # Subject input
        ttk.Label(self.ncea_frame, text="Subject:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.subject_var = tk.StringVar()
        self.subject_entry = ttk.Entry(
            self.ncea_frame,
            textvariable=self.subject_var,
            font=("Arial", 12),
            width=20
        )
        self.subject_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Level selection
        ttk.Label(self.ncea_frame, text="Level:", font=("Arial", 12)).grid(
            row=2, column=2, sticky=tk.W, pady=5, padx=5
        )
        self.level_var = tk.StringVar()
        self.level_combo = ttk.Combobox(
            self.ncea_frame,
            textvariable=self.level_var,
            values=["Level 1", "Level 2", "Level 3"],
            state="readonly",
            width=15
        )
        self.level_combo.grid(row=2, column=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.level_combo.set("Level 1")
        
        # Grade selection
        ttk.Label(self.ncea_frame, text="Grade:", font=("Arial", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.grade_var = tk.StringVar()
        self.grade_combo = ttk.Combobox(
            self.ncea_frame,
            textvariable=self.grade_var,
            values=["Not Achieved", "Achieved", "Merit", "Excellence"],
            state="readonly",
            width=15
        )
        self.grade_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.grade_combo.set("Achieved")
        
        # Credits input
        ttk.Label(self.ncea_frame, text="Credits:", font=("Arial", 12)).grid(
            row=3, column=2, sticky=tk.W, pady=5, padx=5
        )
        self.credits_var = tk.StringVar()
        self.credits_combo = ttk.Combobox(
            self.ncea_frame,
            textvariable=self.credits_var,
            values=["4", "5", "6", "8", "10", "12", "14", "16", "18", "20"],
            state="readonly",
            width=15
        )
        self.credits_combo.grid(row=3, column=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.credits_combo.set("4")
        
        # Add subject button
        self.add_subject_button = ttk.Button(
            self.ncea_frame,
            text="Add Subject",
            command=self.add_subject,
            style="Accent.TButton"
        )
        self.add_subject_button.grid(row=4, column=0, columnspan=4, pady=20)
        
        # Subjects list frame
        self.subjects_frame = ttk.LabelFrame(self.ncea_frame, text="Your NCEA Subjects", padding="10")
        self.subjects_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.subjects_frame.columnconfigure(0, weight=1)
        
        # Treeview for displaying subjects
        columns = ("Subject", "Level", "Grade", "Credits")
        self.subjects_tree = ttk.Treeview(
            self.subjects_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        # Define headings
        self.subjects_tree.heading("Subject", text="Subject")
        self.subjects_tree.heading("Level", text="Level")
        self.subjects_tree.heading("Grade", text="Grade")
        self.subjects_tree.heading("Credits", text="Credits")
        
        # Define column widths
        self.subjects_tree.column("Subject", width=200)
        self.subjects_tree.column("Level", width=100)
        self.subjects_tree.column("Grade", width=100)
        self.subjects_tree.column("Credits", width=80)
        
        self.subjects_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        tree_scrollbar = ttk.Scrollbar(self.subjects_frame, orient=tk.VERTICAL, command=self.subjects_tree.yview)
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.subjects_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Remove subject button
        self.remove_subject_button = ttk.Button(
            self.ncea_frame,
            text="Remove Selected Subject",
            command=self.remove_subject,
            style="Secondary.TButton"
        )
        self.remove_subject_button.grid(row=6, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        # Clear all button
        self.clear_subjects_button = ttk.Button(
            self.ncea_frame,
            text="Clear All Subjects",
            command=self.clear_subjects,
            style="Secondary.TButton"
        )
        self.clear_subjects_button.grid(row=6, column=2, columnspan=2, pady=10, padx=5, sticky=tk.E)
        
        # Summary frame
        self.summary_frame = ttk.LabelFrame(self.ncea_frame, text="NCEA Summary", padding="10")
        self.summary_frame.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Summary labels
        self.level1_label = ttk.Label(self.summary_frame, text="Level 1 Credits: 0", font=("Arial", 10))
        self.level1_label.grid(row=0, column=0, sticky=tk.W, padx=10)
        
        self.level2_label = ttk.Label(self.summary_frame, text="Level 2 Credits: 0", font=("Arial", 10))
        self.level2_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        self.level3_label = ttk.Label(self.summary_frame, text="Level 3 Credits: 0", font=("Arial", 10))
        self.level3_label.grid(row=0, column=2, sticky=tk.W, padx=10)
        
        self.total_label = ttk.Label(self.summary_frame, text="Total Credits: 0", font=("Arial", 10, "bold"))
        self.total_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=(5, 0))
        
        # Configure weights
        self.ncea_frame.columnconfigure(0, weight=1)
        self.ncea_frame.columnconfigure(1, weight=1)
        self.ncea_frame.columnconfigure(2, weight=1)
        self.ncea_frame.columnconfigure(3, weight=1)
        self.ncea_frame.rowconfigure(5, weight=1)
        self.subjects_frame.rowconfigure(0, weight=1)
        
        # Load existing subjects if any
        self.load_subjects()
        
    # Setup the Frost AI Advisor tab
    def setup_frost_tab(self):
        # Title
        title_label = ttk.Label(
            self.frost_frame, 
            text="Frost AI Advisor", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Description
        description = ttk.Label(
            self.frost_frame,
            text="I can help you check university subject requirements and calculate if your NCEA grades meet the Rank Score requirements.",
            font=("Arial", 10),
            wraplength=700,
            justify=tk.CENTER
        )
        description.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Chat display area
        self.chat_frame = ttk.LabelFrame(self.frost_frame, text="Chat with Frost", padding="10")
        self.chat_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)
        
        self.chat_text = tk.Text(
            self.chat_frame, 
            height=20, 
            width=80,
            font=("Arial", 11),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for chat
        chat_scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_text.yview)
        chat_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.chat_text.configure(yscrollcommand=chat_scrollbar.set)
        
        # Input frame
        input_frame = ttk.Frame(self.frost_frame)
        input_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(0, weight=1)
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_var,
            font=("Arial", 12)
        )
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_to_frost,
            style="Accent.TButton"
        )
        self.send_button.grid(row=0, column=1, sticky=tk.E)
        
        # Example queries
        examples_frame = ttk.LabelFrame(self.frost_frame, text="Example Queries", padding="10")
        examples_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        examples_text = "Try asking about: 'Computer Science', 'Medicine', 'Engineering', 'Law', 'Psychology', 'Business'"
        examples_label = ttk.Label(
            examples_frame,
            text=examples_text,
            font=("Arial", 9),
            wraplength=700,
            justify=tk.CENTER
        )
        examples_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure weights
        self.frost_frame.columnconfigure(0, weight=1)
        self.frost_frame.rowconfigure(2, weight=1)
        
        # Bind Enter key to send message
        self.input_entry.bind('<Return>', lambda event: self.send_to_frost())
        
        # Add welcome message
        self.add_frost_message("Hello! I'm Frost, your AI academic advisor. I can help you check university subject requirements based on your NCEA grades. What subject are you interested in?")
        
    # Add a message from Frost to the chat
    def add_frost_message(self, message):
        self.chat_text.configure(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"Frost: {message}\n\n")
        self.chat_text.see(tk.END)
        self.chat_text.configure(state=tk.DISABLED)
    
    # Add a message from the user to the chat
    def add_user_message(self, message):
        self.chat_text.configure(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"You: {message}\n")
        self.chat_text.see(tk.END)
        self.chat_text.configure(state=tk.DISABLED)
    
    # Process user input and generate Frost's response
    def send_to_frost(self):
        user_input = self.input_var.get().strip()
        
        if not user_input:
            return
        
        # Add user message to chat
        self.add_user_message(user_input)
        
        # Clear input field
        self.input_var.set("")
        
        # Process the query and generate response
        response = self.process_frost_query(user_input)
        
        # Add Frost's response after a short delay (simulate thinking)
        self.root.after(500, lambda: self.add_frost_message(response))
    
    # Process user query and return Frost's response
    def process_frost_query(self, query):
        query_lower = query.lower()
        
        # University subject database with rank score requirements
        subject_requirements = {
            "computer science": 250,
            "medicine": 320,
            "engineering": 260,
            "law": 280,
            "psychology": 240,
            "business": 230,
            "accounting": 240,
            "nursing": 250,
            "architecture": 270,
            "education": 220
        }
        
        # Check if query matches any known subjects
        matched_subject = None
        for subject in subject_requirements:
            if subject in query_lower:
                matched_subject = subject
                break
        
        if matched_subject:
            required_score = subject_requirements[matched_subject]
            current_score = self.calculate_rank_score()
            score_difference = required_score - current_score
            
            if score_difference <= 0:
                return f"Based on your current NCEA results, you meet the Rank Score requirement for {matched_subject.title()}! \n\nRequired: {required_score}\nYour Score: {current_score}\n\nYou have {abs(score_difference)} points above the requirement. Well done!"
            else:
                return f"For {matched_subject.title()}, the required Rank Score is {required_score}. \n\nBased on your current NCEA results, your estimated Rank Score is {current_score}. \n\nYou need {score_difference} more points to meet the requirement. Consider focusing on improving your grades in key subjects or taking additional credits."
        else:
            return "I'm not sure about that subject. Try asking about common university subjects like Computer Science, Medicine, Engineering, Law, Psychology, or Business. You can also ask about specific requirements for any subject you're interested in."
    
    # Calculate Rank Score based only on Level 3 subjects
    def calculate_rank_score(self):
        # Grade multipliers for Level 3 subjects only
        grade_multipliers = {
            "Not Achieved": 0,
            "Achieved": 2,
            "Merit": 3,
            "Excellence": 4
        }
        
        # Calculate score from Level 3 subjects only
        level3_score = 0
        
        for item in self.subjects_tree.get_children():
            values = self.subjects_tree.item(item, "values")
            subject, level, grade, credits = values
            
            # Only consider Level 3 subjects
            if level == "Level 3":
                credits_int = int(credits)
                multiplier = grade_multipliers.get(grade, 0)
                level3_score += credits_int * multiplier
        
        return level3_score
    
    # Add a subject to the NCEA list
    def add_subject(self):
        subject = self.subject_var.get().strip()
        level = self.level_var.get()
        grade = self.grade_var.get()
        credits = self.credits_var.get()
        
        if not subject:
            messagebox.showerror("Error", "Please enter a subject name.")
            return
            
        # Add to treeview
        self.subjects_tree.insert("", "end", values=(subject, level, grade, credits))
        
        # Clear input fields
        self.subject_var.set("")
        self.level_combo.set("Level 1")
        self.grade_combo.set("Achieved")
        self.credits_combo.set("4")
        
        # Update summary
        self.update_summary()
        
        # Save subjects to file
        self.save_subjects()
        
        # Set focus back to subject entry
        self.subject_entry.focus()
    
    # Remove selected subject from the list
    def remove_subject(self):
        selected_item = self.subjects_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a subject to remove.")
            return
            
        self.subjects_tree.delete(selected_item)
        self.update_summary()
        self.save_subjects()
    
    # Clear all subjects from the list
    def clear_subjects(self):
        if not self.subjects_tree.get_children():
            messagebox.showinfo("Info", "No subjects to clear.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all subjects?"):
            self.subjects_tree.delete(*self.subjects_tree.get_children())
            self.update_summary()
            self.save_subjects()
    
    # Update the NCEA summary information
    def update_summary(self):
        level1_credits = 0
        level2_credits = 0
        level3_credits = 0
        
        for item in self.subjects_tree.get_children():
            values = self.subjects_tree.item(item, "values")
            level = values[1]
            credits = int(values[3])
            
            if level == "Level 1":
                level1_credits += credits
            elif level == "Level 2":
                level2_credits += credits
            elif level == "Level 3":
                level3_credits += credits
        
        total_credits = level1_credits + level2_credits + level3_credits
        
        self.level1_label.config(text=f"Level 1 Credits: {level1_credits}")
        self.level2_label.config(text=f"Level 2 Credits: {level2_credits}")
        self.level3_label.config(text=f"Level 3 Credits: {level3_credits}")
        self.total_label.config(text=f"Total Credits: {total_credits}")
    
    # Save subjects to user data file
    def save_subjects(self):
        subjects = []
        for item in self.subjects_tree.get_children():
            values = self.subjects_tree.item(item, "values")
            subject, level, grade, credits = values
            subjects.append({
                "subject": subject,
                "level": level,
                "grade": grade,
                "credits": credits
            })
        
        # Update user data
        self.login_app.users[self.username]["subjects"] = subjects
        self.login_app.save_user_data()
    
    # Load subjects from user data
    def load_subjects(self):
        if self.username in self.login_app.users and "subjects" in self.login_app.users[self.username]:
            subjects = self.login_app.users[self.username]["subjects"]
            for subject_data in subjects:
                self.subjects_tree.insert("", "end", values=(
                    subject_data["subject"],
                    subject_data["level"],
                    subject_data["grade"],
                    subject_data["credits"]
                ))
            self.update_summary()
    
    # Get career suggestions based on user inputs
    def get_suggestions(self):
        interests_text = self.interests_text.get("1.0", tk.END).strip()
        
        # Validate that interests are provided
        if not interests_text:
            messagebox.showerror("Error", "Please enter your interests.")
            return
            
        # Process interests (split by comma, strip whitespace, and convert to lowercase)
        interests = [x.strip().lower() for x in interests_text.split(",") if x.strip()]
        # Validate that at least one interest was entered
        if not interests:
            messagebox.showerror("Error", "Please enter at least one interest separated by commas.")
            return
            
        # Create student object (using username as name)
        student = Student(self.username, interests)
        
        # Get career suggestions from the advisor
        results = self.advisor.suggest(student)
        
        # Display results in the text area
        self.display_results(student, results)
        
    # Display career suggestions in the results text area
    def display_results(self, student, results):
        # Enable text widget for editing to update content
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)        # Clear previous results
        
        # Add personalized greeting message
        self.results_text.insert(tk.END, student.greet() + "\n")
        
        # Check if any career suggestions were found
        if results:
            self.results_text.insert(
                tk.END, 
                "Depending on your interests, here are some career paths and suggested subjects that might be suitable for you:\n\n"
            )
            
            # Display each career suggestion with its subjects in numbered list
            for i, (career, subjects) in enumerate(results, 1):
                self.results_text.insert(tk.END, f"{i}. Career Path: {career}\n")
                self.results_text.insert(tk.END, f"   Suggested Subjects: {', '.join(subjects)}\n\n")
        else:
            # Display message when no matching careers are found
            self.results_text.insert(
                tk.END, 
                "No matching careers were found. Please try entering more or different interests.\n"
            )
            
        # Add closing message
        self.results_text.insert(tk.END, "Thank you for using Career Pathway Advisor!")
        
        # Disable text widget to make it read-only again
        self.results_text.configure(state=tk.DISABLED)
    
    # Logout user and return to login screen
    def logout(self):
        self.root.destroy()
        self.login_app.root.deiconify()  # Show login window again
        # Clear login form for security
        self.login_app.username_var.set("")
        self.login_app.password_var.set("")
        self.login_app.username_entry.focus()  # Set focus back to username field


def main():
    root = tk.Tk()                          # Create main application window
    login_app = LoginGUI(root)              # Initialize the login GUI
    root.mainloop()                         # Start the GUI event loop


# Entry point of the program
if __name__ == "__main__":
    main()