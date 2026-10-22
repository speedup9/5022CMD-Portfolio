from course import Course
from graph import Graph


def build_sample_graph():
    """Create the sample courses and prerequisite links."""
    graph = Graph()
    courses = {
        "CS101": Course("CS101", "Programming Fundamentals", 4, "core"),
        "CS102": Course("CS102", "Object-Oriented Programming", 4, "core"),
        "CS201": Course("CS201", "Data Structures", 4, "core"),
        "CS202": Course("CS202", "Database Systems", 3, "core"),
        "CS301": Course("CS301", "Advanced Algorithms", 4, "core"),
        "CS302": Course("CS302", "Software Engineering", 3, "core"),
        "CS303": Course("CS303", "Machine Learning", 3, "elective"),
        "CS304": Course("CS304", "Web Development", 3, "elective"),
    }
    for course in courses.values():
        graph.addVertex(course)

    # (prerequisite, course that requires it): edge goes prerequisite -> course
    prerequisites = [
        ("CS101", "CS102"),
        ("CS102", "CS201"),
        ("CS102", "CS202"),
        ("CS201", "CS301"),
        ("CS201", "CS302"),
        ("CS202", "CS302"),
        ("CS301", "CS303"),
        ("CS202", "CS304"),
    ]
    for prereq, course in prerequisites:
        graph.addEdge(courses[prereq], courses[course])
    return graph


def find_course(graph, code):
    """Return the Course with this code, or None."""
    for course in graph.getVertices():
        if course.course_code == code.upper():
            return course
    return None


def ask_course(graph, prompt):
    """Ask for a course code and return the Course (or None with a message)."""
    code = input(prompt).strip()
    course = find_course(graph, code)
    if course is None:
        print("Course not found.")
    return course


def list_courses(graph):
    print("\n--- All Courses ---")
    for course in graph.getVertices():
        print(f"{course.course_code:<7} {course.course_name}")


def view_details(graph):
    course = ask_course(graph, "Enter course code: ")
    if course:
        print()
        print(course)


def view_prerequisites(graph):
    course = ask_course(graph, "Enter course code: ")
    if course:
        prereqs = graph.listIncomingAdjacentVertex(course)
        print(f"\nPrerequisites of {course.course_code} ({course.course_name}):")
        if not prereqs:
            print("  None")
        for p in prereqs:
            print(f"  {p.course_code} - {p.course_name}")


def view_unlocked(graph):
    course = ask_course(graph, "Enter course code: ")
    if course:
        unlocked = graph.listOutgoingAdjacentVertex(course)
        print(f"\nCourses unlocked by {course.course_code} ({course.course_name}):")
        if not unlocked:
            print("  None")
        for u in unlocked:
            print(f"  {u.course_code} - {u.course_name}")


def add_course(graph):
    print("\n--- Add New Course ---")
    code = input("Course code: ").strip().upper()
    if find_course(graph, code):
        print("That course code already exists.")
        return
    name = input("Course name: ").strip()
    try:
        credits_ = int(input("Credit hours: "))
    except ValueError:
        print("Credit hours must be a number. Course not added.")
        return
    level = input("Level (core/elective): ").strip().lower()
    if level not in ("core", "elective"):
        print("Level must be 'core' or 'elective'. Course not added.")
        return
    graph.addVertex(Course(code, name, credits_, level))
    print(f"Course {code} added.")


def add_prerequisite(graph):
    print("\n--- Add Prerequisite ---")
    course = ask_course(graph, "Course that will REQUIRE a prerequisite: ")
    if course is None:
        return
    prereq = ask_course(graph, "Course to add AS the prerequisite: ")
    if prereq is None:
        return
    if graph.addEdge(prereq, course):
        print(f"{prereq.course_code} is now a prerequisite of {course.course_code}.")
    else:
        print("Could not add: already a prerequisite, or same course.")


def remove_prerequisite(graph):
    print("\n--- Remove Prerequisite ---")
    course = ask_course(graph, "Course to remove a prerequisite from: ")
    if course is None:
        return
    prereq = ask_course(graph, "Prerequisite course to remove: ")
    if prereq is None:
        return
    if graph.removeEdge(prereq, course):
        print(f"{prereq.course_code} is no longer a prerequisite of {course.course_code}.")
    else:
        print("That prerequisite link does not exist.")


def view_profile(graph):
    course = ask_course(graph, "Enter course code: ")
    if course:
        print()
        print(course.profile())


def main():
    graph = build_sample_graph()
    actions = {
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
        print("\n===== Course Prerequisite System =====")
        print("1. List all courses")
        print("2. View course details")
        print("3. View prerequisites of a course")
        print("4. View courses unlocked by a course")
        print("5. Add a new course")
        print("6. Add a prerequisite")
        print("7. Remove a prerequisite")
        print("8. View course profile (elective details hidden)")
        print("9. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "9":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](graph)
        else:
            print("Invalid choice, please enter 1-9.")


if __name__ == "__main__":
    main()
