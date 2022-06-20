from psycopg2 import connect
from os import system
from time import localtime
from random import randint

def update_log(conn,query,type,source,dest,money):
    times=localtime()
    date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
    transaction_number=str(randint(0,100000))
    query.execute('insert into "DailyLogSystem" values(%s,%s,%s,%s,%s,%s)',(transaction_number,date,type,source,dest,money))
    conn.commit()
    
def deposit(conn,query,account):
    system('cls')
    new_in=int(input("How much money do you want to deposit?\n"))
    if new_in<0:
        print("The amount of money that you want to deposit should be greater than zero.")
        return
    query.execute('select "TransactionLimit" from "CreditCard" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if new_in>int(row[0]):
        print("Exceeded the Tranction Limit!")
        return
    query.execute('select "Savings" from "Customer" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    savings=int(row[0])+new_in
    query.execute('update "Customer" set "Savings"=%s where "Account"=%s',(savings,account))
    conn.commit()
    
    update_log(conn,query,'Deposit',account,'null',new_in)
    
    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
            path=date+'_Deposit_'+str(account)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("Your Receipt.\n")
            file.write("==============================\n")
            query.execute('select * from "Customer" where "Account"=%(account)s',{'account':account})
            row=query.fetchone()
            lines=["Name:\t\t",str(row[1]),"\nAccount:\t",str(row[2]),"\nDate:\t\t",date,"\nTime:\t\t",timing,"\nSavings:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tDeposit\nMoney:\t\t+",str(new_in)]
            file.writelines(lines)
            file.write("\n==============================\nThanks for Using.")
            break
        elif receipt==2:
            break
    return

def withdraw(conn,query,account):
    system('cls')
    new_out=int(input("How much money do you want to withdraw?\n"))
    if new_out<0:
        print("The amount of money that you want to deposit should be greater than zero.")
        return
    query.execute('select "TransactionLimit" from "CreditCard" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if new_out>int(row[0]):
        print("Exceeded the Tranction Limit!")
        return
    query.execute('select "Savings" from "Customer" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if new_out>int(row[0]):
        print("You don't have enough money to withdraw.")
        return
    savings=int(row[0])-new_out
    query.execute('update "Customer" set "Savings"=%s where "Account"=%s',(savings,account))
    conn.commit()
    
    update_log(conn,query,'Withdraw',account,'null',new_out)
    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
            path=date+'_WithDraw_'+str(account)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("Your Receipt.\n")
            file.write("==============================\n")
            query.execute('select * from "Customer" where "Account"=%(account)s',{'account':account})
            row=query.fetchone()
            lines=["Name:\t\t",str(row[1]),"\nAccount:\t",str(row[2]),"\nDate:\t\t",date,"\nTime:\t\t",timing,"\nSavings:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tWithdraw\nMoney:\t\t-",str(new_out)]
            file.writelines(lines)
            file.write("\n==============================\nThanks for Using.")
            break
        elif receipt==2:
            break
    return   

def money_transfer(conn,query,account):
    system('cls')
    dest_account=input('Please input the destination accout:')
    query.execute('select "Savings" from "Customer" where "Account"=%(account)s',{'account':dest_account})
    row_dest=query.fetchone()
    if row_dest==None:
        print('There is no account:',dest_account,'.',sep='')
        return
    transfer=int(input('How much of money do you want to transfer?\n'))
    if transfer<0:
        print("The amount of money that you want to transfer should be greater than zero.")
        return
    query.execute('select "Savings" from "Customer" where "Account"=%(account)s',{'account':account})
    row_resource=query.fetchone()
    if transfer>int(row_resource[0]):
        print("You don't have enough money to transer.")
        return
    print("Processing...")
    new_dest_saving=int(row_dest[0])+transfer
    new_res_saving=int(row_resource[0])-transfer
    query.execute('update "Customer" set "Savings"=%s where "Account"=%s',(new_res_saving,account))
    conn.commit()
    query.execute('update "Customer" set "Savings"=%s where "Account"=%s',(new_dest_saving,dest_account))
    conn.commit()
    
    update_log(conn,query,'Transfer-out',account,dest_account,transfer)
    conn.commit()
    update_log(conn,query,'Transfer-in',account,dest_account,transfer)
    conn.commit()
    
    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            times=localtime()
            date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
            path=date+'_Transfer_'+str(account)+'.txt'
            timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
            file=open(path,'w')
            file.write("Your Receipt.\n")
            file.write("==============================\n")
            query.execute('select * from "Customer" where "Account"=%(account)s',{'account':account})
            row=query.fetchone()
            lines=["Name:\t\t",str(row[1]),"\nAccount:\t",str(row[2]),"\nDest_Account:\t",str(dest_account),"\nDate:\t\t",date,"\nTime:\t\t",timing,"\nSavings:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tTransfer\nMoney:\t\t",str(transfer)]
            file.writelines(lines)
            file.write("\n==============================\nThanks for Using.")
            break
        elif receipt==2:
            break
    
    return

def balance(query,account):
    system('cls')
    times=localtime()
    print("Your Balance.")
    print("=============================")
    query.execute('select * from "Customer" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    date=str(times.tm_year)+'-'+str(times.tm_mon)+'-'+str(times.tm_mday)
    timing=str(times.tm_hour)+':'+str(times.tm_min)+':'+str(times.tm_sec)
    print('Name:\t\t',row[1])
    print('Account:\t',row[2])
    print('Savings:\t',row[3])
    print('Date:\t\t',date)
    print('Time:\t\t',timing)
    print('-----------------------------')
    print("Operation:\tCheck Balance")
    print("=============================")
    while True:
        receipt=int(input("Do you need to print the receipt?\n1:yes\n2:no\n"))
        if receipt==1:
            path=date+'_Balance_'+str(account)+'.txt'
            file=open(path,'w')
            file.write("Your Balance.\n")
            file.write("==============================\n")
            lines=["Name:\t\t",str(row[1]),"\nAccount:\t",str(row[2]),"\nSavings:\t",str(row[3]),"\nDate:\t\t",date,"\nTime:\t\t",timing,"\nSavings:\t",str(row[3])]
            file.writelines(lines)
            file.write("\n------------------------------\n")
            lines=["Operation:\tCheck Balance"]
            file.writelines(lines)
            file.write("\n==============================\nThanks for Using.")
            break
        elif receipt==2:
            break
    return

def change_password(conn,query,account):
    system('cls')
    password=input('Please input your password number again:')
    query.execute('select "Password" from "CreditCard" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if password==row[0]:
        new_password=input('Please input your new password:')
        query.execute('update "CreditCard" set "Password"=%s where "Account"=%s',(new_password,account))
        conn.commit()
        system('cls')
        print('Your password has successfully changed.')
    else:
        system('cls')
        print('Wrong Password!')
    return

def atm_system():
    system('cls')
    print("You're in atm system!")
    
    conn=connect(database='Bank',user='dufeng',password='a0984078318',host='database-3.cn4nipsynuds.us-east-1.rds.amazonaws.com',port='5432')
    query=conn.cursor()
    
    login_times=0
    account=""
    password=""
    flag=False
    #輸入錯誤5次就鎖卡
    while login_times<5:
        account=input("Please input your account number:")
        password=input("Please input your password number:")
        query.execute('select "Account","Password" from "CreditCard"')
        rows=query.fetchall()
        
        flag_account=False
        for row in rows:
            if account==row[0]:
                flag_account=True
                if password==row[1]:
                    flag=True
                    break
        if flag_account==False:
            print("There is no account:'",account,"'.",sep="")
            return
        
        if flag:
            break
        else:
            system('cls')
            print("Something got wrong with your account number or password number.")
            print("You still have ",4-login_times," times to try.")
            login_times+=1
            
    if flag==False:
        query.execute('update "CreditCard" set "Condition"=%s where "Account"=%s',('0',account))
        conn.commit()
        
    query.execute('select "Condition" from "CreditCard" where "Account"=%(account)s',{'account':account})
    row=query.fetchone()
    if row[0]==0:
        print("Your credit card is not available.")
        conn.close()
        return
    
    system('cls')
    print("Successfully login.")
    while True:
        operate=int(input("What do you want to do?\n1:Deposit\n2:Withdraw\n3:Money Transfer\n4:Check Account Balance\n5:Change the Password\n6:Quit\n"))
        flag_flag=True
        if operate==1:
            deposit(conn,query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==2:
            withdraw(conn,query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==3:
            money_transfer(conn,query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==4:
            balance(query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==5:
            change_password(conn,query,account)
            while True:
                next_op=int(input("Continue for else operation?\n1:Yes continue\n2:No Quit\n"))
                if next_op==1:
                    break
                elif next_op==2:
                    flag_flag=False
                    break
        elif operate==6:
            system('cls')
            break
        else:
            system('cls')
            print("Error!")
        
        if flag_flag:
            system('cls')
        else:
            system('cls')
            break
    conn.close()
    
if __name__=='__main__':
    atm_system()