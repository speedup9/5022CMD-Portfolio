class Course:
    """Represents a single course offered by a university."""

    def __init__(self, course_code, course_name, credit_hours, level):
        self.course_code = course_code      # str, e.g. "CS101"
        self.course_name = course_name      # str
        self.credit_hours = credit_hours    # int
        self.level = level                  # str, "core" or "elective"

    def __str__(self):
        """Full details of the course."""
        return (f"Course Code  : {self.course_code}"
                f"\nCourse Name  : {self.course_name}"
                f"\nCredit Hours : {self.credit_hours}"
                f"\nLevel        : {self.level.capitalize()}")

    def profile(self):
        """Profile view: electives only show the name, core courses show everything."""
        if self.level == "elective":
            return f"Course Name  : {self.course_name}\n(Other details are hidden for elective courses)"
        return str(self)
