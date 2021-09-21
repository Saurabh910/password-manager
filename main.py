from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from json.decoder import JSONDecodeError
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list.extend([random.choice(letters) for _ in range(nr_letters)])
    password_list.extend([random.choice(symbols) for _ in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for _ in range(nr_numbers)])

    random.shuffle(password_list)
    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website_name = website_entry.get()
    email = email_entry.get()
    password = pass_entry.get()

    new_data = {
        website_name: {
            "email": email,
            "password": password
        }
    }

    if (len(website_name) or len(email) or len(password)) < 1:
        messagebox.showinfo(title="Oops!", message="Hey, You have left some field empty. Try again")
    else:
        is_ok = messagebox.askokcancel(title=website_name, message=f"These are the details enter: \nEmail: {email} "
                                                                   f"\nPassword: {password} \nIs it okay to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            except JSONDecodeError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                pass_entry.delete(0, END)


# ---------------------------- SEARCH -------------------------------- #


def search():

    website_name = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            email = data[website_name]["email"]
            password = data[website_name]["password"]
    except FileNotFoundError:
        file = open("data.json", "w")
        file.close()
    except JSONDecodeError:
        messagebox.showinfo(title="Oops!", message="The website you entered couldn't be found. Try again.")
        website_entry.delete(0, END)
    except KeyError:
        messagebox.showinfo(title="Oops!", message="The website you entered couldn't be found. Try again.")
        website_entry.delete(0, END)
    else:
        messagebox.showinfo(title="Secret Info!", message=f"{website_name}\n email: {email}\n password: {password}")
    finally:
        website_entry.delete(0, END)
        pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 95, image=logo_img)
canvas.grid(row=0, column=1)

# Website label and entry
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

# Email label and entry
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(index=0, string="typeyouremail")

# Password Label, Entry, Button
pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

pass_entry = Entry(width=35)
pass_entry.grid(row=3, column=1, columnspan=2)

pass_button = Button(text="Generate Password", width=15, command=password_generator)
pass_button.grid(row=4, column=1, sticky="E")

# Add Button
add_button = Button(text="Add", width=15, command=save)
add_button.grid(row=4, column=2, sticky="W")

# Search Button
search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=4, column=0, sticky="W")

window.mainloop()
