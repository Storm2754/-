class Student:
    def __init__(self, id, фамилия, имя, отчество, датаРождения, адрес, телефон, факультет, курс, группа):
        self.id = id
        self.фамилия = фамилия
        self.имя = имя
        self.отчество = отчество
        self.датаРождения = датаРождения
        self.адрес = адрес
        self.телефон = телефон
        self.факультет = факультет
        self.курс = курс
        self.группа = группа

    def __str__(self):
        return (f"Student ( id={self.id}, фамилия='{self.фамилия}', имя='{self.имя}', отчество='{self.отчество}',"
                f"датаРождения='{self.датаРождения}', адрес='{self.адрес}', телефон='{self.телефон}', "
                f"факультет='{self.факультет}', курс='{self.курс}', группа='{self.группа}')")


class Student_Management:
    @staticmethod
    def get_students_by_faculty(students, faculty):
        return [student for student in students if student.факультет == faculty]
        
    @staticmethod
    def get_students_by_faculty_and_course(students, faculty, course):
        return [student for student in students if student.факультет == faculty and student.курс == course]
        
    @staticmethod
    def get_students_born_after(students, year):
        return [student for student in students if int(student.датаРождения.split('-')[0]) > year]
        
    @staticmethod
    def get_students_by_group(students, group):
        return [student for student in students if student.группа == group]


# Создаем массив объектов
students = [
    Student(1, 'Иванов', 'Иван', 'Иванович', '2000-01-01', 'ул. Ленина, д. 1', '1234567890', 'Физика', 2, 'A'),
    Student(2, 'Петров', 'Петр', 'Петрович', '2001-02-02', 'ул. Пушкина, д. 2', '0987654321', 'Математика', 3, 'B'),
    Student(3, 'Сидоров', 'Сидор', 'Сидорович', '2002-03-03', 'ул. Чехова, д. 3', '1122334455', 'Физика', 1, 'A'),
    Student(4, 'Кузнецов', 'Алексей', 'Алексеевич', '2000-04-04', 'ул. Горького, д. 4', '2233445566', 'Химия', 2, 'B'),
    Student(5, 'Смирнова', 'Мария', 'Ивановна', '2001-05-05', 'ул. Лермонтова, д. 5', '3344556677', 'Математика', 3, 'A'),
    Student(6, 'Васильев', 'Дмитрий', 'Сергеевич', '2002-06-06', 'ул. Толстого, д. 6', '4455667788', 'Физика', 1, 'B')
]

# СПИСОК СТУДЕНТОВ С ОДНОГО ФАКУЛЬТЕТА (Задание а)
print('СПИСОК СТУДЕНТОВ С ОДНОГО ФАКУЛЬТЕТА')
physics_students = Student_Management.get_students_by_faculty(students, 'Физика')
for student in physics_students:
    print(student)
    
# СПИСОК СТУДЕНТОВ ПО ФАКУЛЬТЕТУ И КУРСУ (Задание б)
print('\nСПИСОК СТУДЕНТОВ ПО ФАКУЛЬТЕТУ И КУРСУ')
physics_course_1_students = Student_Management.get_students_by_faculty_and_course(students, 'Физика', 1)
for student in physics_course_1_students:
    print(student)
    
# СПИСОК СТУДЕНТОВ РОДИВШИХСЯ ПОСЛЕ ОПРЕДЕЛЕННОГО ГОДА (Задание в)
print('\nСПИСОК СТУДЕНТОВ РОДИВШИХСЯ ПОСЛЕ ОПРЕДЕЛЕННОГО ГОДА')
students_born_after_2001 = Student_Management.get_students_born_after(students, 2001)
for student in students_born_after_2001:
    print(student)    
    
# СПИСОК СТУДЕНТОВ ПО УЧЕБНОЙ ГРУППЕ (Задание г)
print('\nСПИСОК СТУДЕНТОВ ПО УЧЕБНОЙ ГРУППЕ')
group_A_students = Student_Management.get_students_by_group(students, 'B')
for student in group_A_students:
    print(student)
    
    
