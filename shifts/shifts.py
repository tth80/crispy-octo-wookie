import random

SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6

names = ['Maria', 'Emilia', 'Sofia', 'Olivia', 'Aino', 'Aurora', 'Helmi', 'Ilona', 'Matilda', 'Katariina', 'Iida', 'Amanda', 'Julia', 'Ella', 'Eveliina', 'Johanna', 'Anni', 'Anna', 'Kristiina', 'Elina', 'Aleksandra', 'Sara', 'Emma', 'Aada', 'Helena', 'Karoliina', 'Linnea', 'Venla', 'Siiri', 'Alexandra', 'Juhani', 'Johannes', 'Matias', 'Mikael', 'Olavi', 'Onni', 'Ilmari', 'Oskari', 'Elias', 'Aleksi', 'Valtteri', 'Kristian', 'Antero', 'Eemeli', 'Viljami', 'Tapani', 'Oliver', 'Lauri', 'Petteri', 'Veeti', 'Eetu', 'Juho', 'Samuel', 'Tapio', 'Eemil', 'Sakari', 'Leevi', 'Emil', 'Joona', 'Anton']

class Employee:
    name = None

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Emp:{}".format(self.name)

class Company:
    shifts = None

    def __init__(self):
        self.shifts = {}
    
    def set_weekday(self, weekday, *shifts):
        self.shifts[weekday] = shifts

    def print_schedule(self):
        for day in range(7):
            shift_rep = ['{0[0]}:{0[1]} - {1[0]}:{1[1]}'.format(s_start, s_end) for s_start, s_end in self.shifts[day]]

            print("{0}: {1}".format(day, ', '.join(shift_rep)))

    def set_employees(self, *employees):
        self.employees = employees


if __name__ == '__main__':
    acme = Company()
    # define 2 shifts from 8-16 and 13-21
    acme.set_weekday(SUNDAY, ((10,00), (18,00)), ((13,00), (21,00)))
    acme.set_weekday(MONDAY, ((8,00), (16,00)), ((13,00), (21,00))) 
    acme.set_weekday(TUESDAY, ((8,00), (16,00)), ((13,00), (21,00))) 
    acme.set_weekday(WEDNESDAY, ((8,00), (16,00)), ((13,00), (21,00))) 
    acme.set_weekday(THURSDAY, ((8,00), (16,00)), ((13,00), (21,00))) 
    acme.set_weekday(FRIDAY, ((8,00), (16,00)), ((13,00), (21,00))) 
    acme.set_weekday(SATURDAY, ((8,00), (16,00)), ((13,00), (21,00))) 

    emp_pool = [Employee(random.choice(names)) for x in range(20)] # create 20 users

    acme.set_employees(*emp_pool)
    print(acme.employees)

    acme.print_schedule()
