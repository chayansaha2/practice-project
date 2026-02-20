
import json 
import random
import string
from pathlib import Path








class Bank:

    database = 'data.json'
    data =[]

    try:
        if Path(database).exists:
            with open(database) as fs:
                data = json.loads(fs.read())

        else:
            print("Database doesn't exsit")
    except Exception as err:
        print(f"An error ouured as {err}")


    @classmethod
    def __update(cls):
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerator(cls):
        alpha = random.choices(string.ascii_letters, k = 3)
        num = random.choices(string.digits, k =3 )
        spchar = random.choices("!@##%%%&*", k = 1)

        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
    

    def createaccount(self):
        info = {
            "name": input("Tell me your name:-"),
            "age" : int(input("Tell me your age:-")),
            "email": input("Tell me your email id:-"),
            "pin": int(input("Tell me your pin:-")),
            "accountNo": Bank.__accountgenerator(),
            "balance" : 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("sorry you can't open a account")

        else:
            print("Account has been created successfully...")

        for i in info:
            print(f"{i}: {info[i]}")
        print("Please notedown your Account Number")


        Bank.data.append(info)
        
        Bank.__update()


    def depositemoney(self):
        accountNum = input("Enter your account number:-")
        pinNo = int (input("Enter  your pin number:"))

        useraccount = [i for i in Bank.data if i["accountNo"] == accountNum and i["pin"] == pinNo]
        if useraccount == False:
            print("Sorry no user foound")
        else:
            amount = int(input("How much money do you want to deposite:-"))
            useraccount[0]["balance"] += amount
            Bank.__update()
        print("Money diposite successfully!")

    
    def withdrawmoney(self):
        accountNum = input("Enter your account number:-")
        try:
            pinNo = int(input("Enter your pin number:-"))
            
            # Corrected List Comprehension syntax
            useraccount = [i for i in Bank.data if i["accountNo"] == accountNum and i["pin"] == pinNo]

            if not useraccount: # Checks if the list is empty
                print("Sorry, no user found with those credentials.")
            else:
                target = useraccount[0]
                amount = int(input("How much money do you want to withdraw?: "))
                
                if amount <= 0:
                    print("Amount must be positive!")
                elif target["balance"] < amount:
                    print(f"Insufficient funds! Your balance is: {target['balance']}")
                else:
                    target["balance"] -= amount
                    Bank.__update() # Save the change to JSON
                    print(f"Successfully withdrew {amount}. New balance: {target['balance']}")
                
        except ValueError:
            print("Invalid input! Please enter numbers for PIN and Amount.")
    

    def showdetails(self):
        accountNum = input("Enter your account number:-")
        pinNo = int (input("Enter  your pin number:"))

        useraccount = [i for i in Bank.data if i["accountNo"] == accountNum and i["pin"] == pinNo]
        print("Here is your personal information:")

        for i in useraccount[0]:
            print(f" {i}: {useraccount[0][i]}")


  
    def updatedetails(self):
        accountNum = input("Enter your account number:-")
        pinNo = int (input("Enter  your pin number:"))

        useraccount = [i for i in Bank.data if i["accountNo"] == accountNum and i["pin"] == pinNo]

        if not useraccount:
            print("No data found")
            return
        else:
            print("you can't change age, account number and balace")
            print("Fill the details for change or leave it empty if no changes")
            newdata ={
                "name" : input("Please tell a new name and enter:-"),
                "email" : input("please tell me new email and enter:-"),
                "pin" : input("Tell me your new pin:-")        
            }
            if newdata["name"] == "":
                newdata["name"] = useraccount[0]["name"]
            if newdata["email"] == "":
                newdata["email"] = useraccount[0]["email"]
            if newdata["pin"] == "":
                newdata["pin"]= useraccount[0]["pin"]

            newdata["age"] = useraccount[0]["age"]
            newdata["accountNo"] = useraccount[0]["accountNo"]
            newdata["balance"] = useraccount[0]["balance"]

            if type(newdata["pin"]) ==str:
                newdata["pin"] = int(newdata["pin"])

            for i in newdata:
               if newdata[i] == useraccount[0][i]:
                continue
               else: 
                useraccount[0][i] = newdata[i]

            Bank.__update()
            print("Your details update successfully")


    def deleteaccount(self):
        accountNum = input("Enter your account number:-")
        pinNo = int (input("Enter  your pin number:"))

        useraccount = [i for i in Bank.data if i["accountNo"] == accountNum and i["pin"] == pinNo]
        if not useraccount:
            print("no result found")
        else:
            check = input("For delete your account press Y")
            if check == 'n' or check == 'N':
                pass
            else:
                index = Bank.data.index(useraccount[0])
                Bank.data.pop(index)
                print("Account delete successfully!")

                Bank.__update()









user = Bank()


print("Press 1 for Creating a bank account:-")
print("Press 2 for Depositing money:-")
print("press 3 for Withdrawing money:-")
print("press 4 for Details:-")
print("press 5 for Updateing account details:-")
print("press 6 for Deleting account:-")

check = int(input("Tell me your response:"))

if check == 1:
    user.createaccount()
if check == 2:
    user.depositemoney()
if check == 3:
    user.withdrawmoney()
if check == 4:
    user.showdetails()
if check == 5:
    user.updatedetails()
if check == 6:
    user.deleteaccount()
