#This calss holds information for career path and its related interests and subjects
class Subject_recommandation:
    def __init__(self, career_name, interests, subjects):
        self.career_name = career_name         
        self.interests = interests             
        self.subjects = subjects              

    #Check how many of the student's interests match the career
    def match(self, student_interests):
        score = len(set(self.interests).intersection(student_interests))
        #Calculates number of matching interests
        return score


class User:
    def __init__(self, name):
        self.name = name


    def greet(self):
        print(f"\nHi {self.name}, welcome to the Career Pathway Advisor!\n")


#Students' information
class Student(User):
    def __init__(self, name, interests):
        super().__init__(name)        
        self.interests = interests     


#Mathcing the inputs with subjects
class Career_advisor:
    def __init__(self):
        #Lists of career options with their matching interests
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

    #Check each career to see if it matches the student's interests
    def suggest(self, student):
        suggestions = []  #Create an empty list to store matched careers
        for rec in self.recommendations:
            score = rec.match(student.interests)  #Match score based on interests
            if score >= 1:  #If there's at least one match, include this career
                suggestions.append((rec.career_name, rec.subjects))
        return suggestions



def input_interests(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            #Split user inputs by commas and clean each interest
            items = [x.strip().lower() for x in raw.split(",") if x.strip()]
            if items:
                return items  # Return the list if not empty
        #If input is invalid, try again
        print("Please insert at least 1 interest (separate with commas), try again. \n")


#Main program
def main():
    # =Ask for user name and interests
    name = input("Please insert your name: ").strip()
    interests = input_interests("Please insert your interests (e.g. math, art, biology) separate with commas: ")

    #Create a student object
    student = Student(name, interests)
    student.greet()

    #Create a career advisor and get suggestions
    advisor = Career_advisor()
    results = advisor.suggest(student)

    #Display the results to the user
    if results:
        print("Depending on your interests, here are some career paths and suggested subjects that might be suitable for you:\n")
        for career, subjects in results:
            print(f"Career path: {career}")
            print(f"Suggested subjects: {', '.join(subjects)}\n")
    else:
        #If no matches found
        print("No matching careers were found. Please try entering more or different interests.")
    print("Thank you for using Career Pathway Advisor!")


# Entry point of the program
if __name__ == "__main__":
    main()
