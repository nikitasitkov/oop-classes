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

def average_student_grade_for_course(students, course):
    """Средняя оценка за домашние задания по всем студентам для заданного курса."""
    all_grades = []

    for student in students:
        if not isinstance(student, Student):
            continue

        if course in student.grades:
            all_grades.extend(student.grades[course])

    if not all_grades:
        return None

    return sum(all_grades) / len(all_grades)

def average_lecturer_grade_for_course(lecturers, course):
    """Средняя оценка за лекции по всем лекторам для заданного курса."""
    all_grades = []

    for lecturer in lecturers:
        if not isinstance(lecturer, Lecturer):
            continue

        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])

    if not all_grades:
        return None

    return sum(all_grades) / len(all_grades)


if __name__ == '__main__':

    # Два студента
    student1 = Student('Ольга', 'Алёхина', 'Ж')
    student2 = Student('Иван', 'Сидоров', 'М')

    # Два лектора
    lecturer1 = Lecturer('Иван', 'Иванов')
    lecturer2 = Lecturer('Мария', 'Петрова')

    # Два проверяющих
    reviewer1 = Reviewer('Пётр', 'Петров')
    reviewer2 = Reviewer('Елена', 'Смирнова')

    # Студенты учатся на курсах
    student1.courses_in_progress += ['Python', 'Git']
    student1.finished_courses += ['Java']

    student2.courses_in_progress += ['Python']
    student2.finished_courses += ['Git']

    # Лекторы читают курсы
    lecturer1.courses_attached += ['Python']
    lecturer2.courses_attached += ['Python', 'Git']

    # Ревьюеры проверяют ДЗ по курсам
    reviewer1.courses_attached += ['Python']
    reviewer2.courses_attached += ['Git']

    # Оценки студенту 1 по Python (от reviewer1)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 8)
    reviewer1.rate_hw(student1, 'Python', 10)

    # Оценки студенту 1 по Git (от reviewer2)
    reviewer2.rate_hw(student1, 'Git', 7)
    reviewer2.rate_hw(student1, 'Git', 9)

    # Оценки студенту 2 по Python (от reviewer1)
    reviewer1.rate_hw(student2, 'Python', 6)
    reviewer1.rate_hw(student2, 'Python', 8)

    # Пробуем поставить оценку по курсу, которого у студента нет
    print(reviewer2.rate_hw(student2, 'Git', 10))  # Ожидаем 'Ошибка'

    # Оценки студенту 1 по Python (от reviewer1)
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Python', 8)
    reviewer1.rate_hw(student1, 'Python', 10)

    # Оценки студенту 1 по Git (от reviewer2)
    reviewer2.rate_hw(student1, 'Git', 7)
    reviewer2.rate_hw(student1, 'Git', 9)

    # Оценки студенту 2 по Python (от reviewer1)
    reviewer1.rate_hw(student2, 'Python', 6)
    reviewer1.rate_hw(student2, 'Python', 8)

    # Пробуем поставить оценку по курсу, которого у студента нет
    print(reviewer2.rate_hw(student2, 'Git', 10))  # Ожидаем 'Ошибка'

    # Оценки лектору 1 по Python от обоих студентов
    student1.rate_lecture(lecturer1, 'Python', 10)
    student2.rate_lecture(lecturer1, 'Python', 8)
    student2.rate_lecture(lecturer1, 'Python', 9)

    # Оценки лектору 2 по Git и Python
    student1.rate_lecture(lecturer2, 'Git', 7)
    student1.rate_lecture(lecturer2, 'Python', 9)

    # Попытка поставить оценку по курсу, которого нет у лектора
    print(student2.rate_lecture(lecturer1, 'Git', 10))       # Ожидаем 'Ошибка'

    # Попытка поставить оценку не лектору, а ревьюеру
    print(student1.rate_lecture(reviewer1, 'Python', 10))    # Ожидаем 'Ошибка'


    print("=== Студенты ===")
    print(student1)
    print()
    print(student2)
    print()

    print("=== Лекторы ===")
    print(lecturer1)
    print()
    print(lecturer2)
    print()

    print("=== Проверяющие ===")
    print(reviewer1)
    print()
    print(reviewer2)
    print()

    print("Средняя оценка student1:", student1._avg_grade())
    print("Средняя оценка student2:", student2._avg_grade())
    print("student1 > student2 ?", student1 > student2)
    print("student1 < student2 ?", student1 < student2)

    print("Средняя оценка lecturer1:", lecturer1._avg_grade())
    print("Средняя оценка lecturer2:", lecturer2._avg_grade())
    print("lecturer1 > lecturer2 ?", lecturer1 > lecturer2)
    print("lecturer1 < lecturer2 ?", lecturer1 < lecturer2)

    students_list = [student1, student2]
    lecturers_list = [lecturer1, lecturer2]

    avg_students_python = average_student_grade_for_course(students_list, 'Python')
    avg_students_git = average_student_grade_for_course(students_list, 'Git')

    avg_lecturers_python = average_lecturer_grade_for_course(lecturers_list, 'Python')
    avg_lecturers_git = average_lecturer_grade_for_course(lecturers_list, 'Git')

    print("Средняя оценка студентов по Python:", avg_students_python)
    print("Средняя оценка студентов по Git:", avg_students_git)

    print("Средняя оценка лекторов по Python:", avg_lecturers_python)
    print("Средняя оценка лекторов по Git:", avg_lecturers_git)
