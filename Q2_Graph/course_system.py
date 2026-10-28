from course import Course
from graph import Graph

CODE_PREFIX = "CS"     # every course code starts with these letters
CODE_DIGITS = 3        # ... followed by this many digits, e.g. CS101


def build_sample_data():
    """Create the course dictionary and the prerequisite graph."""
    courses = {
        "CS101": Course("CS101", "Introduction to Programming", 4, "core"),
        "CS201": Course("CS201", "Data Structures", 4, "core"),
        "CS301": Course("CS301", "Advanced Algorithms", 4, "core"),
        "CS302": Course("CS302", "Database Systems", 3, "core"),
        "CS401": Course("CS401", "Machine Learning", 3, "elective"),
        "CS402": Course("CS402", "Web Development", 3, "elective"),
    }

    graph = Graph()
    for code in courses:                  # one vertex per course code
        graph.addVertex(code)

    # course code : list of the codes it requires as prerequisites
    prerequisites = {
        "CS201": ["CS101"],
        "CS301": ["CS101", "CS201"],
        "CS302": ["CS201"],
        "CS401": ["CS301"],
        "CS402": ["CS302"],
    }
    for course_code, prereq_codes in prerequisites.items():
        for prereq_code in prereq_codes:
            graph.addEdge(prereq_code, course_code)   # arrow: prerequisite -> course

    return courses, graph


def is_valid_code(code):
    """Return True if code is the prefix followed by exactly CODE_DIGITS digits."""
    digits = code[len(CODE_PREFIX):]
    return (code.startswith(CODE_PREFIX)
            and len(digits) == CODE_DIGITS
            and digits.isdigit())


def ask_course(courses, prompt):
    """Ask for a course code and return the Course, or None if it doesn't exist."""
    code = input(prompt).strip().upper()
    if code not in courses:
        print("Course not found.")
        return None
    return courses[code]


def print_prerequisites(courses, graph, course):
    """Print the prerequisites (incoming edges) of a course and return their codes."""
    prereq_codes = graph.listIncomingAdjacentVertex(course.course_code)
    print(f"\nPrerequisites for {course.course_code} - {course.course_name}:")
    if not prereq_codes:
        print("- None")
    for code in prereq_codes:
        print(f"- {code} ({courses[code].course_name})")
    return prereq_codes


def list_courses(courses, graph):
    """Mandatory (a): display all course names."""
    print("\nAvailable Courses:")
    for number, course in enumerate(courses.values(), start=1):
        print(f"{number}. {course.course_code} - {course.course_name}")


def view_details(courses, graph):
    """Mandatory (b): show every detail of one course."""
    course = ask_course(courses, "Enter Course Code: ")
    if course:
        print(f"\nCourse details of {course.course_code}")
        print(course)


def view_prerequisites(courses, graph):  # Arrows coming in (pre -> course)
    """Mandatory (c): list the incoming edges of a course."""
    course = ask_course(courses, "Enter Course Code: ")
    if course:
        print_prerequisites(courses, graph, course)

### (pre -> course -> unlocked)
def view_unlocked(courses, graph):  # Arrows going out (course -> unlocked)
    """Mandatory (d): list the outgoing edges of a course."""
    course = ask_course(courses, "Enter Course Code: ")
    if course:
        unlocked_codes = graph.listOutgoingAdjacentVertex(course.course_code)
        print(f"\nCourses unlocked by {course.course_code} - {course.course_name}:")
        if not unlocked_codes:
            print("- None")
        for code in unlocked_codes:
            print(f"- {code} ({courses[code].course_name})")


def add_course(courses, graph):
    """Optional (a): add a new course (a new vertex) on demand."""
    print("\n--- Add New Course ---")
    code = input("Enter Course Code (e.g. CS601): ").strip().upper()
    if not is_valid_code(code):
        print(f"Invalid code: use {CODE_PREFIX} followed by {CODE_DIGITS} digits "
              f"(e.g. CS601). Course not added.")
        return
    if code in courses:
        print("That course code already exists. Course not added.")
        return
    name = input("Enter Course Name: ").strip()
    if name == "":
        print("Course name is required. Course not added.")
        return
    try:
        credit_hours = int(input("Enter Credit Hours: "))
    except ValueError:
        print("Credit hours must be a whole number. Course not added.")
        return
    if credit_hours <= 0:
        print("Credit hours must be positive. Course not added.")
        return
    level = input("Enter Level (core/elective): ").strip().lower()
    if level not in ("core", "elective"):
        print("Level must be 'core' or 'elective'. Course not added.")
        return

    courses[code] = Course(code, name, credit_hours, level)   # store the details
    graph.addVertex(code)                                     # add the vertex
    print(f"Course {code} added successfully.")


def add_prerequisite(courses, graph):
    """Optional (c): course X adds course Y as a prerequisite (new edge Y -> X)."""
    print("\n--- Add Prerequisite ---")
    course = ask_course(courses, "Enter the course that needs a prerequisite: ")
    if course is None:
        return

    print_prerequisites(courses, graph, course)  # show what it already requires
    prereq = ask_course(courses, "Enter the course to add as its prerequisite: ")
    if prereq is None:
        return
    if graph.addEdge(prereq.course_code, course.course_code):
        print(f"{prereq.course_code} is now a prerequisite of {course.course_code}.")
    else:
        print("Could not add: already a prerequisite, or the same course.")


def remove_prerequisite(courses, graph):
    """Optional (d): course X removes course Y as a prerequisite (remove edge Y -> X)."""
    print("\n--- Remove Prerequisite ---")
    course = ask_course(courses, "Enter the course to remove a prerequisite from: ")
    if course is None:
        return
    if not print_prerequisites(courses, graph, course):  # show what can be removed
        print("There is nothing to remove.")
        return
    prereq = ask_course(courses, "Enter the prerequisite course to remove: ")
    if prereq is None:
        return
    if graph.removeEdge(prereq.course_code, course.course_code):
        print(f"{prereq.course_code} is no longer a prerequisite of {course.course_code} anymore.")
    else:
        print("That prerequisite link does not exist.")


def view_profile(courses, graph):
    """Optional (b): electives show only the name, core courses show everything."""
    course = ask_course(courses, "Enter Course Code: ")
    if course:
        print(f"\nCourse profile of {course.course_code}")
        print(course.profile())


def main():
    """Build the data and run the menu loop."""
    courses, graph = build_sample_data()
    actions = {                                   # menu choice -> function
        "1": list_courses,
        "2": view_details,
        "3": view_prerequisites,
        "4": view_unlocked,
        "5": add_course,
        "6": add_prerequisite,
        "7": remove_prerequisite,
        "8": view_profile,
    }
    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. Add a New Course")
        print("6. Add a Prerequisite")
        print("7. Remove a Prerequisite")
        print("8. View Course Profile (elective details hidden)")
        print("9. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "9":
            print("Exiting program. Goodbye!")
            break
        elif choice in actions:
            actions[choice](courses, graph)
        else:
            print("Invalid choice, please enter 1-9.")


if __name__ == "__main__":
    main()
