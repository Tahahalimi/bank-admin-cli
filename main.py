import sqlite3
from colorama import Fore, Style

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    national_id TEXT NOT NULL UNIQUE,
    balance REAL NOT NULL
)
''')
conn.commit()
conn.close()

class Account:
    def __init__(self,name,lastName,idNumber,balance):
        self.name = name
        self.lastName = lastName
        self.idNumber = idNumber
        self.balance = balance

def show_menu():
    print(Fore.CYAN + '''
1. Open new account
2. Account information
3. Withdraw
4. Deposit
5. Transfer
6. Check balance
7. Exit
''' + Style.RESET_ALL)
    
def add_account(account):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO accounts (name, lastname ,national_id , balance) VALUES (?, ?, ?, ?)",
        (account.name,account.lastName,account.idNumber, account.balance)
    )

    conn.commit()
    acc_id = cursor.lastrowid
    account_number = f"9{acc_id:05}"
    conn.close()
    print(Fore.GREEN + f"Account for {account.name} added to database!")
    print(Fore.GREEN + f"The account number is {account_number}")


def show_accounts():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts")
    all_accounts = cursor.fetchall()
    
    for acc in all_accounts:
        print(acc)

    conn.close()

def get_account(acc_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE id = ?",
        (acc_id,)
    )

    account = cursor.fetchone()

    conn.close()

    return account

def convert_id(acc_id):
    if acc_id.startswith("9"):
        return int(acc_id[1:])
    return None

def transaction(sendId,receiveid, amount):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id=?",(sendId,))
    senderBalnce = cursor.fetchone()[0]
    cursor.execute("SELECT balance FROM accounts WHERE id =?",(receiveid,))
    receiverBalance = cursor.fetchone()[0]
    amount = float(amount)
    if senderBalnce >= amount:
        sNew = senderBalnce - amount
        rNew = receiverBalance + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?",(sNew,sendId))
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?",(rNew,receiveid))
        conn.commit()
        conn.close()
        print(Fore.GREEN + f"Transaction is complete! Sender new balance: {sNew}$")
    else:
        print(Fore.RED + "Sender balance is not enough to do the transaction")
        print(Fore.RED + f"Sender Balnce: {senderBalnce}$")

def check_Balance(accid):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM  accounts WHERE id=?",(accid,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        print(Fore.GREEN + f"balance: {balance}$")
    else:
        print(Fore.RED + "Account not found!")

    conn.close()
def updateBalance(accid,amount,operation):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE id=?",(accid,))
    result = cursor.fetchone()
    amount = float(amount)
    if result:
        balance = result[0]
        if operation == "4":
            newBalance = balance + amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?",(newBalance,accid))
            conn.commit()
            print(Fore.GREEN + f"Deposit successful. New balance:{newBalance}$")
        elif operation == "3":
            if balance >= amount:
                newBalance = balance - amount
                cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?",(newBalance,accid))
                conn.commit()
                print(Fore.GREEN + f"withdraw successful. New balance:{newBalance}$")
            else:
                print(Fore.RED + f"Not enough balance! Current balance: {balance}$")
    else:
        print("Account not found!")
    conn.close()


print(Fore.MAGENTA + r'''
=========================
      BANK CLI
        V1.0
=========================
''' + Style.RESET_ALL)

while True:
    show_menu()
    toDo = input("what should I do for you? ")
    if toDo == "1":
        Name = input("Enter the First Name of the user: ")
        lastName = input("Enter the Last Name of the user: ")
        idnumber = input("Enter the id Number of user: ")
        balance = float(input("Enter the start balance of the user: "))
        add_account(Account(Name,lastName,idnumber,balance))
    if toDo == "2":
        num = input("Enter account number to check information: ")
        num = convert_id(num)

        if num is None:
            print(Fore.RED + "Invalid Account number")
            print()
        else:
            acc = get_account(num)

            if acc:
                print(Fore.GREEN + f'''
============================
Account Information
============================
Name       : {acc[1]} {acc[2]}
National ID: {acc[3]}
Balance    : {acc[4]}$
============================
''')
            else:
                print(Fore.RED + "Account not found")
    if toDo =="3":
        accid = input("Enter The account id: ")
        amount = input("Enter the amount you want withdraw: ")
        accid = convert_id(accid)
        updateBalance(accid,amount,"3")
        print()
    if toDo =="4":
        accid = input("Enter The account id: ")
        amount = input("Enter the amount you want Deposit: ")
        accid = convert_id(accid)
        updateBalance(accid,amount,"4")
        print()
    if toDo =="5":
        senderAcc = input("Enter the sender account: ")
        receiverAcc = input("Enter receiver account: ")
        amount = input("Enter the amount: ")
        senderAcc = convert_id(senderAcc)
        receiverAcc = convert_id(receiverAcc)
        if senderAcc and receiverAcc:
            transaction(senderAcc,receiverAcc,amount)
            print()
        else:
            print(Fore.RED + "something went wrong double check the accounts numbers")
            print()
    if toDo =="6":
        accid = input("Enter the accont id: ")
        accid = convert_id(accid)
        check_Balance(accid)
        print()
    if toDo == "7":
        print(Fore.YELLOW + "Goodbye")
        break