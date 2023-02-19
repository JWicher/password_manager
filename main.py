import tkinter
from tkinter import messagebox
import random
import json
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def validate(website,username, pwd):
    if len(website) == 0 or len(username) == 0 or len(pwd) == 0:
        return False

    return True


def generate_password():
    input_password.delete(0, tkinter.END)

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = ''.join(password_list)

    input_password.insert(0, password)
    pyperclip.copy(text=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = input_website.get()
    username = input_email_username.get()
    password = input_password.get()

    is_valid = validate(username=username, website=website, pwd=password)

    if not is_valid:
        messagebox.showerror(title="Error", message="You hae not provided all data")

    else:
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Save those credentials?\nUsername: {username}\nPassword: {password}"
        )

        new_password = {
            website: {
                "password": password,
                "username": username
            }
        }

        if is_ok:
            try:
                with open(file="password_manager.json", mode='r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(file="password_manager.json", mode='w') as data_file:
                    json.dump(new_password, data_file, indent=4)
            else:
                data.update(new_password)
                with open(file="password_manager.json", mode='w') as file:
                    json.dump(data, file, indent=4)

            finally:
                input_website.delete(0, tkinter.END)
                input_password.delete(0, tkinter.END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    searched_website = input_website.get()

    try:
        with open(file="password_manager.json", mode='r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Not found", message="The is no file with data")
    else:
        if searched_website in data:
            password_details = data[searched_website]

            messagebox.showinfo(
                title=searched_website,
                message=f"website: {searched_website}\nusername: {password_details['username']}\npassword: {password_details['password']}"
            )
        else:
            messagebox.showerror(
                title="Not found",
                message=f"The website {searched_website} does not have stored "f"credentials")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password manager")
window.config(width=200, height=200, pady=20, padx=20)


# logo
image_logo = tkinter.PhotoImage(file="./logo.png")
canvas = tkinter.Canvas(width=200, height=200)
canvas.create_image(100, 100, image=image_logo)
canvas.grid(column=1, row=0)


# labels
label_website = tkinter.Label(text="Website:")
label_website.grid(row=1, column=0)

label_email_username = tkinter.Label(text="Email/Username:")
label_email_username.grid(row=2, column=0)

label_password = tkinter.Label(text="Password:")
label_password.grid( row=3, column=0)


#  inputs
input_website = tkinter.Entry(width=38)
input_website.grid(row=1, column=1, columnspan=2)
input_website.focus()

input_email_username = tkinter.Entry(width=21)
input_email_username.grid(row=2, column=1)
input_email_username.insert(0, "test@mail.com")
input_password = tkinter.Entry(width=21)
input_password.grid(row=3, column=1)


#  buttons generate
button_generate_password = tkinter.Button(text="Generate Password", command=generate_password)
button_generate_password.grid(row=3, column=2)
# button add
button_add = tkinter.Button(text="Add", width=36, command=save_password)
button_add.grid(row=4, column=1, columnspan=2)
# button search
button_search = tkinter.Button(text="Search", command=search, width=13)
button_search.grid(row=2, column=2)


# ---------------------------- APP MAINLOOP ------------------------------- #
window.mainloop()
