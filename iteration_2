#THis is the iteration_2 of my programm
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# User data file for storing login credentials
USER_DATA_FILE = "users_v2.json"

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
    
    def center_window(self, width, height):
        #Centre the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_user_data(self):
        #Load user data from file
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, Exception):
                # Initialize empty dictionary if file is corrupted or empty
                self.users = {}
        else:
            self.users = {}  # Initialize empty dictionary if file doesn't exist
    
    def save_user_data(self):
        #Save user data to file
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(self.users, f, indent=4)  # Save with pretty formatting
    
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
        if self.users[username] != password:
            messagebox.showerror("Error", "Incorrect password.")
            return
        
        # Login successful, open main application
        self.open_main_app(username)
    
    def open_register(self):
        #open register window
        register_window = tk.Toplevel(self.root)  # Create new top-level window
        register_window.transient(self.root)      # Set as transient to main window
        register_window.grab_set()               # Make window modal
        RegisterGUI(register_window, self)       # Initialize registration GUI
    
    def open_main_app(self, username):
        #Open main app
        self.root.withdraw()  # Hide login window
        
        # Create main application window
        main_window = tk.Toplevel(self.root)
        # Set protocol for when window is closed
        main_window.protocol("WM_DELETE_WINDOW", lambda: self.on_main_app_close(main_window))
        app = CareerAdvisorGUI(main_window, username, self)  # Pass self (LoginGUI instance)
    
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
    
    #Centre the window on screen
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
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
        
        # Save new user data
        self.login_app.users[username] = password
        self.login_app.save_user_data()
        
        # Show success message and close registration window
        messagebox.showinfo("Success", "Registration successful! You can now login.")
        self.root.destroy()


# Main Career Advisor GUI class with user authentication
class CareerAdvisorGUI:
    def __init__(self, root, username, login_app):  # Added login_app parameter for logout functionality
        self.root = root
        self.username = username              # Store logged-in username
        self.login_app = login_app            # Save login_app reference for logout
        self.root.title(f"Career Pathway Advisor - Welcome {username}")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        self.advisor = Career_advisor()       # Create career advisor instance
        
        # Create main frame for organizing UI elements
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Title label for the application
        title_label = ttk.Label(
            self.main_frame, 
            text="Career Pathway Advisor", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Personalized welcome message
        welcome_label = ttk.Label(
            self.main_frame, 
            text=f"Welcome, {username}!",
            font=("Arial", 12)
        )
        welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Name input section
        ttk.Label(self.main_frame, text="Your Name:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.name_var = tk.StringVar()         # Variable to store name input
        self.name_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.name_var, 
            font=("Arial", 12),
            width=30
        )
        self.name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Interests input section
        ttk.Label(self.main_frame, text="Your Interests:", font=("Arial", 12)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.interests_text = tk.Text(        # Text area for entering interests
            self.main_frame, 
            height=4, 
            width=30,
            font=("Arial", 12)
        )
        self.interests_text.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        # Helper text for formatting interests
        ttk.Label(self.main_frame, text="Separate interests with commas", foreground="gray").grid(
            row=4, column=1, sticky=tk.W, pady=(0, 10)
        )
        
        # Submit button to get career suggestions
        self.submit_button = ttk.Button(
            self.main_frame, 
            text="Get Career Suggestions", 
            command=self.get_suggestions,
            style="Accent.TButton"
        )
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Results area to display career suggestions
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Career Suggestions", padding="10")
        self.results_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.results_frame.columnconfigure(0, weight=1)
        
        # Text widget to display career suggestions (initially disabled)
        self.results_text = tk.Text(
            self.results_frame, 
            height=12, 
            width=60,
            font=("Arial", 11),
            state=tk.DISABLED                  # Initially disabled to prevent editing
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results text area
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure weights for resizing
        self.main_frame.rowconfigure(6, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        
        # Logout button for user to return to login screen
        self.logout_button = ttk.Button(
            self.main_frame, 
            text="Logout", 
            command=self.logout,
            style="Secondary.TButton"
        )
        self.logout_button.grid(row=7, column=0, columnspan=2, pady=10)
        
    def get_suggestions(self):
        # Get user inputs from GUI components
        name = self.name_var.get().strip()              # Get name and remove whitespace
        interests_text = self.interests_text.get("1.0", tk.END).strip()  # Get interests text
        
        # Validate that name is not empty
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
            
        # Validate that interests are provided
        if not interests_text:
            messagebox.showerror("Error", "Please enter your interests.")
            return
            
        # Process interests - split by comma, strip whitespace, and convert to lowercase
        interests = [x.strip().lower() for x in interests_text.split(",") if x.strip()]
        # Validate that at least one interest was entered
        if not interests:
            messagebox.showerror("Error", "Please enter at least one interest separated by commas.")
            return
            
        # Create student object with provided information
        student = Student(name, interests)
        
        # Get career suggestions from the advisor
        results = self.advisor.suggest(student)
        
        # Display results in the text area
        self.display_results(student, results)
        
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
