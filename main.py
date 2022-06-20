import employee
import atm
from os import system

if __name__=='__main__':
    system("cls")
    while True:
        print("Welcome to our bank system!")
        system_use=int(input("Which system will want to use?\n1:atm system\n2:employee system\n"))
        if system_use==1 or system_use==2:
            break
        system("cls")
        print("Erorr!")
    system("cls")
    
    if system_use==1:
        atm.atm_system()
    else:
        employee.employee_system()
    print('Thanks for Using.')
    