class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'

        if course not in self.courses_in_progress or course not in lecturer.courses_attached:
            return 'Ошибка'

        if not (1 <= grade <= 10):
            return 'Ошибка'

        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]

    def _avg_grade(self):
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return None
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg = self._avg_grade()
        if avg is None:
            avg_text = "нет оценок"
        else:
            avg_text = f"{avg:.1f}"

        if self.courses_in_progress:
            in_progress = ", ".join(self.courses_in_progress)
        else:
            in_progress = "нет"

        if self.finished_courses:
            finished = ", ".join(self.finished_courses)
        else:
            finished = "нет"

        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_text}\n"
                f"Курсы в процессе изучения: {in_progress}\n"
                f"Завершенные курсы: {finished}")

    def _avg_grade_or_zero(self):
        avg = self._avg_grade()
        return avg if avg is not None else 0.0

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_grade_or_zero() < other._avg_grade_or_zero()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._avg_grade_or_zero() == other._avg_grade_or_zero()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _avg_grade(self):
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return None
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg = self._avg_grade()
        if avg is None:
            avg_text = "нет оценок"
        else:
            avg_text = f"{avg:.1f}"
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_text}")

    def _avg_grade_or_zero(self):
        avg = self._avg_grade()
        return avg if avg is not None else 0.0

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_grade_or_zero() < other._avg_grade_or_zero()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._avg_grade_or_zero() == other._avg_grade_or_zero()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"




