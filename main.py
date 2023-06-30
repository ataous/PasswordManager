import json
from random import randint, choices, shuffle
from tkinter import *
from tkinter import messagebox as msg

import pyperclip

FONT_NAME = "Inter"
DEFAULT_EMAIL = "test@email.com"
DATA_FILE = "data.json"

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_list = choices(letters, k=randint(8, 10)) + \
                    choices(numbers, k=randint(2, 4)) + \
                    choices(symbols, k=randint(2, 4))
    shuffle(password_list)
    password = ''.join(map(str, password_list))
    inp_password.delete(0, END)
    inp_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = inp_website.get().strip().title()
    email = inp_email.get().strip()
    password = inp_password.get().strip()

    if website != "" and email != "" and password != "":
        check = msg.askokcancel(title=website, message=f"These are the details entered: \n"
                                                       f"Email: {email} \n"
                                                       f"Password: {password} \n"
                                                       f"Is it ok?")
        if check:
            new_data = {
                website: {
                    "email": email,
                    "password": password
                }
            }

            try:
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open(DATA_FILE, "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open(DATA_FILE, "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                inp_website.delete(0, END)
                inp_email.delete(0, END)
                inp_password.delete(0, END)
                inp_email.insert(0, DEFAULT_EMAIL)
                inp_website.focus()
    else:
        msg.showinfo(title="Incomplete Data", message="All fields are required.")


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = inp_website.get().strip().title()

    if website != "":
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            msg.showinfo(title=website, message=f"No password has been saved for {website} yet.")
        else:
            if website in data:
                email = data[website]['email']
                password = data[website]['password']
                inp_email.delete(0, END)
                inp_password.delete(0, END)
                inp_email.insert(0, email)
                inp_password.insert(0, password)
                msg.showinfo(title=website, message=f"Email/Username: {email}\n\nPassword: {password}")
            else:
                msg.showinfo(title=website, message=f"No password has been saved for {website} yet.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

lbl_website = Label(text="Website:", bg="white", anchor="e", width=12, font=(FONT_NAME, 10, "roman"))
lbl_website.grid(row=1, column=0)

inp_website = Entry(width=32, bg="white")
inp_website.grid(row=1, column=1, sticky="w", pady=4)
inp_website.focus()

btn_search = Button(text="Search", width=16, command=search)
btn_search.grid(row=1, column=2, sticky="w")

lbl_email = Label(text="Email/Username:", bg="white", anchor="e", width=12, font=(FONT_NAME, 10, "roman"))
lbl_email.grid(row=2, column=0)

inp_email = Entry(width=53, bg="white")
inp_email.grid(row=2, column=1, columnspan=2, sticky="w", pady=4)
inp_email.insert(0, DEFAULT_EMAIL)

lbl_password = Label(text="Password:", bg="white", anchor="e", width=12, font=(FONT_NAME, 10, "roman"))
lbl_password.grid(row=3, column=0)

inp_password = Entry(width=32, bg="white")
inp_password.grid(row=3, column=1, sticky="w", pady=4)

btn_password = Button(text="Generate Password", width=16, command=generate_password)
btn_password.grid(row=3, column=2, sticky="w")

btn_add = Button(width=44, text="Add", padx=3, command=save)
btn_add.grid(row=4, column=1, columnspan=2, sticky="w", pady=5)

window.mainloop()
