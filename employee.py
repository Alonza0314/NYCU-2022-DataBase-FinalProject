from time import localtime
from psycopg2 import connect
from os import system

def unlock(conn,query,account):
    cu_account=input("Input customer's account:")
    cu_password=input("Input customer's password:")
    em_password=input("Input your employee password:")
    query.execute('select "Password" from "Staff" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if em_password!=row[0]:
        system('cls')
        print('Wrong Password!')
        return
    print('Processing...')
    query.execute('select "Account","Password" from "CreditCard" where "Account"=%s and "Password"=%s',(cu_account,cu_password))
    row=query.fetchone()
    if row==None:
        system('cls')
        print("Wrong account or password.")
        return
    query.execute('update "CreditCard" set "Condition"=%s where "Account"=%s',('1',cu_account))
    conn.commit()
    system("cls")
    print('Unlock Successfully!')
    return
        
def dailylog(query,account):
    password=input("Input your employee password:")
    query.execute('select "Password","Permission" from "Staff" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if password!=row[0]:
        system('cls')
        print("Wrong Password!")
        return
    if row[1]<2:
        system('cls')
        print("You don't have the right to access log.")
        return
    times=localtime()
    date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
    query.execute('select * from "DailyLogSystem"')
    rows=query.fetchall()
    for row in rows:
        print("Transaction Number: ",row[0]," \tDate: ",row[1]," \tType: ",row[2]," \tSource Account: ",row[3]," \tDestination Account: ",row[4]," \tTransaction Money: ",row[5])
    return

def employee_system():
    system('cls')
    print("You're in employ system!")
    
    conn=connect(database='Bank',user='dufeng',password='a0984078318',host='database-3.cn4nipsynuds.us-east-1.rds.amazonaws.com',port='5432')
    query=conn.cursor()
    
    account=''
    password=''
    flag=False
    
    while True:
        account=input("Please input your employee account number:")
        password=input("Please input your employee password number:")
        query.execute('select "Account","Password" from "Staff"')
        rows=query.fetchall()
        
        flag_account=False
        for row in rows:
            if account==row[0]:
                flag_account=True
                if password==row[1]:
                    flag=True
                    break
        if flag_account==False:
            print("There is no employee account:'",account,"'.",sep="")
            return

        if flag:
            break
        else:
            system('cls')
            print("Something got wrong with your account number or password number.")
    
    system('cls')
    print("Successfully login.")
    while True:
        operate=int(input('What do you want to do?\n1:Unlock Credit Card\n2:Check Daily Log\n3:Quit\n'))
        flag_flag=True
        if operate==1:
            unlock(conn,query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==2:
            dailylog(query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==3:
            system('cls')
            break
        else:
            system('cls')
            print('Error!')
        
        if flag_flag:
            system('cls')
        else:
            system('cls')
            break
    conn.close()
    
if __name__=='__main__':
    employee_system()