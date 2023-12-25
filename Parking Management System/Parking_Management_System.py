import mysql.connector

import time

from tkinter import *
from tkinter import messagebox


con = mysql.connector.connect(
    host='localhost', database=' parking_system', user='root', password='tiger')
cursor = con.cursor()

cursor.execute('DROP TABLE IF EXISTS login;')
cursor.execute(
    'CREATE TABLE IF NOT EXISTS login (id int(11) NOT NULL PRIMARY KEY, name char(30) DEFAULT NULL, pwd char(30) DEFAULT NULL)')
s = "INSERT INTO login (id,name,pwd) VALUES (%s,%s,%s)"
b = [(1, 'mihir', 'tiger'), (2, 'soham', 'tiger'), (3, 'admin', 'tiger')]
cursor.executemany(s, b)
con.commit()

cursor.execute('DROP TABLE IF EXISTS parking_type;')
cursor.execute('CREATE TABLE IF NOT EXISTS parking_type(id int(11) NOT NULL PRIMARY KEY, name char(20) DEFAULT NULL, price float(7,2) DEFAULT NULL)')
s = "INSERT INTO parking_type (id,name,price) VALUES (%s,%s,%s)"
b = [(1, 'two wheeler', 30.00), (2, 'car', 50.00),
     (3, 'bus', 250.00), (4, 'truck', 350.00), (5, 'trolly', 450.00)]
cursor.executemany(s, b)
con.commit()

cursor.execute('DROP TABLE IF EXISTS parking_space;')
cursor.execute('CREATE TABLE IF NOT EXISTS parking_space(id int(11) NOT NULL PRIMARY KEY, type_id int(11) DEFAULT NULL, status char(20) DEFAULT NULL)')
s = "INSERT INTO parking_space (id,type_id,status) VALUES (%s,%s,%s)"
b = [(1, 1, 'full'), (2, 3, 'open'), (3, 5, 'open')]
cursor.executemany(s, b)
con.commit()

cursor.execute('DROP TABLE IF EXISTS transaction;')
cursor.execute('CREATE TABLE IF NOT EXISTS transaction (id int(11) NOT NULL PRIMARY KEY auto_increment, vehicle_id char(20) DEFAULT NULL,parkingtype_id int(11) DEFAULT NULL,parkingspace_id int(11) DEFAULT NULL,entry_time int(20) DEFAULT NULL, exit_time int(20) DEFAULT NULL, amount int(10) DEFAULT NULL)')
s = "INSERT INTO transaction (id,vehicle_id,parkingtype_id,parkingspace_id,entry_time,exit_time,amount) VALUES (%s,%s,%s,%s,%s,%s,%s)"
b = [(1, 'dl14cb-1087', 1, 1, '1635781628', '1635781999', 30)]
cursor.executemany(s, b)
con.commit()

cursor.execute('select name from parking_type')
parkingty = cursor.fetchall()
rows = cursor.rowcount

options1 = []
for i in range(rows):
    a = parkingty[i]
    b = a[0]
    options1.append(b)


def display_parking_space_records():
    cursor.execute('select * from parking_space')
    records = cursor.fetchall()
    for row in records:
        print(row)


def display_transaction():
    cursor.execute('select * from transaction')
    records = cursor.fetchall()
    for row in records:
        print(row)


def login():
    while True:
        uname = enter_name.get()
        upass = enter_passwd.get()
        cursor.execute(
            'select * from login where name="{}" and pwd ="{}"'.format(uname, upass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows != 1:
            eror_message = messagebox.showerror("Error", "Wrong credentials")
            break

        else:
            login_screen.destroy()
            main_menu()
            break


def add_parking_type_record():

    add_park_type = Tk()
    add_park_type.iconbitmap("converted1.ico")
    add_park_type.title("Parking Management System")

    header = Label(add_park_type, text="Add Parking Type Record",
                   bg="Blue", fg="white", font=30, width=50)
    header.pack(fill="both")

    name = Label(add_park_type, text="Enter Parking Type", font=10, width=25)
    name.pack(padx=10, pady=5)
    enter_name = Entry(add_park_type, width=25, borderwidth=5)
    enter_name.pack(padx=10, pady=5)

    price = Label(
        add_park_type, text="Enter Parking Price per day", font=10, width=25)
    price.pack(padx=10, pady=5)
    enter_price = Entry(add_park_type, width=25, borderwidth=5)
    enter_price.pack(padx=10, pady=5)

    submit = Button(add_park_type, text="SUBMIT", font=20, command=lambda: add_parking_type_record_p(
        enter_name.get(), enter_price.get()), bg="#97ffff")
    submit.pack(padx=10, pady=5)

    def add_parking_type_record_p(name, price):

        cursor.execute('select max(id) from parking_type')
        no = cursor.fetchone()
        new = str(no[0]+1)

        label = Label(add_park_type, text="New Parking Type ID is:" +
                      new, font=10, width=25, bg="#90ff00")
        label.pack()

        sql = 'insert into parking_type values({},"{}",{});'.format(
            new, name, price)
        cursor.execute(sql)
        con.commit()


def add_parking_slot_record():

    w = Toplevel()
    w.iconbitmap("converted1.ico")
    w.title("Parking Management System")

    header = Label(w, text="Add Parking Slot Record",
                   bg="Blue", fg="white", font=30, width=50)
    header.pack(fill="both")

    b1 = Label(w, text="Enter Parking Type", font=10, width=25)
    b1.pack(padx=10, pady=5)

    cursor.execute('select name from parking_type')
    parkingty = cursor.fetchall()
    rows = cursor.rowcount

    options1 = []
    for i in range(rows):
        a = parkingty[i]
        b = a[0]
        options1.append(b)

    clicked1 = StringVar()
    clicked1.set(options1[0])

    drop1 = OptionMenu(w, clicked1, *options1)
    drop1.pack(padx=10, pady=5)

    b2 = Label(w, text="Enter current Status", font=10, width=25)
    b2.pack(padx=10, pady=5)

    clicked2 = StringVar()
    clicked2.set("open")

    drop2 = OptionMenu(w, clicked2, "open", "full")
    drop2.pack(padx=10, pady=5)

    submit = Button(w, text="SUBMIT", font=20, command=lambda: add_parking_slot_record_p(
        clicked1.get(), clicked2.get()), bg="#97ffff")
    submit.pack(padx=10, pady=5)

    def add_parking_slot_record_p(pos, status):
        cursor.execute(
            'select id from parking_type where name="{}";'.format(pos))
        id = cursor.fetchone()
        parking_type_id = id[0]

        cursor.execute('select max(id) from parking_space')
        no = cursor.fetchone()
        new = str(no[0]+1)

        label = Label(w, text="New Parking space ID is:" +
                      new, font=10, width=25, bg="#90ff00")
        label.pack()

        sql = 'insert into parking_space values({},{},"{}")'.format(
            new, parking_type_id, status)
        cursor.execute(sql)
        con.commit()


def modify_parking_type_record():

    w = Tk()
    w.iconbitmap("converted1.ico")
    w.title("Parking Management System")

    header = Label(w, text="What do you want to change",
                   bg="Blue", fg="white", font=30, width=50)
    header.pack(fill="both")

    btn1 = Button(w, text="Parking Type Name", bg="#97ffff", font=10,
                  width=25, command=lambda: modify_parking_type_name())
    btn1.pack(padx=10, pady=5)

    btn2 = Button(w, text="Parking Type Price", bg="#97ffff", font=10,
                  width=25, command=lambda: modify_parking_type_price())
    btn2.pack(padx=10, pady=5)

    def modify_parking_type_name():
        root = Toplevel()
        root.iconbitmap("converted1.ico")
        root.title("Parking Management System")

        header1 = Label(root, text="Modify Parking Type Name",
                        bg="Blue", fg="white", font=30, width=50)
        header1.pack(fill="both")

        b1 = Label(root, text="Enter name to be changed", font=10, width=25)
        b1.pack(padx=10, pady=5)

        cursor.execute('select name from parking_type')
        parkingty = cursor.fetchall()
        rows = cursor.rowcount

        options1 = []
        for i in range(rows):
            a = parkingty[i]
            b = a[0]
            options1.append(b)

        clicked1 = StringVar()
        clicked1.set(options1[0])

        drop1 = OptionMenu(root, clicked1, *options1)
        drop1.pack(padx=10, pady=5)

        b2 = Label(root, text="Enter new value", font=10, width=25)
        b2.pack(padx=10, pady=5)

        e1 = Entry(root, borderwidth=5)
        e1.pack(padx=10, pady=5)

        submit = Button(root, text="SUBMIT", font=20, command=lambda: modify_parking_type_name_p(
            clicked1.get(), e1.get()), bg="#97ffff")
        submit.pack(padx=10, pady=5)

        def modify_parking_type_name_p(pos, value):
            cursor.execute(
                'select id from parking_type where name="{}";'.format(pos))
            id = cursor.fetchone()
            park_id = id[0]
            cursor.execute(
                'update parking_type set name="{}" where id={}'.format(value, park_id))
            con.commit()
            label = Label(root, text="Record updated",
                          font=10, width=25, bg="#90ff00")
            label.pack()

    def modify_parking_type_price():
        root = Toplevel()
        root.iconbitmap("converted1.ico")
        root.title("Parking Management System")

        header1 = Label(root, text="Modify Parking Type Price",
                        bg="Blue", fg="white", font=30, width=50)
        header1.pack(fill="both")

        b1 = Label(root, text="Enter parking type to be changed",
                   font=10, width=30)
        b1.pack(padx=10, pady=5)

        cursor.execute('select name from parking_type')
        parkingty = cursor.fetchall()
        rows = cursor.rowcount

        options1 = []
        for i in range(rows):
            a = parkingty[i]
            b = a[0]
            options1.append(b)

        clicked1 = StringVar()
        clicked1.set(options1[0])

        drop1 = OptionMenu(root, clicked1, *options1)
        drop1.pack(padx=10, pady=5)

        b2 = Label(root, text="Enter new price", font=10, width=25)
        b2.pack(padx=10, pady=5)

        e1 = Entry(root, borderwidth=5)
        e1.pack(padx=10, pady=5)

        submit = Button(root, text="SUBMIT", font=20, command=lambda: modify_parking_type_price_p(
            clicked1.get(), e1.get()), bg="#97ffff")
        submit.pack(padx=10, pady=5)

        def modify_parking_type_price_p(pos, value):
            cursor.execute(
                'select id from parking_type where name="{}";'.format(pos))
            id = cursor.fetchone()
            park_id = id[0]
            cursor.execute(
                'update parking_type set price={} where id={}'.format(value, park_id))
            con.commit()

            label = Label(root, text="Record updated",
                          font=10, width=25, bg="#90ff00")
            label.pack()


def modify_parking_space_record():

    w = Tk()
    w.iconbitmap("converted1.ico")
    w.title("Parking Management System")

    header = Label(w, text="What do you want to change",
                   bg="Blue", fg="white", font=30, width=50)
    header.pack(fill="both")

    btn1 = Button(w, text="Parking Type ID", bg="#97ffff", font=10,
                  width=25, command=lambda: modify_parking_id())
    btn1.pack(padx=10, pady=5)

    btn2 = Button(w, text="Status", bg="#97ffff", font=10,
                  width=25, command=lambda: modify_parking_status())
    btn2.pack(padx=10, pady=5)

    def modify_parking_id():
        root = Toplevel()
        root.iconbitmap("converted1.ico")
        root.title("Parking Management System")

        header1 = Label(root, text="Modify Parking Type ID",
                        bg="Blue", fg="white", font=30, width=50)
        header1.pack(fill="both")

        b1 = Label(root, text="Enter parking space ID", font=10, width=25)
        b1.pack(padx=10, pady=5)

        e1 = Entry(root, borderwidth=5)
        e1.pack()

        b2 = Label(root, text="Enter new parking type ID", font=10, width=25)
        b2.pack(padx=10, pady=5)

        e2 = Entry(root, borderwidth=5)
        e2.pack(padx=10, pady=5)

        submit = Button(root, text="SUBMIT", font=20, command=lambda: modify_parking_id_p(
            e1.get(), e2.get()), bg="#97ffff")
        submit.pack(padx=10, pady=5)

        def modify_parking_id_p(space_id, value):
            cursor.execute(
                'update parking_space set type_id={} where id={}'.format(value, space_id))
            con.commit()
            label = Label(root, text="Record updated",
                          font=10, width=25, bg="#90ff00")
            label.pack()

    def modify_parking_status():
        root = Toplevel()
        root.iconbitmap("converted1.ico")
        root.title("Parking Management System")

        header1 = Label(root, text="Modify Status", bg="Blue",
                        fg="white", font=30, width=50)
        header1.pack(fill="both")

        b1 = Label(root, text="Enter parking space ID", font=10, width=25)
        b1.pack(padx=10, pady=5)

        e1 = Entry(root, borderwidth=5)
        e1.pack()

        b2 = Label(root, text="Enter new status", font=10, width=25)
        b2.pack(padx=10, pady=5)

        clicked2 = StringVar()
        clicked2.set("open")

        drop2 = OptionMenu(root, clicked2, "open", "full")
        drop2.pack(padx=10, pady=5)

        submit = Button(root, text="SUBMIT", font=20, command=lambda: modify_parking_status_p(
            e1.get(), clicked2.get()), bg="#97ffff")
        submit.pack(padx=10, pady=5)

        def modify_parking_status_p(space_id, value):
            cursor.execute(
                'update parking_space set status="{}" where id={}'.format(value, space_id))
            con.commit()
            label = Label(root, text="Record updated",
                          font=10, width=25, bg="#90ff00")
            label.pack()


def add_new_vehicle():

    w = Toplevel()
    w.iconbitmap("converted1.ico")
    w.title("Parking Management System")

    header = Label(w, text="Vehicle Login", bg="Blue",
                   fg="white", font=30, width=50)
    header.pack(fill="both")

    b1 = Label(w, text="Enter vehicle number", font=10, width=25)
    b1.pack(padx=10, pady=5)

    e1 = Entry(w, borderwidth=5)
    e1.pack(padx=10, pady=5)

    b2 = Label(w, text="Enter parking type", font=10, width=25)
    b2.pack(padx=10, pady=5)

    cursor.execute('select name from parking_type')
    parkingty = cursor.fetchall()
    rows = cursor.rowcount

    options1 = []
    for i in range(rows):
        a = parkingty[i]
        b = a[0]
        options1.append(b)

    clicked1 = StringVar()
    clicked1.set(options1[0])

    drop1 = OptionMenu(w, clicked1, *options1)
    drop1.pack(padx=10, pady=5)

    b3 = Label(w, text="Enter space ID", font=10, width=25)
    b3.pack(padx=10, pady=5)

    cursor.execute("select id from parking_space where status='open'")
    parkingsp = cursor.fetchall()
    rows = cursor.rowcount

    options2 = []
    for i in range(rows):
        a = parkingsp[i]
        b = a[0]
        options2.append(b)

    clicked2 = IntVar()
    clicked2.set(options2[0])

    drop2 = OptionMenu(w, clicked2, *options2)
    drop2.pack(padx=10, pady=5)

    submit = Button(w, text="SUBMIT", font=20, command=lambda: v_login(
        e1.get(), clicked1.get(), clicked2.get()), bg="#97ffff")
    submit.pack(padx=10, pady=5)

    def v_login(vehicle_id, pos, parkingspaceid):
        cursor.execute(
            'select id from parking_type where name="{}";'.format(pos))
        id = cursor.fetchone()
        parkingtype_id = id[0]

        entry = time.time()
        sql = 'insert into transaction(vehicle_id,parkingtype_id,parkingspace_id,entry_time) values("{}",{},{},{})'.format(
            vehicle_id, parkingtype_id, parkingspaceid, entry)
        cursor.execute(sql)
        con.commit()
        cursor.execute(
            'update parking_space set status ="full" where id ={}'.format(parkingspaceid))
        cursor.execute('update parking_space set type_id={} where id={}'.format(
            parkingtype_id, parkingspaceid))
        con.commit()

        cursor.execute(
            'select id from transaction where vehicle_id="{}"'.format(vehicle_id))
        a = str(cursor.fetchone())
        b = str(a[1])

        confirmation = Label(w, text="vehicle id is "+b,
                             font=10, width=25, bg="#90ff00")
        confirmation.pack()


def remove_vehicle():

    w = Toplevel()
    w.iconbitmap("converted1.ico")
    w.title("Parking Management System")

    header = Label(w, text="Vehicle Logout", bg="Blue",
                   fg="white", font=30, width=50)
    header.pack(fill="both")

    b1 = Label(w, text="Enter vehicle ID", font=10, width=25)
    b1.pack(padx=10, pady=5)

    e1 = Entry(w, borderwidth=5)
    e1.pack(padx=10, pady=5)

    submit = Button(w, text="SUBMIT", font=20,
                    command=lambda: remove_vehicle_p(e1.get()), bg="#97ffff")
    submit.pack(padx=10, pady=5)

    def remove_vehicle_p(id):
        exit = time.time()
        cursor.execute(
            'select entry_time from transaction where id={}'.format(id))
        a = cursor.fetchone()
        entry = a[0]
        seconds = exit-entry
        minutes = seconds//60
        hours = minutes//60
        hours = +1
        cursor.execute(
            'select parkingtype_id from transaction where id={}'.format(id))
        a = cursor.fetchone()
        parkingtype = a[0]
        cursor.execute(
            'select price from parking_type where id={}'.format(parkingtype))
        a = cursor.fetchone()
        per = a[0]
        amount = int(per*hours)
        cursor.execute('update transaction set exit_time={},amount={} where id={}'.format(
            exit, amount, id))
        con.commit()
        cursor.execute(
            'select parkingspace_id from transaction where id={}'.format(id))
        a = cursor.fetchone()
        parkingspace = a[0]
        cursor.execute(
            'update parking_space set status="open" where id={}'.format(parkingspace))
        con.commit()

        amount_str = str(amount)
        confirmation = Label(w, text="The amount is " +
                             amount_str, font=10, width=25, bg="#90ff00")
        confirmation.pack()


def search_menu():

    menu = Tk()
    menu.iconbitmap("converted1.ico")
    menu.title("Parking Management System")

    header = Label(menu, text="Search Menu", bg="Blue",
                   fg="white", font=30, width=50)
    header.pack(fill="both")

    btn1 = Button(menu, text="Free Space", bg="#97ffff", font=10,
                  width=25, command=lambda: parking_status("open"))
    btn1.pack(padx=10, pady=5)

    btn2 = Button(menu, text="Ocupied Space", bg="#97ffff", font=10,
                  width=25, command=lambda: parking_status("full"))
    btn2.pack(padx=10, pady=5)

    btn4 = Button(menu, text="Money Collected", bg="#97ffff",
                  font=10, width=25, command=lambda: money_collected())
    btn4.pack(padx=10, pady=5)

    btn5 = Button(menu, text="Exit", bg="red", font=10,
                  width=25, command=menu.destroy)
    btn5.pack(padx=10, pady=5)

    def parking_status(status):
        sql = "select id from parking_space where status ='{}'".format(status)
        cursor.execute(sql)
        records = cursor.fetchall()
        list = []
        for row in records:
            confirmation = Label(
                menu, text=row[0], font=10, width=25, bg="#90ff00")
            confirmation.pack()

    def money_collected():
        money = 0
        cursor.execute(
            'select amount from transaction where amount is not null')
        a = cursor.fetchall()
        for i in a:
            money += i[0]

        confirmation = Label(menu, text=str(
            money), font=10, width=25, bg="#90ff00")
        confirmation.pack()


def main_menu():

    menu = Tk()
    menu.iconbitmap("converted1.ico")
    menu.title("Parking Management System")

    header = Label(menu, text="Main Menu", bg="Blue",
                   fg="white", font=30, width=50)
    header.pack(fill="both")

    btn1 = Button(menu, text="Vehicle Login", bg="#97ffff",
                  font=10, width=25, command=add_new_vehicle)
    btn1.pack(padx=10, pady=5)

    btn2 = Button(menu, text="Vehicle Logout", bg="#97ffff",
                  font=10, width=25, command=remove_vehicle)
    btn2.pack(padx=10, pady=5)

    btn3 = Button(menu, text="Search Menu", bg="#97ffff",
                  font=10, width=25, command=search_menu)
    btn3.pack(padx=10, pady=5)

    btn4 = Button(menu, text="Add New Parking Type", bg="#97ffff",
                  font=10, width=25, command=add_parking_type_record)
    btn4.pack(padx=10, pady=5)

    btn5 = Button(menu, text="Add New Parking Slot", bg="#97ffff",
                  font=10, width=25, command=add_parking_slot_record)
    btn5.pack(padx=10, pady=5)

    btn6 = Button(menu, text="Modify Parking Type Record", bg="#97ffff",
                  font=10, width=25, command=modify_parking_type_record)
    btn6.pack(padx=10, pady=5)

    btn7 = Button(menu, text="Modify Parking Slot Record", bg="#97ffff",
                  font=10, width=25, command=modify_parking_space_record)
    btn7.pack(padx=10, pady=5)

    btn8 = Button(menu, text="Close Application", bg="red",
                  font=10, width=25, command=menu.destroy)
    btn8.pack(padx=10, pady=5)


login_screen = Tk()

login_screen.title("Parking Management System")
login_screen.iconbitmap("converted1.ico")

# login
label1 = Label(login_screen, text="Enter Your Login Details",
               fg="white", bg="blue", font=30, width=50)
label1.pack(fill="both")

user_name = Label(login_screen, text="Enter you name", font=20)
user_name.pack(padx=10, pady=5)

enter_name = Entry(login_screen, borderwidth=5)
enter_name.pack(padx=10, pady=5)

user_passwd = Label(login_screen, text="Enter you password", font=20)
user_passwd.pack(padx=10, pady=5)

enter_passwd = Entry(login_screen, borderwidth=5)
enter_passwd.pack(padx=10, pady=5)

submit = Button(login_screen, text="SUBMIT",
                font=20, command=login, bg="#97ffff")
submit.pack(padx=10, pady=5)

login_screen.mainloop()
