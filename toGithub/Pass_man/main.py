from tkinter import *
import random
import string
from tkinter import messagebox
import json

LETTERS = list(string.ascii_letters)
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
PASSWORD = []
USER = None
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_random_pass():
    global PASSWORD
    if PASSWORD:
        PASSWORD = []
    pass_entry.delete(0, END)
    for i in range(0, random.randint(4, 5)):
        PASSWORD += random.choice(LETTERS), random.choice(NUMBERS)

    random.shuffle(PASSWORD)
    pass_entry.insert(END, f"{''.join(PASSWORD)}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_pass():
    global USER
    website = web_entry.get().capitalize()
    user = USER
    password = pass_entry.get()
    new_data = {
        website: {
            'email': user,
            'password': password
        }
    }

    if website and user and password:

        is_ok = messagebox.askokcancel(message=f"Is the information below correct?\nWebsite: {
            website}\nUser: {user}\nPassword: {password}")

        if is_ok:

            try:
                with open('User_data.json', 'r') as data_file:
                    data = json.load(data_file)
                    data.update(new_data)

            except FileNotFoundError:
                with open('User_data.json', 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:

                with open('User_data.json', 'w') as data_file:
                    json.dump(data, data_file, indent=4)

        # with open('User_data.json', 'r') as data_file:
        #     # reading old data
        #     data = json.load(data_file)
        #     # updating old data with new data
        #     data.update(new_data)

        # with open('User_data.json', 'w') as data_file:
        #     # saving updated data
        #     json.dump(data, data_file, indent=4)

            finally:
                web_entry.delete(0, END)
                pass_entry.delete(0, END)
                web_entry.focus()


def selected_user(selection):
    global USER
    USER = selection


def search_user():

    website = web_entry.get().capitalize()
    user = USER
    password = pass_entry.get()

    if website and user and not (password):
        try:
            with open('User_data.json', 'r') as data_file:
                data = json.load(data_file)
                password = data[website]['password']
        except FileNotFoundError:
            messagebox.showinfo(title='Error', message='No such file found')
        except KeyError:
            messagebox.showinfo(title='Error', message=f"No details for {user} in {website}")
            
        else:
            messagebox.showinfo(title=website.capitalize(), message=f"Email:  {
                                user}\nPassword:  {password}")

        finally:
            web_entry.delete(0, END)

    # ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# --------- labels

web_label = Label(text='Website:')
web_label.grid(column=0, row=1)

user_label = Label(text='Email/Username:')
user_label.grid(column=0, row=2)

pass_label = Label(text='Password:')
pass_label.grid(column=0, row=3)

# --------- entries

web_entry = Entry(width=22)
web_entry.grid(column=1, row=1)
web_entry.focus()

pass_entry = Entry(width=22)
pass_entry.grid(column=1, row=3)


# -------- buttons


gen_pass_btn = Button(text='Generate Password', command=gen_random_pass)
gen_pass_btn.grid(column=2, row=3)

add_btn = Button(text='Add', width=36, command=add_pass)
add_btn.grid(column=1, row=4, columnspan=4)

search_btn = Button(text='Search', width=12, command=search_user)
search_btn.grid(column=2, row=1)

# --------- Menu

emails = StringVar()
menu = OptionMenu(window, emails,
                  'nuerruzzle@gmail.com',
                  'claus0844@gmail.com',
                  'nuerruel24@gmail.com',
                  command=selected_user)
menu.config(width=34)
menu.grid(column=1, row=2, columnspan=2)
emails.set('<Choose Email>')

window.mainloop()
