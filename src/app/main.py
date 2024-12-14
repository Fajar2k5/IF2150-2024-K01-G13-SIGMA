from tkinter import *
from tkinter import messagebox
import os
import sqlite3
from ware_gui import WarehouseGUI
from item_gui import ItemGUI
from wareitem_gui import WarehouseItemGUI


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "database.db")
IMG_PATH = os.path.join(os.path.dirname(BASE_DIR), "img")


root = Tk()
root.title("SIGMA")
root.geometry("900x600")
root.config(bg="white")
root.resizable(False, False)


def create_database():
    os.makedirs(DATABASE_DIR, exist_ok=True)

    # Connect to SQLite database (or create one if it doesn't exist)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username text not null,
        email text not null,
        password text not null
        )
        """)
    conn.commit()
    conn.close()


def on_focus_in(event, placeholder_text):
    entry = event.widget
    if entry.get() == placeholder_text:
        entry.delete(0, END) 


def on_focus_out(event, placeholder_text):
    entry = event.widget
    if entry.get() == "":
        entry.insert(0, placeholder_text) 


def register(username, email, password):
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO accounts (username, email, password) VALUES(?,?,? )
                        """, (username, email, password))
        connection.commit()
        cursor.execute("""
        SELECT * FROM accounts               
        """)
        connection.commit()
        print(cursor.fetchall())
        connection.close()
        return True
    except Exception as error:
        return False
    

def checkUsername(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username FROM accounts WHERE username==(?)
                       """, (username,))
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response


def checkEmail(email):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username FROM accounts WHERE email==(?)
                       """, (email,))
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response


def verifyLoginbyUsername(username, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username,password FROM accounts WHERE username==(?) AND password==(?)
                       """, (username, password))
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response


def  verifyLoginbyEmail(email, password):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT username FROM accounts WHERE email==(?) AND password==(?)
                       """, (email, password))
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response


def sign_in_page():
    def goto_register():
        login_frame.destroy()
        sign_up_page()

    def toggle_password():
        if password['show'] == '':
            showButtn.config(image=hide_icon)
            password.config(show="*")
        else:
            showButtn.config(image=show_icon)
            password.config(show='')
    def get_account_info():
        if checkUsername(user.get()):
            connect=sqlite3.connect(DATABASE_PATH)
            cursor=connect.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE username==(?)
                            """, (user.get(),))
            connect.commit()
            response = cursor.fetchone()
            connect.close()
        else:
            connect=sqlite3.connect(DATABASE_PATH)
            cursor=connect.cursor()
            cursor.execute("""
                SELECT * FROM accounts WHERE email==(?)
                            """, (user.get(),))
            connect.commit()
            response = cursor.fetchone()
            connect.close()
        return response

    def verify():
        global account_info
        if user.get() != '' and user.get() != 'Username or Email':
            if password.get() != '' and password.get() != 'Password':
                if checkUsername(user.get()) or checkEmail(user.get()):
                    res1 = verifyLoginbyUsername(user.get(), password.get())
                    res2 = verifyLoginbyEmail(user.get(), password.get())
                    if res1:
                        
                        account_info = list(get_account_info())
                        login_frame.destroy()
                        home_page()
                    elif res2:
                        account_info = list(get_account_info())
                        login_frame.destroy()
                        home_page()
                    else:
                        messagebox.showerror("Invalid", "Password is incorrect")
                else:
                    messagebox.showerror("Invalid", "Username not found")
            else:
                messagebox.showerror("Invalid", "Password is required")
        else:
            messagebox.showerror("Invalid", "Username is required")
    login_frame = Frame(root)
    login_frame.pack(pady=10)
    login_frame.pack_propagate(False)
    login_frame.configure(width=900, height=900, bg="white")
    show_icon = PhotoImage(file=os.path.join(IMG_PATH, "show.png"))
    hide_icon = PhotoImage(file=os.path.join(IMG_PATH, "hide.png"))
    img = PhotoImage(file=os.path.join(IMG_PATH, "login.png"))
    label = Label(login_frame, image=img, bg="white")
    label.image = img
    label.place(x=25, y=50)
    frame = Frame(login_frame, width=350, height=350, bg="white")
    frame.place(x=480, y=145)
    heading = Label(frame, text="Sign In", font=('Microsoft Yahei UI Light', 23 ,'bold'), fg='#6666ff', bg='white')
    heading.place(x=120, y=30)
    usernamePlaceholder = "Username or Email"
    passwordPlaceholder = "Password"
    user = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30)
    user.insert(0, usernamePlaceholder)  
    user.bind("<FocusIn>", lambda event: on_focus_in(event, usernamePlaceholder)) 
    user.bind("<FocusOut>", lambda event: on_focus_out(event, usernamePlaceholder))  
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=140)
    user.place(x=50, y=120)
    password = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30, show="*")
    password.insert(0, passwordPlaceholder)  
    password.bind("<FocusIn>", lambda event: on_focus_in(event, passwordPlaceholder)) 
    password.bind("<FocusOut>", lambda event: on_focus_out(event, passwordPlaceholder))  
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=200)
    password.place(x=50, y=180)
    showButtn=Button(frame, image=hide_icon, bd=0, width=20, height=20, bg="white", command=toggle_password)
    showButtn.image = hide_icon
    showButtn.place(x=310, y=175)

    Button(frame, text="Sign In", font=('Microsoft Yahei UI Light', 11), bg='#6666ff', fg='white', border=0, width=30, command=verify).place(x=50, y=250)
    Label(frame, text="Don't have an account?", font=('Microsoft Yahei UI Light', 9), fg='black', bg='white').place(x=50, y=285)
    Button(frame, text="Sign Up", font=('Microsoft Yahei UI Light', 9), bg='white', fg='#6666ff', border=0, command=goto_register).place(x=190, y=284)


def sign_up_page():
    def goto_login():
        register_frame.destroy()
        sign_in_page()

    def toggle_password():
        if password['show'] == '':
            showButtn.config(image=hide_icon)
            password.config(show="*")
        else:
            showButtn.config(image=show_icon)
            password.config(show='')

    def toggle_repeat_password():
        if repeatPassword['show'] == '':
            showButtn.config(image=hide_icon)
            repeatPassword.config(show="*")
        else:
            showButtn.config(image=show_icon)
            repeatPassword.config(show='')
    
    def verify():
        if user.get() != '' and user.get() != 'Username':
            if email.get() != '' and email.get() != 'Email':
                if password.get() != '' and password.get() != 'Password':
                    if repeatPassword.get() == password.get():
                        if not (checkUsername(user.get()) or checkEmail(email.get())):
                            res = register(username=user.get(), email=email.get(), password=password.get())
                            if res:
                                user.delete(0, END)
                                user.insert(0, usernamePlaceholder)
                                email.delete(0, END)
                                email.insert(0, emailPlaceholder)
                                password.delete(0, END)
                                password.insert(0, passwordPlaceholder)
                                repeatPassword.delete(0, END)
                                repeatPassword.insert(0, passwordPlaceholder)
                                messagebox.showinfo("Success", "Your account is registered" )
                        else:
                            messagebox.showerror("Invalid", "Username or Email already exist")
                    else:
                        messagebox.showerror("Invalid", "Incorrect Password")
                else:
                    messagebox.showerror("Invalid", "Password is required")
            else:
                messagebox.showerror("Invalid", "Email is required")
        else:
            messagebox.showerror("Invalid", "Username is required")
    register_frame = Frame(root)
    register_frame.pack()
    register_frame.pack_propagate(False)
    register_frame.configure(width=900, height=900, bg="white")
    show_icon = PhotoImage(file=os.path.join(IMG_PATH, "show.png"))
    hide_icon = PhotoImage(file=os.path.join(IMG_PATH, "hide.png"))
    img = PhotoImage(file=os.path.join(IMG_PATH, "login.png"))
    label = Label(register_frame, image=img, bg="white")
    label.image = img
    label.place(x=25, y=50)
    frame = Frame(register_frame, width=350, height=350, bg="white")
    frame.place(x=480, y=145)
    heading = Label(frame, text="Sign Up", font=('Microsoft Yahei UI Light', 23 , 'bold'), fg='#6666ff', bg='white')
    heading.place(x=120, y=30)
    usernamePlaceholder = "Username"
    emailPlaceholder = "Email"
    passwordPlaceholder = "Password"
    user = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30)
    user.insert(0, usernamePlaceholder)  
    user.bind("<FocusIn>", lambda event: on_focus_in(event, usernamePlaceholder)) 
    user.bind("<FocusOut>", lambda event: on_focus_out(event, usernamePlaceholder))  
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=140)
    user.place(x=50, y=120)
    email = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30)
    email.insert(0, emailPlaceholder)
    email.bind("<FocusIn>", lambda event: on_focus_in(event, emailPlaceholder))
    email.bind("<FocusOut>", lambda event: on_focus_out(event, emailPlaceholder))
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=180)
    email.place(x=50, y=160)
    password = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30, show="*")
    password.insert(0, passwordPlaceholder)  
    password.bind("<FocusIn>", lambda event: on_focus_in(event, passwordPlaceholder)) 
    password.bind("<FocusOut>", lambda event: on_focus_out(event, passwordPlaceholder))  
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=220)
    password.place(x=50, y=200)
    repeatPassword = Entry(frame, font=('Microsoft Yahei UI Light', 11), bg='white', fg='black', border=0, width=30, show="*")
    repeatPassword.insert(0, passwordPlaceholder)
    repeatPassword.bind("<FocusIn>", lambda event: on_focus_in(event, passwordPlaceholder)) 
    repeatPassword.bind("<FocusOut>", lambda event: on_focus_out(event, passwordPlaceholder))
    repeatPassword.place(x=50, y=240)
    Frame(frame, height=1, width=280, bg="black").place(x=50, y=260)
    showButtn = Button(frame, image=hide_icon, bd=0, width=20, height=20, bg="white", command=toggle_password)
    showButtn.image = hide_icon
    showButtn.place(x=310, y=195)
    showButtn = Button(frame, image=hide_icon, bd=0, width=20, height=20, bg="white", command=toggle_repeat_password)
    showButtn.image = hide_icon
    showButtn.place(x=310, y=235)    
    Button(frame, text="Sign Up", font=('Microsoft Yahei UI Light', 11), bg='#6666ff', fg='white', border=0, width=30, command=verify).place(x=50, y=280)
    Label(frame, text="Already have an account?", font=('Microsoft Yahei UI Light', 9), fg='black', bg='white').place(x=50, y=315)
    Button(frame, text="Sign In", font=('Microsoft Yahei UI Light', 9), bg='white', fg='#6666ff', border=0, command=goto_login).place(x=190, y=314)


def home_page():
    def logout():
        menuBar_Frame.destroy()
        home_frame.destroy()
        sign_in_page()
    def switch_indicator(indicator,page):
        home_indicator.configure(bg='#6666ff')
        akun_indicator.configure(bg='#6666ff')
        warehouse_indicator.configure(bg='#6666ff')
        item_indicator.configure(bg='#6666ff')
        indicator.configure(bg='white')
        if menuBar_Frame.winfo_width() > 45:
            fold_menu()
        home_frame.destroy()
        menuBar_Frame.destroy()
        page()

    def pop_menu():
        menuBar_Frame.configure(width=200)
        toggle.configure(image=close, command=fold_menu)

    def fold_menu():
        menuBar_Frame.configure(width=45)
        toggle.configure(image=open, command=pop_menu)
    menuBar_Frame = Frame(root)
    menuBar_Frame.pack(side=LEFT, fill=Y, padx=3, pady=4)
    menuBar_Frame.pack_propagate(False)
    menuBar_Frame.configure(width=45, bg='#6666ff')  
    open = PhotoImage(file=os.path.join(IMG_PATH, "toggle.png"))
    close = PhotoImage(file=os.path.join(IMG_PATH, "close.png"))
    toggle = Button(menuBar_Frame, image=open, bd=0, bg='#6666ff', command=pop_menu)
    toggle.image = open
    toggle.place(x=5, y=5)
    homeimg = PhotoImage(file=os.path.join(IMG_PATH, "home.png"))
    home = Button(menuBar_Frame, image=homeimg, bd=0, bg='#6666ff', command=lambda: switch_indicator(home_indicator, home_page))
    home.image = homeimg
    home.place(x=5, y=120)
    home_indicator = Label(menuBar_Frame, bg='white')
    home_indicator.place(x=0, y=120, width=2, height=30)
    home_label = Button(menuBar_Frame, text="Home", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white',bd=0, command=lambda: switch_indicator(home_indicator, home_page),width=10)
    home_label.place(x=50, y=120)
    akunimg = PhotoImage(file=os.path.join(IMG_PATH, "user.png"))
    akun = Button(menuBar_Frame, image=akunimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(akun_indicator, akun_page))
    akun.image = akunimg
    akun.place(x=5, y=190)
    akun_indicator = Label(menuBar_Frame, bg='#6666ff')
    akun_indicator.place(x=0, y=190, width=2, height=30)
    akun_label = Button(menuBar_Frame, text="Account", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(akun_indicator, akun_page),width=10)
    akun_label.place(x=50, y=190)
    warehouseimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouse.png"))
    warehouse = Button(menuBar_Frame, image=warehouseimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouse_indicator, warehouse_page))
    warehouse.image = warehouseimg
    warehouse.place(x=5, y=260)
    warehouse_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouse_indicator.place(x=0, y=260, width=2, height=30)
    warehouse_label = Button(menuBar_Frame, text="Warehouse", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouse_indicator, warehouse_page),width=10)
    warehouse_label.place(x=50, y=260)
    itemimg = PhotoImage(file=os.path.join(IMG_PATH, "product.png"))
    item = Button(menuBar_Frame, image=itemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(item_indicator, item_page))
    item.image = itemimg
    item.place(x=5, y=330)
    item_indicator = Label(menuBar_Frame, bg='#6666ff')
    item_indicator.place(x=0, y=330, width=2, height=30)
    item_label = Button(menuBar_Frame, text="Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(item_indicator, item_page),width=10)
    item_label.place(x=50, y=330)
    warehouseitemimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouseitem.png"))
    warehouseitem = Button(menuBar_Frame, image=warehouseitemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page))
    warehouseitem.image = warehouseitemimg
    warehouseitem.place(x=5, y=400)
    warehouseitem_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouseitem_indicator.place(x=0, y=400, width=2, height=30)
    warehouseitem_label = Button(menuBar_Frame, text="Warehouse Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page),width=13)
    warehouseitem_label.place(x=50, y=400)
    logoutimg = PhotoImage(file=os.path.join(IMG_PATH, "logout.png"))
    logoutb = Button(menuBar_Frame, image=logoutimg, bd=0, bg='#6666ff', command=logout)
    logoutb.image = logoutimg
    logoutb.place(x=10, y=550)
    logout_label = Button(menuBar_Frame, text="Logout", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', command=logout, bd=0, width=10)
    logout_label.place(x=50, y=550)
    home_frame = Frame(root)
    home_frame.pack()
    home_frame.pack_propagate(False)
    home_frame.configure(width=900, height=900, bg="white")
    label = Label(home_frame,text="Welcome to Sigma!", font=('Microsoft Yahei UI Light', 23 , 'bold'), fg='#6666ff', bg='white')
    label.place(x=300, y=50)
    img = PhotoImage(file=os.path.join(IMG_PATH, "homebg.png"))
    label1 = Label(home_frame, image=img, bg="white")
    label1.image = img
    label1.place(x=150, y=150)

def akun_page():
    def logout():
        menuBar_Frame.destroy()
        akun_frame.destroy()
        sign_in_page()
    def switch_indicator(indicator,page):
        home_indicator.configure(bg='#6666ff')
        akun_indicator.configure(bg='#6666ff')
        warehouse_indicator.configure(bg='#6666ff')
        item_indicator.configure(bg='#6666ff')
        indicator.configure(bg='white')
        if menuBar_Frame.winfo_width() > 45:
            fold_menu()
        akun_frame.destroy()
        menuBar_Frame.destroy()
        page()
    def pop_menu():
        menuBar_Frame.configure(width=200)
        toggle.configure(image=close, command=fold_menu)

    def fold_menu():
        menuBar_Frame.configure(width=45)
        toggle.configure(image=img, command=pop_menu)
    
    def verify():
        if username.get() != '':
            if email.get() != '':
                if password.get() != '':
                    res1 = checkUsername(username.get())
                    res2 = checkEmail(email.get())
                    if res1:
                        if res1[0][0] == account_info[1]:
                            if not res2:
                                connnection = sqlite3.connect(DATABASE_PATH)
                                cursor = connnection.cursor()
                                cursor.execute("""
                                    UPDATE accounts SET username=(?), email=(?), password=(?) WHERE username==(?)
                                                """, (username.get(), email.get(), password.get(), account_info[1]))
                                connnection.commit()
                                connnection.close()
                                messagebox.showinfo("Success", "Account updated")
                                global_username = username.get()
                                account_info[1] = username.get()
                                account_info[2] = email.get()
                                account_info[3] = password.get()
                            elif res2[0][0] == account_info[2]:
                                connnection = sqlite3.connect(DATABASE_PATH)
                                cursor = connnection.cursor()
                                cursor.execute("""
                                    UPDATE accounts SET username=(?), email=(?), password=(?) WHERE username==(?)
                                                """, (username.get(), email.get(), password.get(), account_info[1]))
                                connnection.commit()
                                connnection.close()
                                messagebox.showinfo("Success", "Account updated")
                                global_username = username.get()
                                account_info[1] = username.get()
                                account_info[2] = email.get()
                                account_info[3] = password.get()
                            else:
                                messagebox.showerror("Invalid", "Email already exist")
                        else:
                            messagebox.showerror("Invalid", "Username already exist")
                    elif res2:
                        if res2[0][0] == account_info[1]:
                            if not res1:
                                connnection = sqlite3.connect(DATABASE_PATH)
                                cursor = connnection.cursor()
                                cursor.execute("""
                                    UPDATE accounts SET username=(?), email=(?), password=(?) WHERE email==(?)
                                                """, (username.get(), email.get(), password.get(), account_info[2]))
                                connnection.commit()
                                connnection.close()
                                messagebox.showinfo("Success", "Account updated")
                                global_username = username.get()
                                account_info[1]=username.get()
                                account_info[2]=email.get()
                                account_info[3]=password.get()
                            elif res1[0][0] == account_info[1]:
                                connnection = sqlite3.connect(DATABASE_PATH)
                                cursor = connnection.cursor()
                                cursor.execute("""
                                    UPDATE accounts SET username=(?), email=(?), password=(?) WHERE email==(?)
                                                """, (username.get(), email.get(), password.get(), account_info[2]))
                                connnection.commit()
                                connnection.close()
                                messagebox.showinfo("Success", "Account updated")
                                global_username = username.get()
                                account_info[1]=username.get()
                                account_info[2]=email.get()
                                account_info[3]=password.get()
                            else:
                                messagebox.showerror("Invalid", "Username already exist")
                        else:
                            messagebox.showerror("Invalid", "Email already exist")
                    else:
                        connnection = sqlite3.connect(DATABASE_PATH)
                        cursor = connnection.cursor()
                        cursor.execute("""
                            UPDATE accounts SET username=(?), email=(?), password=(?) WHERE username==(?)
                                        """, (username.get(), email.get(), password.get(), account_info[1]))
                        connnection.commit()
                        connnection.close()
                        messagebox.showinfo("Success", "Account updated")
                        global_username = username.get()
                        account_info[1]=username.get()
                        account_info[2]=email.get()
                        account_info[3]=password.get()
                else:
                    messagebox.showerror("Invalid", "Password is required")
            else:
                messagebox.showerror("Invalid", "Email is required")
        else:
            messagebox.showerror("Invalid", "Username is required")


    menuBar_Frame = Frame(root)
    menuBar_Frame.pack(side=LEFT, fill=Y, padx=3, pady=4)
    menuBar_Frame.pack_propagate(False)
    menuBar_Frame.configure(width=45, bg='#6666ff')  
    img = PhotoImage(file=os.path.join(IMG_PATH, "toggle.png"))
    close = PhotoImage(file=os.path.join(IMG_PATH, "close.png"))
    toggle = Button(menuBar_Frame, image=img, bd=0, bg='#6666ff', command=pop_menu)
    toggle.image = img
    toggle.place(x=5, y=5)
    homeimg = PhotoImage(file=os.path.join(IMG_PATH, "home.png"))
    home = Button(menuBar_Frame, image=homeimg, bd=0, bg='#6666ff', command=lambda: switch_indicator(home_indicator, home_page))
    home.image = homeimg
    home.place(x=5, y=120)
    home_indicator = Label(menuBar_Frame, bg='#6666ff')
    home_indicator.place(x=0, y=120, width=2, height=30)
    home_label = Button(menuBar_Frame, text="Home", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white',bd=0, command=lambda: switch_indicator(home_indicator, home_page),width=10)
    home_label.place(x=50, y=120)
    akunimg = PhotoImage(file=os.path.join(IMG_PATH, "user.png"))
    akun = Button(menuBar_Frame, image=akunimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(akun_indicator, akun_page))
    akun.image = akunimg
    akun.place(x=5, y=190)
    akun_indicator = Label(menuBar_Frame, bg='white')
    akun_indicator.place(x=0, y=190, width=2, height=30)
    akun_label = Button(menuBar_Frame, text="Account", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(akun_indicator, akun_page),width=10)
    akun_label.place(x=50, y=190)
    warehouseimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouse.png"))
    warehouse = Button(menuBar_Frame, image=warehouseimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouse_indicator, warehouse_page))
    warehouse.image = warehouseimg
    warehouse.place(x=5, y=260)
    warehouse_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouse_indicator.place(x=0, y=260, width=2, height=30)
    warehouse_label = Button(menuBar_Frame, text="Warehouse", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouse_indicator, warehouse_page),width=10)
    warehouse_label.place(x=50, y=260)
    itemimg = PhotoImage(file=os.path.join(IMG_PATH, "product.png"))
    item = Button(menuBar_Frame, image=itemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(item_indicator, item_page))
    item.image = itemimg
    item.place(x=5, y=330)
    item_indicator = Label(menuBar_Frame, bg='#6666ff')
    item_indicator.place(x=0, y=330, width=2, height=30)
    item_label = Button(menuBar_Frame, text="Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(item_indicator, item_page),width=10)
    item_label.place(x=50, y=330)
    warehouseitemimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouseitem.png"))
    warehouseitem = Button(menuBar_Frame, image=warehouseitemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page))
    warehouseitem.image = warehouseitemimg
    warehouseitem.place(x=5, y=400)
    warehouseitem_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouseitem_indicator.place(x=0, y=400, width=2, height=30)
    warehouseitem_label = Button(menuBar_Frame, text="Warehouse Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page),width=13)
    warehouseitem_label.place(x=50, y=400)
    logoutimg = PhotoImage(file=os.path.join(IMG_PATH, "logout.png"))
    logoutb = Button(menuBar_Frame, image=logoutimg, bd=0, bg='#6666ff', command=logout)
    logoutb.image = logoutimg
    logoutb.place(x=10, y=550)
    logout_label = Button(menuBar_Frame, text="Logout", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', command=logout, bd=0, width=10)
    logout_label.place(x=50, y=550)
    akun_frame = Frame(root)
    akun_frame.pack()
    akun_frame.pack_propagate(False)
    akun_frame.configure(width=900, height=900, bg="white")
    user_label = Label(akun_frame, text="Username", font=('Microsoft Yahei UI Light', 15), bg='white', fg='black')
    user_label.place(x=325, y=150)
    username= Entry(akun_frame, font=('Microsoft Yahei UI Light', 13), bg='white', fg='black', border=1, width=30)
    username.insert(0, account_info[1])
    username.place(x=325, y=200)
    email_label = Label(akun_frame, text="Email", font=('Microsoft Yahei UI Light', 15), bg='white', fg='black')
    email_label.place(x=325, y=250)
    email = Entry(akun_frame, font=('Microsoft Yahei UI Light', 13), bg='white', fg='black', border=1, width=30)
    email.insert(0, account_info[2])
    email.place(x=325, y=300)
    password_label = Label(akun_frame, text="Password", font=('Microsoft Yahei UI Light', 15), bg='white', fg='black')
    password_label.place(x=325, y=350)
    password = Entry(akun_frame, font=('Microsoft Yahei UI Light', 13), bg='white', fg='black', border=1, width=30)
    password.insert(0, account_info[3])
    password.place(x=325, y=400)
    save = Button(akun_frame, text="Save", font=('Microsoft Yahei UI Light', 13), bg='#6666ff', fg='white', border=0, width=10, command=verify)
    save.place(x=415, y=450)   
    label = Label(akun_frame,text="Account", font=('Microsoft Yahei UI Light', 23 , 'bold'), fg='#6666ff', bg='white')
    label.place(x=400, y=50)


def warehouse_page():
    def logout():
        menuBar_Frame.destroy()
        warehouse_frame.destroy()
        sign_in_page()
    def switch_indicator(indicator,page):
        home_indicator.configure(bg='#6666ff')
        akun_indicator.configure(bg='#6666ff')
        warehouse_indicator.configure(bg='#6666ff')
        item_indicator.configure(bg='#6666ff')
        indicator.configure(bg='white')
        if menuBar_Frame.winfo_width() > 45:
            fold_menu()
        warehouse_frame.destroy()
        menuBar_Frame.destroy()
        page()
    def pop_menu():
        menuBar_Frame.configure(width=200)
        toggle.configure(image=close, command=fold_menu)

    def fold_menu():
        menuBar_Frame.configure(width=45)
        toggle.configure(image=img, command=pop_menu)

    menuBar_Frame = Frame(root)
    menuBar_Frame.pack(side=LEFT, fill=Y, padx=3, pady=4)
    menuBar_Frame.pack_propagate(False)
    menuBar_Frame.configure(width=45, bg='#6666ff')  
    img = PhotoImage(file=os.path.join(IMG_PATH, "toggle.png"))
    close = PhotoImage(file=os.path.join(IMG_PATH, "close.png"))
    toggle = Button(menuBar_Frame, image=img, bd=0, bg='#6666ff', command=pop_menu)
    toggle.image = img
    toggle.place(x=5, y=5)
    homeimg = PhotoImage(file=os.path.join(IMG_PATH, "home.png"))
    home = Button(menuBar_Frame, image=homeimg, bd=0, bg='#6666ff', command=lambda: switch_indicator(home_indicator, home_page))
    home.image = homeimg
    home.place(x=5, y=120)
    home_indicator = Label(menuBar_Frame, bg='#6666ff')
    home_indicator.place(x=0, y=120, width=2, height=30)
    home_label = Button(menuBar_Frame, text="Home", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white',bd=0, command=lambda: switch_indicator(home_indicator, home_page),width=10)
    home_label.place(x=50, y=120)
    akunimg = PhotoImage(file=os.path.join(IMG_PATH, "user.png"))
    akun = Button(menuBar_Frame, image=akunimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(akun_indicator, akun_page))
    akun.image = akunimg
    akun.place(x=5, y=190)
    akun_indicator = Label(menuBar_Frame, bg='#6666ff')
    akun_indicator.place(x=0, y=190, width=2, height=30)
    akun_label = Button(menuBar_Frame, text="Account", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(akun_indicator, akun_page),width=10)
    akun_label.place(x=50, y=190)
    warehouseimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouse.png"))
    warehouse = Button(menuBar_Frame, image=warehouseimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouse_indicator, warehouse_page))
    warehouse.image = warehouseimg
    warehouse.place(x=5, y=260)
    warehouse_indicator = Label(menuBar_Frame, bg='white')
    warehouse_indicator.place(x=0, y=260, width=2, height=30)
    warehouse_label = Button(menuBar_Frame, text="Warehouse", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouse_indicator, warehouse_page),width=10)
    warehouse_label.place(x=50, y=260)
    itemimg = PhotoImage(file=os.path.join(IMG_PATH, "product.png"))
    item = Button(menuBar_Frame, image=itemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(item_indicator, item_page))
    item.image = itemimg
    item.place(x=5, y=330)
    item_indicator = Label(menuBar_Frame, bg='#6666ff')
    item_indicator.place(x=0, y=330, width=2, height=30)
    item_label = Button(menuBar_Frame, text="Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(item_indicator, item_page),width=10)
    item_label.place(x=50, y=330)
    warehouseitemimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouseitem.png"))
    warehouseitem = Button(menuBar_Frame, image=warehouseitemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page))
    warehouseitem.image = warehouseitemimg
    warehouseitem.place(x=5, y=400)
    warehouseitem_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouseitem_indicator.place(x=0, y=400, width=2, height=30)
    warehouseitem_label = Button(menuBar_Frame, text="Warehouse Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page),width=13)
    warehouseitem_label.place(x=50, y=400)
    logoutimg = PhotoImage(file=os.path.join(IMG_PATH, "logout.png"))
    logoutb = Button(menuBar_Frame, image=logoutimg, bd=0, bg='#6666ff', command=logout)
    logoutb.image = logoutimg
    logoutb.place(x=10, y=550)
    logout_label = Button(menuBar_Frame, text="Logout", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', command=logout, bd=0, width=10)
    logout_label.place(x=50, y=550)
    warehouse_frame = Frame(root)
    warehouse_frame.pack()
    warehouse_frame.pack_propagate(False)
    warehouse_frame.configure(width=900, height=900, bg="white")
    label = Label(warehouse_frame,text="Warehouse", font=('Microsoft Yahei UI Light', 23 , 'bold'), fg='#6666ff', bg='white')
    label.place(x=400, y=50)

    # Instantiate and display the WarehouseGUI
    warehouse_gui = WarehouseGUI(warehouse_frame)
    warehouse_gui.main_frame.pack(fill=BOTH, expand=True)


def item_page():
    def logout():
        menuBar_Frame.destroy()
        item_frame.destroy()
        sign_in_page()
    def switch_indicator(indicator,page):
        home_indicator.configure(bg='#6666ff')
        akun_indicator.configure(bg='#6666ff')
        warehouse_indicator.configure(bg='#6666ff')
        item_indicator.configure(bg='#6666ff')
        indicator.configure(bg='white')
        if menuBar_Frame.winfo_width() > 45:
            fold_menu()
        item_frame.destroy()
        menuBar_Frame.destroy()
        page()
    def pop_menu():
        menuBar_Frame.configure(width=200)
        toggle.configure(image=close, command=fold_menu)

    def fold_menu():
        menuBar_Frame.configure(width=45)
        toggle.configure(image=img, command=pop_menu)

    menuBar_Frame = Frame(root)
    menuBar_Frame.pack(side=LEFT, fill=Y, padx=3, pady=4)
    menuBar_Frame.pack_propagate(False)
    menuBar_Frame.configure(width=45, bg='#6666ff')  
    img = PhotoImage(file=os.path.join(IMG_PATH, "toggle.png"))
    close = PhotoImage(file=os.path.join(IMG_PATH, "close.png"))
    toggle = Button(menuBar_Frame, image=img, bd=0, bg='#6666ff', command=pop_menu)
    toggle.image = img
    toggle.place(x=5, y=5)
    homeimg = PhotoImage(file=os.path.join(IMG_PATH, "home.png"))
    home = Button(menuBar_Frame, image=homeimg, bd=0, bg='#6666ff', command=lambda: switch_indicator(home_indicator, home_page))
    home.image = homeimg
    home.place(x=5, y=120)
    home_indicator = Label(menuBar_Frame, bg='#6666ff')
    home_indicator.place(x=0, y=120, width=2, height=30)
    home_label = Button(menuBar_Frame, text="Home", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white',bd=0, command=lambda: switch_indicator(home_indicator, home_page),width=10)
    home_label.place(x=50, y=120)
    akunimg = PhotoImage(file=os.path.join(IMG_PATH, "user.png"))
    akun = Button(menuBar_Frame, image=akunimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(akun_indicator, akun_page))
    akun.image = akunimg
    akun.place(x=5, y=190)
    akun_indicator = Label(menuBar_Frame, bg='#6666ff')
    akun_indicator.place(x=0, y=190, width=2, height=30)
    akun_label = Button(menuBar_Frame, text="Account", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(akun_indicator, akun_page),width=10)
    akun_label.place(x=50, y=190)
    warehouseimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouse.png"))
    warehouse = Button(menuBar_Frame, image=warehouseimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouse_indicator, warehouse_page))
    warehouse.image = warehouseimg
    warehouse.place(x=5, y=260)
    warehouse_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouse_indicator.place(x=0, y=260, width=2, height=30)
    warehouse_label = Button(menuBar_Frame, text="Warehouse", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouse_indicator, warehouse_page),width=10)
    warehouse_label.place(x=50, y=260)
    itemimg = PhotoImage(file=os.path.join(IMG_PATH, "product.png"))
    item = Button(menuBar_Frame, image=itemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(item_indicator, item_page))
    item.image = itemimg
    item.place(x=5, y=330)
    item_indicator = Label(menuBar_Frame, bg='white')
    item_indicator.place(x=0, y=330, width=2, height=30)
    item_label = Button(menuBar_Frame, text="Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(item_indicator, item_page),width=10)
    item_label.place(x=50, y=330)
    warehouseitemimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouseitem.png"))
    warehouseitem = Button(menuBar_Frame, image=warehouseitemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page))
    warehouseitem.image = warehouseitemimg
    warehouseitem.place(x=5, y=400)
    warehouseitem_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouseitem_indicator.place(x=0, y=400, width=2, height=30)
    warehouseitem_label = Button(menuBar_Frame, text="Warehouse Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page),width=13)
    warehouseitem_label.place(x=50, y=400)
    logoutimg = PhotoImage(file=os.path.join(IMG_PATH, "logout.png"))
    logoutb = Button(menuBar_Frame, image=logoutimg, bd=0, bg='#6666ff', command=logout)
    logoutb.image = logoutimg
    logoutb.place(x=10, y=550)
    logout_label = Button(menuBar_Frame, text="Logout", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', command=logout, bd=0, width=10)
    logout_label.place(x=50, y=550)
    item_frame = Frame(root)
    item_frame.pack()
    item_frame.pack_propagate(False)
    item_frame.configure(width=900, height=900, bg="white")
    label = Label(item_frame,text="Item", font=('Microsoft Yahei UI Light', 23 , 'bold'), fg='#6666ff', bg='white')
    label.place(x=400, y=50)

    # Instantiate and display the ItemGUI
    item_gui = ItemGUI(item_frame)
    item_gui.main_frame.pack(fill=BOTH, expand=True)


def warehouse_item_page():
    def logout():
        menuBar_Frame.destroy()
        warehouse_item.destroy()
        sign_in_page()
    def switch_indicator(indicator,page):
        home_indicator.configure(bg='#6666ff')
        akun_indicator.configure(bg='#6666ff')
        warehouse_indicator.configure(bg='#6666ff')
        item_indicator.configure(bg='#6666ff')
        indicator.configure(bg='white')
        if menuBar_Frame.winfo_width() > 45:
            fold_menu()
        warehouse_item.destroy()
        menuBar_Frame.destroy()
        page()

    def pop_menu():
        menuBar_Frame.configure(width=200)
        toggle.configure(image=close, command=fold_menu)

    def fold_menu():
        menuBar_Frame.configure(width=45)
        toggle.configure(image=img, command=pop_menu)

    menuBar_Frame = Frame(root)
    menuBar_Frame.pack(side=LEFT, fill=Y, padx=3, pady=4)
    menuBar_Frame.pack_propagate(False)
    menuBar_Frame.configure(width=45, bg='#6666ff')  
    img = PhotoImage(file=os.path.join(IMG_PATH, "toggle.png"))
    close = PhotoImage(file=os.path.join(IMG_PATH, "close.png"))
    toggle = Button(menuBar_Frame, image=img, bd=0, bg='#6666ff', command=pop_menu)
    toggle.image = img
    toggle.place(x=5, y=5)
    homeimg = PhotoImage(file=os.path.join(IMG_PATH, "home.png"))
    home = Button(menuBar_Frame, image=homeimg, bd=0, bg='#6666ff', command=lambda: switch_indicator(home_indicator, home_page))
    home.image = homeimg
    home.place(x=5, y=120)
    home_indicator = Label(menuBar_Frame, bg='#6666ff')
    home_indicator.place(x=0, y=120, width=2, height=30)
    home_label = Button(menuBar_Frame, text="Home", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white',bd=0, command=lambda: switch_indicator(home_indicator, home_page),width=10)
    home_label.place(x=50, y=120)
    akunimg = PhotoImage(file=os.path.join(IMG_PATH, "user.png"))
    akun = Button(menuBar_Frame, image=akunimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(akun_indicator, akun_page))
    akun.image = akunimg
    akun.place(x=5, y=190)
    akun_indicator = Label(menuBar_Frame, bg='#6666ff')
    akun_indicator.place(x=0, y=190, width=2, height=30)
    akun_label = Button(menuBar_Frame, text="Account", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(akun_indicator, akun_page),width=10)
    akun_label.place(x=50, y=190)
    warehouseimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouse.png"))
    warehouse = Button(menuBar_Frame, image=warehouseimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouse_indicator, warehouse_page))
    warehouse.image = warehouseimg
    warehouse.place(x=5, y=260)
    warehouse_indicator = Label(menuBar_Frame, bg='#6666ff')
    warehouse_indicator.place(x=0, y=260, width=2, height=30)
    warehouse_label = Button(menuBar_Frame, text="Warehouse", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouse_indicator, warehouse_page),width=10)
    warehouse_label.place(x=50, y=260)
    itemimg = PhotoImage(file=os.path.join(IMG_PATH, "product.png"))
    item = Button(menuBar_Frame, image=itemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(item_indicator, item_page))
    item.image = itemimg
    item.place(x=5, y=330)
    item_indicator = Label(menuBar_Frame, bg='#6666ff')
    item_indicator.place(x=0, y=330, width=2, height=30)
    item_label = Button(menuBar_Frame, text="Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(item_indicator, item_page),width=10)
    item_label.place(x=50, y=330)
    warehouseitemimg = PhotoImage(file=os.path.join(IMG_PATH, "warehouseitem.png"))
    warehouseitem = Button(menuBar_Frame, image=warehouseitemimg, bd=0, bg='#6666ff', command= lambda: switch_indicator(warehouseitem_indicator, warehouse_page))
    warehouseitem.image = warehouseitemimg
    warehouseitem.place(x=5, y=400)
    warehouseitem_indicator = Label(menuBar_Frame, bg='white')
    warehouseitem_indicator.place(x=0, y=400, width=2, height=30)
    warehouseitem_label = Button(menuBar_Frame, text="Warehouse Item", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', bd=0, command= lambda: switch_indicator(warehouseitem_indicator, warehouse_item_page),width=13)
    warehouseitem_label.place(x=50, y=400)
    logoutimg = PhotoImage(file=os.path.join(IMG_PATH, "logout.png"))
    logoutb = Button(menuBar_Frame, image=logoutimg, bd=0, bg='#6666ff', command=logout)
    logoutb.image = logoutimg
    logoutb.place(x=10, y=550)
    logout_label = Button(menuBar_Frame, text="Logout", font=('Microsoft Yahei UI Light Bold', 14), bg='#6666ff', fg='white', command=logout, bd=0, width=10)
    logout_label.place(x=50, y=550)
    warehouse_item = Frame(root)
    warehouse_item.pack()
    warehouse_item.pack_propagate(False)
    warehouse_item.configure(width=900, height=900, bg="white")
    
    warehouse_item_gui = WarehouseItemGUI(warehouse_item)
    warehouse_item_gui.main_frame.pack(fill=BOTH, expand=True)


    

# Halaman login
create_database()
sign_in_page()
root.mainloop()
