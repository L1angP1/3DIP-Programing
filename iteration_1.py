# This is the iteration_1 of my program
import tkinter as tk
from tkinter import ttk, messagebox

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


# Main GUI class for the Career Pathway Advisor application
class CareerAdvisorGUI:
    def __init__(self, root):
        self.root = root                       # Store the root window
        self.root.title("Career Pathway Advisor")  # Set window title
        self.root.geometry("600x500")          # Set window size
        self.root.configure(bg="#f0f0f0")      # Set background color
        
        self.advisor = Career_advisor()        # Create career advisor instance
        
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
        
        # Name input section
        ttk.Label(self.main_frame, text="Your Name:", font=("Arial", 12)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.name_var = tk.StringVar()         # Variable to store name input
        self.name_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.name_var, 
            font=("Arial", 12),
            width=30
        )
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Interests input section
        ttk.Label(self.main_frame, text="Your Interests:", font=("Arial", 12)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.interests_text = tk.Text(        # Text area for entering interests
            self.main_frame, 
            height=4, 
            width=30,
            font=("Arial", 12)
        )
        self.interests_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        # Helper text for formatting interests
        ttk.Label(self.main_frame, text="Separate interests with commas", foreground="gray").grid(
            row=3, column=1, sticky=tk.W, pady=(0, 10)
        )
        
        # Submit button to get career suggestions
        self.submit_button = ttk.Button(
            self.main_frame, 
            text="Get Career Suggestions", 
            command=self.get_suggestions,
            style="Accent.TButton"
        )
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Results area to display career suggestions
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Career Suggestions", padding="10")
        self.results_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
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
        self.main_frame.rowconfigure(5, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Style configuration for buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        
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
            
        # Process interests (split by comma, strip whitespace, and convert to lowercase)
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
        self.results_text.delete("1.0", tk.END)        # Clear previous results1
        
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


def main():
    root = tk.Tk()                          # Create main application window
    app = CareerAdvisorGUI(root)            # Initialize the GUI application
    root.mainloop()                         # Start the GUI loop


# Entry point of the program
if __name__ == "__main__":
    main()
