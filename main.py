from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generatePassword():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    passwordLetters = [choice(letters) for n in range(randint(8, 10))]
    passwordSymbols = [choice(symbols) for n in range(randint(2,4))]
    passwordNumbers = [choice(numbers) for n in range(randint(2,4))]

    passwordList = passwordLetters + passwordSymbols + passwordNumbers
    shuffle(passwordList)

    password = "".join(passwordList)
    passwordEntry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = websiteEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    newData = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
    else:
        try:
            with open("data.json", "r") as dataFile:
                #Reading old data
                data = json.load(dataFile)
        except FileNotFoundError:
            with open("data.json", "w") as dataFile:
                json.dump(newData, dataFile, indent=4)
        else:
            #Updating old data with new data
            data.update(newData)

            with open("data.json", "w") as dataFile:
                #Saving updated data
                json.dump(newData, dataFile, indent=4)
        finally:
            websiteEntry.delete(0, END)
            passwordEntry.delete(0, END)

# -------------------------- FIND PASSWORD ----------------------- #

def findPassword():
    website = websiteEntry.get()
    try:
        with open("data.json") as dataFile:
            data = json.load(dataFile)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logoImg = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logoImg)
canvas.grid(row=0,column=1)


#Labels
websiteLabel = Label(text="Website:")
websiteLabel.grid(row=1, column=0)

emailLabel = Label(text="Email/Username:")
emailLabel.grid(row=2, column=0)

passwordLabel = Label(text="Password:")
passwordLabel.grid(row=3, column=0)

#Entries
websiteEntry = Entry(width=25)
websiteEntry.grid(row=1, column=1)
websiteEntry.focus()

emailEntry = Entry(width=35)
emailEntry.grid(row=2, column=1, columnspan=2)
emailEntry.insert(0, "SomeEmail@somemail.com")

passwordEntry = Entry(width=25)
passwordEntry.grid(row=3, column=1)

#Buttons
generatePasswordButton = Button(text="Generate Password", command=generatePassword)
generatePasswordButton.grid(row=3, column=2)

addButton = Button(text="Add", width=36, command=save)
addButton.grid(row=4, column=1, columnspan=2)

searchButton = Button(text="Search", command=findPassword)
searchButton.grid(row=1, column=2)


window.mainloop()
