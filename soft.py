from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from reportlab.pdfgen import canvas
import datetime
import sqlite3
import win32api



def update_server():
    root1 = Tk()
    root1.title("update server")
    root1.geometry("600x600")
    root1.minsize(300, 100)
    root1.maxsize(400, 200)
    frame2 = Frame(root1, bg="light green")
    frame2.grid(row=20, column=20, padx=10, pady=10)
    tex = Label(frame2, text="SERVER UPDATE:")
    tex.grid(row=0, column=1, padx=100, pady=7)
    prodid = Label(frame2, text="product id:")
    prodid.grid(row=1, column=0)
    prodname = Label(frame2, text="product name:")
    prodname.grid(row=2, column=0)
    prodprice = Label(frame2, text="price:")
    prodprice.grid(row=3, column=0)
    prodstock = Label(frame2, text="Stock")
    prodstock.grid(row=4, column=0)

    global p_id_entry, p_name_entry, p_price_entry, p_stock_entry
    p_id_entry = Entry(frame2)
    p_id_entry.grid(row=1, column=1)
    p_name_entry = Entry(frame2)
    p_name_entry.grid(row=2, column=1)
    p_price_entry = Entry(frame2)
    p_price_entry.grid(row=3, column=1)
    p_stock_entry = Entry(frame2)
    p_stock_entry.grid(row=4, column=1)
    btn3 = Button(frame2, text="Update", font="baloobhai2 7 bold", command=update_data)
    btn3.grid(row=5, column=1)
    p_id_entry.bind('<Return>', lambda funct3: p_name_entry.focus())
    p_name_entry.bind('<Return>', lambda funct4: p_price_entry.focus())
    p_price_entry.bind('<Return>', lambda funct5: p_stock_entry.focus())
    p_stock_entry.bind("<Return>",returnstc)

    root1.mainloop()
    root1.destroy()

    return

def returnstc(entry=0):
    if (p_id_entry.get() != "" or p_name_entry.get() != "" or p_price_entry.get() != "" or p_stock_entry.get() != ""):
        update_data()
def update_data():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS product
                     (product_id text, product_name text, price real,stocks integer)''')
    products = [p_id_entry.get(), p_name_entry.get(), p_price_entry.get(), p_stock_entry.get()]
    sq_q = "INSERT INTO product VALUES (?,?,?,?)"
    c.executemany(sq_q, (products,))
    conn.commit()
    messagebox.showinfo("info", "value saved")
    conn.close()
    return


def search_box(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    global x
    x = e1.get()
    print(x)
    data = c.execute("SELECT product_id,product_name,price  FROM product WHERE product_name LIKE (?)", (f"%{x}%",))
    data = c.fetchall()
    print(data)
    results(data)
    c.close()
    return


def results(data):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    results_box.delete(0, END)
    j = 0
    c.execute(
        "CREATE TABLE IF NOT EXISTS selected (ind integer,product_id text,product_name text,price real,qty text,tick text)")
    for row in data:
        am = f"{row[0]}" + "                                         " + f"{row[1]}" + "                                    " + f"{row[2]}"
        results_box.insert(END, am)
        amx = (j, row[0], row[1], row[2], 0, "no")
        sq_q2 = "INSERT INTO selected VALUES  (?,?,?,?,?,?)"
        c.execute(sq_q2, amx)
        conn.commit()
        j = j + 1
        # results_box.bind('<Button-1>', selected)
        # results_box.insert(END,am)




    #
    # indset=0
    # results_box.bind("<Down>", lambda idx:downarrow(indset))
    # results_box.bind("<Up>",lambda idx:uparrow(indset))
    # conn.commit()

    c.close()
    return
# def searchdown(entry=0):
#     # lenbox = results_box.size()
#     results_box.selection_set(0)
#     results_box.focus()
#
# def uparrow(event,indset):
#     indset=indset+1
#     results_box.selection_set(indset)
#
#
# def downarrow(event,indset):
#     indset=indset-1
#     results_box.selection_set(indset)


def selected(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    i = results_box.curselection()
    sq_q3 = "UPDATE selected set tick = ? WHERE ind = ?"
    for value in i:
        vale = (str("yes"), int(value))
    c.executemany(sq_q3, (vale,))

    conn.commit()
    for value in i:
        valuex = value
    en4.bind('<Return>', ins_qty(valuex))
    results_box.delete(0, END)
    disp_val()
    c.close()
    return


def ins_qty(i):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()

    qty_val = (zx.get(), int(i))
    c.execute("UPDATE selected SET qty = ? WHERE ind = ?", (zx.get(), int(i)))
    conn.commit()
    c.close()
    return


def disp_val():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()

    temp = "yes"
    sel_val = c.execute("SELECT product_id,product_name,price,qty FROM selected WHERE tick = ?", (temp,))
    sel_val = c.fetchall()

    for row in sel_val:
        # col_add=(row[0],row[1],row[2],row[3])
        list_final.insert(parent='', index=END, text="",values=(row[0], row[1], row[2], row[3], int(row[2]) * int(row[3])))
        # atv=[(row[0],row[1],row[2],row[3],int(row[2])*int(row[3]))]

        c.execute(
            "CREATE TABLE IF NOT EXISTS finalbill(product_id text,product_name text,price real,qty text,t_val integer)")
        c.execute("INSERT INTO finalbill VALUES (?,?,?,?,?)",
                  (row[0], row[1], row[2], row[3], int(row[2]) * int(row[3])))
    conn.commit()
    c.execute("DROP TABLE selected")
    conn.close()
    return


def generatebill(entry=0):
    preview_box.delete(0, END)
    preview_box.insert(END,"                         "+"Welcome to  The Hunger taless", "\n")
    preview_box.insert(END, f"\n Bill Number :{B_no.get()}")
    preview_box.insert(END, f"\n Customer Name: {ent_n.get()}")
    preview_box.insert(END, f"\n Phone Number: {M_no.get()}")
    global xdt
    xdt = datetime.datetime.now()
    preview_box.insert(END, f"\n Date&Time: {xdt}")
    preview_box.insert(END, f"\n======================================================================")
    preview_box.insert(END,
                       "\n Id" + "                 " + "Product" + "             " + "Price" + "          " + "Qty" + "        " + "Final price")
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM finalbill")
    fi_bill = c.fetchall()

    c.execute("SELECT SUM(t_val) FROM finalbill")
    va1 = c.fetchall()
    c.execute("SELECT SUM(Qty) FROM finalbill")
    va2 = c.fetchall()
    for row in va1:
        global F_price
        F_price = StringVar(value=row[0])
    for row in va2:
        global I_count
        I_count = StringVar(value=row[0])
    global ent1
    ent1 = Entry(root, textvariable=F_price, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(250, 600, window=ent1)
    ent4 = Entry(root, textvariable=I_count, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(560, 650, window=ent4)
    global paid
    paid = StringVar(value=F_price.get())

    ent2 = Entry(root, textvariable=paid, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(560, 600, window=ent2)
    ent3 = Entry(root, textvariable=discount, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(250, 650, window=ent3)
    ent4 = Entry(root, textvariable=I_count, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(560, 650, window=ent4)

    conn.commit()
    for row in fi_bill:
        preview_box.insert(END,
                           "\n" + f"{row[0]}" + "                  " + f"{row[1]}" + "                 " + f"{row[2]}" + "          " + f"{row[3]}" + "          " + f"{row[4]}")
    # for row in list_final:
    #     preview_box.insert(END,"\n"+f"{row[0]}"+"              "+f"{row[1]}"+"               "+f"{row[2]}"+"               "+f"{row[3]}"+"               "+f"{row[4]}")

    preview_box.insert(END,
                       "\n" + " TOTAL PRICE:" + "                         " + f"Rs.{F_price.get()}")
    # if(paid.get()<F_price.get()):
    #     preview_box.insert(END, "\n"+" PAID:"+"                "+"                "+"        "+f"Rs.{paid.get()}")
    if (int(discount.get()) != 0):
        preview_box.insert(END,
                           "\n" + " DISCOUNT:" + "                        " + f"{discount.get()}%")

        a = (int(discount.get()) / 100) * int(F_price.get())
        preview_box.insert(END,
                           "\n" + " FINAL PRICE " + "                      "+ f"Rs.{int(F_price.get()) - a}")
    preview_box.insert(END, f"\n====================================================================")

    conn.commit()
    c.close()
    return


def invoice_bill(entry=0):
    pdf = canvas.Canvas(f"./bills/invo{B_no.get()}.pdf")
    pdf.setFont("Times-Roman", 25)
    pdf.drawString(250, 800, "INVOICE")
    pdf.line(230, 793, 380, 793)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(20, 760, "Vandana Store")
    pdf.drawString(20, 745, "Near Tehsil Sitapur")
    pdf.drawString(20, 730, "497111 Sarguja (C.G)")
    pdf.drawString(450, 775, f"Date:{datetime.datetime.now()}")
    pdf.drawString(450, 760, f"{ent_n.get()}")
    pdf.drawString(450, 745, f"{M_no.get()}")
    pdf.drawString(450, 730, f"Invoice No:{B_no.get()}")
    pdf.drawString(10, 697, "Id")
    pdf.drawString(80, 697, "Product")
    pdf.drawString(260, 697, "Price")
    pdf.drawString(390, 697, "qty")
    pdf.drawString(470, 697, "final price")
    pdf.line(0, 688, 830, 688)
    pdf.line(0, 710, 830, 710)
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM finalbill")
    xcx = c.fetchall()
    xtc = 670
    for rows in xcx:
        pdf.drawString(10, xtc, f"{rows[0]}")
        pdf.drawString(80, xtc, f"{rows[1]}")
        pdf.drawString(260, xtc, f"{rows[2]}")
        pdf.drawString(390, xtc, f"{rows[3]}")
        pdf.drawString(470, xtc, f"{rows[4]}")
        xtc = xtc - 15
    pdf.line(0, xtc, 830, xtc)
    pdf.drawString(30, xtc - 15, "Total cost:")
    pdf.drawString(300, xtc - 15, f"Rs.{ent1.get()}")
    pdf.drawString(30, xtc - 30, "Discount:")
    pdf.drawString(300, xtc - 30, f"{discount.get()}%")
    pdf.drawString(30, xtc - 45, "Final price:")
    a = (int(discount.get()) / 100) * int(ent1.get())
    pdf.drawString(300, xtc - 45, f"Rs.{int(ent1.get()) - a}")
    pdf.line(0, xtc - 60, 830, xtc - 60)
    pdf.drawString(240, xtc - 70, "Thank you For Shopping")
    conn.commit()
    c.close()

    pdf.showPage()
    pdf.save()


def Print_bill(entry=0):

    op = messagebox.askyesno("Print Bill", "Do you want to print the bill?")
    if op > 0:
        thermal = canvas.Canvas(f"./bills/{B_no.get()}.pdf",pagesize=(136.05,595.22))
        thermal.setFont("Times-Roman", 8)
        thermal.drawString(40, 580, "WELCOME")
        thermal.line(0, 576, 140,576)
        thermal.setFont("Helvetica", 6)
        thermal.drawString(5, 570, "The Hunger Tales")
        thermal.drawString(5, 560, "Tehsil road Sitapur")
        thermal.drawString(5, 550, "497111 Sarguja (C.G)")
        thermal.drawString(5, 540, f"Date:{datetime.datetime.now()}")
        thermal.drawString(5, 530, f"{ent_n.get()}")
        thermal.drawString(5, 520, f"{M_no.get()}")
        thermal.drawString(5, 510, f"Invoice No:{B_no.get()}")
        thermal.drawString(3, 498, "Id")
        thermal.drawString(30, 498, "Product")
        thermal.drawString(80, 498, "qty")
        thermal.drawString(110, 498, "final price")
        thermal.line(0, 505, 140, 505)
        thermal.line(0, 495, 140, 495)
        conn = sqlite3.connect('TC_billing.db')
        c = conn.cursor()
        c.execute("SELECT * FROM finalbill")
        xcx = c.fetchall()
        xtc = 490
        for rows in xcx:
            thermal.drawString(3, xtc, f"{rows[0]}")
            thermal.drawString(20, xtc, f"{rows[1]}")
            thermal.drawString(80, xtc, f"{rows[3]}")
            thermal.drawString(110, xtc, f"{rows[4]}")
            xtc = xtc - 10
            if(xtc<20):
                thermal.showPage()
                xtc=580
        thermal.line(0, xtc, 140, xtc)
        if (xtc < 20):
            thermal.showPage()
            xtc = 580
        thermal.drawString(10, xtc - 10, "Total cost:")
        thermal.drawString(80, xtc - 10, f"Rs.{ent1.get()}")
        if (xtc-10 < 20):
            thermal.showPage()
            xtc = 580
        thermal.drawString(10, xtc - 20, "Discount:")
        thermal.drawString(80, xtc - 20, f"{discount.get()}%")
        if (xtc-20 < 20):
            thermal.showPage()
            xtc = 580
        thermal.drawString(10, xtc - 30, "Final price:")
        a = (int(discount.get()) / 100) * int(ent1.get())
        thermal.drawString(80, xtc - 30, f"Rs.{int(ent1.get()) - a}")
        if (xtc-30 < 20):
            thermal.showPage()
            xtc = 580
        thermal.line(0, xtc - 40, 170, xtc - 40)
        if (xtc - 40 < 20):
            thermal.showPage()
            xtc = 580

        thermal.drawString(40, xtc - 50, "Thank you For Shopping")
        if (xtc - 50 < 20):
            thermal.showPage()
            xtc = 580
        thermal.drawString(40, xtc - 60, "Contact Us on +917905902625")
        conn.commit()
        c.close()

        thermal.showPage()
        thermal.save()
        # bill_data = preview_box.get(0, END)
        # f1 = open("bills/" + str(B_no.get()) + ".txt", "a")
        # for row in bill_data:
        #     f1.write(str(row))
        # f1.close()
        messagebox.showinfo("Saved", f"Bill no.:{B_no.get()} saved successfully")
        billfile = f"E:\\the hunger tales\\bills\{str(B_no.get())}.pdf"
        win32api.ShellExecute(0, "print", billfile, None, ".", 0)
        conn = sqlite3.connect('TC_billing.db')
        c = conn.cursor()
        c.execute("SELECT bno FROM billno")
        bxx = c.fetchall()
        for row in bxx:
            bxx2 = row[0] + 1
            c.execute("UPDATE billno SET bno = (?) WHERE idx = 0", (bxx2,))
            print(bxx2)
        c.execute("SELECT product_id , product_name , qty FROM finalbill")
        qt = c.fetchall()
        for row in qt:
            c.execute(f"UPDATE product SET stocks = stocks-{row[2]} WHERE product_id = ?", (row[0],))
            conn.commit()
        c.execute(
            "CREATE TABLE IF NOT EXISTS history (Bill_no integer,Date text,Customer_name text,Mobile_no integer,product_count integer,total_price real,discount integer,paid real,unpaid real)")
        xt = int((int(discount.get()) / 100) * int(F_price.get()))
        hist = (B_no.get(), str(xdt.strftime("%x")), ent_n.get(), M_no.get(), I_count.get(), F_price.get(), discount.get(),
                paid.get(), int(F_price.get()) - xt - int(paid.get()))
        c.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?,?,?)", (hist))

        conn.commit()
        c.close()
        clear_data()
    else:
        return


def clear_data(entry=0):

    preview_box.delete(0, END)
    for record in list_final.get_children():
        list_final.delete(record)
    zx.set(1)
    M_no.set("")
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT bno FROM billno")
    bnx=c.fetchall()
    for row in bnx:
        B_no.set(row[0])
    bn()
    global F_price
    F_price.set("")
    global I_count
    I_count.set("")
    discount.set(0)
    global paid
    paid.set("")
    c.execute("DROP TABLE finalbill")
    c.execute("DROP TABLE selected")
    conn.commit()
    c.close()
# -------------------------------------Menu Functions----------------------------------------------

# -----------------------------------------product database--------------------------------------------
def product_base(entry=0):
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Product Database")

    global lbox
    lbox = ttk.Treeview(root2)
    lbox.pack(fill=BOTH)
    lbox['columns'] = ("ID", "Name", "Price", "Stocks")
    # formate our columns
    lbox.column("#0", width=0)
    lbox.column("ID", anchor=W, width=120)
    lbox.column("Name", anchor=CENTER, width=120)
    lbox.column("Price", anchor=W, width=120)
    lbox.column("Stocks", anchor=W, width=120)

    #
    # create headings
    lbox.heading("#0", text="", anchor=W)
    lbox.heading("ID", text="ID", anchor=W)
    lbox.heading("Name", text="Name", anchor=CENTER)
    lbox.heading("Price", text="Price", anchor=W)
    lbox.heading("Stocks", text="Qty", anchor=W)
    for record in lbox.get_children():
        lbox.delete(record)
    disp_ent()

    idl = Label(root2, text="Id of product to deleted:")
    idl.pack()
    global entx
    entx = Entry(root2)
    entx.pack(pady=5)
    bt = Button(root2, text="Delete Entry", font="baloobhai2 10 bold", bg="sky blue")
    bt.pack(pady=5)
    btx = Button(root2, text="Delete All", font="baloobhai2 10 bold", bg="sky blue")
    btx.pack(pady=10)
    bt.bind("<Button-1>", delid)
    btx.bind("<Button-1>", delall)
    root2.mainloop()


def disp_ent():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM product")
    llist = c.fetchall()
    for row in llist:
        lbox.insert(parent="", index=END, text="", values=(row[0], row[1], row[2], row[3]))
    conn.commit()
    c.close()


def delid(entry=0):
    conn = sqlite3.connect("TC_billing.db")
    c = conn.cursor()
    c.execute("DELETE FROM product WHERE product_id = ?", (entx.get(),))
    conn.commit()
    c.close
    for record in lbox.get_children():
        lbox.delete(record)
    disp_ent()


def delall(entry=0):
    conn = sqlite3.connect("TC_billing.db")
    c = conn.cursor()
    c.execute("DELETE FROM product")
    conn.commit()
    c.close
    for record in lbox.get_children():
        lbox.delete(record)
    disp_ent()


# ---------------------------------------------------STOCKS---------------------------------------------

def stks():
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Stocks")
    global lbox1
    lbox1 = ttk.Treeview(root2)
    lbox1.pack(fill=BOTH)
    lbox1['columns'] = ("ID", "Name", "Price", "Stocks")
    lbox1.column("#0", width=0)
    lbox1.column("ID", anchor=W, width=120)
    lbox1.column("Name", anchor=CENTER, width=120)
    lbox1.column("Price", anchor=W, width=120)
    lbox1.column("Stocks", anchor=W, width=120)

    #
    # create headings
    lbox1.heading("#0", text="", anchor=W)
    lbox1.heading("ID", text="ID", anchor=W)
    lbox1.heading("Name", text="Name", anchor=CENTER)
    lbox1.heading("Price", text="Price", anchor=W)
    lbox1.heading("Stocks", text="Qty", anchor=W)
    for record in lbox1.get_children():
        lbox1.delete(record)
    disp_stck()

    idl = Label(root2, text="Id of product stock to be added:")
    idl.pack()
    global entx2
    entx2 = Entry(root2)
    entx2.pack(pady=5)
    stockl = Label(root2, text="qty of product to be added")
    stockl.pack(pady=5)
    global entx3
    entx3 = Entry(root2)
    entx3.pack(pady=5)
    bt = Button(root2, text="save entered stock", font="baloobhai2 10 bold", bg="sky blue")
    bt.pack(pady=5)
    bt.bind("<Button-1>", save_stck)

    root2.mainloop()


def disp_stck():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM product ORDER BY stocks ")
    llist = c.fetchall()
    for row in llist:
        lbox1.insert(parent="", index=END, text="", values=(row[0], row[1], row[2], row[3]))
    conn.commit()
    c.close()


def save_stck(entry=0):
    conn = sqlite3.connect("TC_billing.db")
    c = conn.cursor()
    c.execute(f"UPDATE product SET stocks = stocks+{entx3.get()} WHERE product_id = ?", (entx2.get(),))
    conn.commit()
    c.close
    for record in lbox1.get_children():
        lbox1.delete(record)
    disp_stck()


# -----------------------------------------billing history---------------------------------------------
def billhist():
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Billing History")
    global lbox2
    lbox2 = ttk.Treeview(root2)
    lbox2.pack(fill=BOTH)
    lbox2['columns'] = (
    "Billno", "date", "name", "mob.no.", "product_count", "Total_Price", "discount", "paid", "unpaid")
    lbox2.column("#0", width=0)
    lbox2.column("Billno", anchor=W, width=120)
    lbox2.column("date", anchor=CENTER, width=120)
    lbox2.column("name", anchor=W, width=120)
    lbox2.column("mob.no.", anchor=W, width=120)
    lbox2.column("product_count", anchor=W, width=120)
    lbox2.column("Total_Price", anchor=W, width=120)
    lbox2.column("discount", anchor=W, width=120)
    lbox2.column("paid", anchor=W, width=120)
    lbox2.column("unpaid", anchor=W, width=120)
    #
    # create headings
    lbox2.heading("#0", text="", anchor=W)
    lbox2.heading("Billno", text="Bill.No.", anchor=W)
    lbox2.heading("date", text="Date&Time", anchor=CENTER)
    lbox2.heading("name", text="Name", anchor=W)
    lbox2.heading("mob.no.", text="Mob No.", anchor=W)
    lbox2.heading("product_count", text="Product count", anchor=W)
    lbox2.heading("Total_Price", text="Total Price", anchor=W)
    lbox2.heading("discount", text="discount", anchor=W)
    lbox2.heading("paid", text="paid", anchor=W)
    lbox2.heading("unpaid", text="unpaid", anchor=W)
    for record in lbox2.get_children():
        lbox2.delete(record)
    disp_hist()

    idl = Label(root2, text="Search by name:")
    idl.pack()
    global entxo
    entxo = Entry(root2)
    entxo.pack(pady=5)
    # stockl = Label(root2, text="qty of product to be added")
    # stockl.pack(pady=5)
    # global entx3
    # entx3 = Entry(root2)
    # entx3.pack(pady=5)
    bt2 = Button(root2, text="Search", font="baloobhai2 10 bold", bg="sky blue")
    bt2.pack(pady=5)
    bt2.bind("<Button-1>", search_hist)
    entxo.bind("<Return>", search_hist)
    bt4 = Button(root2, text="Clear search", font="baloobhai2 10 bold", bg="sky blue")
    bt4.pack(pady=5)
    bt4.bind("<Button-1>", clear_se_hist)

    root2.mainloop()


def clear_se_hist(entry=0):
    for record in lbox2.get_children():
        lbox2.delete(record)
    disp_hist()


def search_hist(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    for record in lbox2.get_children():
        lbox2.delete(record)
    print("check1")
    c.execute(
        "SELECT * FROM history WHERE Customer_name LIKE (?)",
        (f"%{entxo.get()}%",))
    llist = c.fetchall()
    print("check2")
    for row in llist:
        lbox2.insert(parent="", index=END, text="",
                     values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    print("check3")
    conn.commit()
    c.close()


def disp_hist():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY Bill_no DESC")
    llist = c.fetchall()
    for row in llist:
        lbox2.insert(parent="", index=END, text="",
                     values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    conn.commit()
    c.close()


# ==============================================Sales============================================================
def billsale():
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Sales")
    global lbox3
    lbox3 = ttk.Treeview(root2)
    lbox3.pack(fill=BOTH)
    lbox3['columns'] = ("date", "total_sale")
    lbox3.column("#0", width=0)
    lbox3.column("date", anchor=W, width=120)
    lbox3.column("total_sale", anchor=CENTER, width=120)
    #
    # create headings
    lbox3.heading("#0", text="", anchor=W)
    lbox3.heading("date", text="date", anchor=W)
    lbox3.heading("total_sale", text="total sale", anchor=CENTER)
    for record in lbox3.get_children():
        lbox3.delete(record)
    disp_sale()

    idl = Label(root2, text="Search by date:")
    idl.pack()
    global entxo1
    entxo1 = Entry(root2)
    entxo1.pack(pady=5)
    # stockl = Label(root2, text="qty of product to be added")
    # stockl.pack(pady=5)
    # global entx3
    # entx3 = Entry(root2)
    # entx3.pack(pady=5)
    bt2 = Button(root2, text="Search", font="baloobhai2 10 bold", bg="sky blue")
    bt2.pack(pady=5)
    bt2.bind("<Button-1>", search_sale)
    entxo1.bind("<Return>", search_sale)
    bt4 = Button(root2, text="Clear search", font="baloobhai2 10 bold", bg="sky blue")
    bt4.pack(pady=5)
    bt4.bind("<Button-1>", clear_se_sale)

    root2.mainloop()


def clear_se_sale(entry=0):
    for record in lbox3.get_children():
        lbox3.delete(record)
    disp_sale()


def search_sale(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    for record in lbox3.get_children():
        lbox3.delete(record)
    print("check1")
    c.execute(
        "SELECT Date,SUM(total_price) FROM history WHERE Date LIKE (?)",
        (f"%{entxo1.get()}%",))
    llist = c.fetchall()
    print("check2")
    for row in llist:
        lbox3.insert(parent="", index=END, text="", values=(row[0], row[1]))
    print("check3")
    conn.commit()
    c.close()


def disp_sale():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT date,SUM(total_price) FROM history GROUP BY Date ")
    llist = c.fetchall()
    for row in llist:
        lbox3.insert(parent="", index=END, text="",
                     values=(row[0], row[1]))
    conn.commit()
    c.close()


# =============================================================borrow=============================================
def billborrow():
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Borrow Account")
    global lbox4
    lbox4 = ttk.Treeview(root2)
    lbox4.pack(fill=BOTH)
    lbox4['columns'] = ("name", "unpaid", "bill_no", "mobileNo")
    lbox4.column("#0", width=0)
    lbox4.column("name", anchor=W, width=120)
    lbox4.column("unpaid", anchor=CENTER, width=120)
    lbox4.column("bill_no", anchor=CENTER, width=120)
    lbox4.column("mobileNo", anchor=CENTER, width=120)
    #
    # create headings
    lbox4.heading("#0", text="", anchor=W)
    lbox4.heading("name", text="Name", anchor=W)
    lbox4.heading("unpaid", text="Unpaid", anchor=CENTER)
    lbox4.heading("bill_no", text="Bill_no", anchor=CENTER)
    lbox4.heading("mobileNo", text="Mobile_No", anchor=CENTER)
    for record in lbox4.get_children():
        lbox4.delete(record)
    disp_borrow()

    idl = Label(root2, text="Search by name:")
    idl.pack()
    global entxo2
    entxo2 = Entry(root2)
    entxo2.pack(pady=5)
    # stockl = Label(root2, text="qty of product to be added")
    # stockl.pack(pady=5)
    # global entx3
    # entx3 = Entry(root2)
    # entx3.pack(pady=5)
    bt2 = Button(root2, text="Search", font="baloobhai2 10 bold", bg="sky blue")
    bt2.pack(pady=5)
    bt2.bind("<Button-1>", search_borrow)
    entxo2.bind("<Return>", search_borrow)
    bt4 = Button(root2, text="Clear search", font="baloobhai2 10 bold", bg="sky blue")
    bt4.pack(pady=5)
    bt4.bind("<Button-1>", clear_se_borrow)

    root2.mainloop()


def clear_se_borrow(entry=0):
    for record in lbox4.get_children():
        lbox4.delete(record)
    disp_borrow()


def search_borrow(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    for record in lbox4.get_children():
        lbox4.delete(record)
    print("check1")
    c.execute(
        "SELECT Customer_name,unpaid,Bill_no,Mobile_no FROM history WHERE Customer_name LIKE (?)",
        (f"%{entxo2.get()}%",))
    llist = c.fetchall()
    print("check2")
    for row in llist:
        lbox4.insert(parent="", index=END, text="", values=(row[0], row[1],row[2],row[3]))
    print("check3")
    conn.commit()
    c.close()


def disp_borrow():
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()
    c.execute("SELECT Customer_name,unpaid,Bill_no,Mobile_no FROM history WHERE unpaid != 0 ")
    llist = c.fetchall()
    for row in llist:
        lbox4.insert(parent="", index=END, text="",
                     values=(row[0], row[1],row[2],row[3]))
    conn.commit()
    c.close()


# --------------------------------------------------main program---------------------------------------


canvas_width = 1355
canvas_height = 1000
root = Tk()
root.title("BILLING SOFTWARE")
root.geometry("1255x900")
can_widget = Canvas(root, width=canvas_width, height=canvas_height)
can_widget.pack()
can_widget.configure(background="Royalblue2")
conn = sqlite3.connect('TC_billing.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS billno (bno integer,idx integer)")
# c.execute("SELECT bno FROM billno")
# boox = c.fetchall()
# for row in boox:
#     if (row[0]>1):
#         break
#     else:
#         c.execute("INSERT INTO billno (bno,idx) VALUES(1,0)")
conn.commit()
c.close()

# BG IMAGE
# image1 = Image.open("11.jpg")
# photo1 = ImageTk.PhotoImage(image1)
# can_widget.create_image(100, 100, image=photo1)
# bg2 = Label(root,image=photo1)
# bg2.pack(fill=BOTH)
# heading
# hed = Label(bg2,text="BILLING SOFTWARE",bg="",font="baloobhai2 30 bold",fg="black")
# hed.grid(row=0,column=0,padx=500,pady=4)
image2 = Image.open("./res/logofnl.png").resize((200,120))
photo2 = ImageTk.PhotoImage(image2)
can_widget.create_image(400, 50, image=photo2)
can_widget.create_text(640, 40, text="THE HUNGER", font="baloobhai2 30 bold", fill="black")
can_widget.create_text(850, 40, text="TALES", font="baloobhai2 30 bold", fill="black")
image3 = Image.open("./res/final.png").resize((120,120))
photo3 = ImageTk.PhotoImage(image3)
can_widget.create_image(1230, 40, image=photo3)
can_widget.create_text(1230, 60, text="Developed by Creative phoenix Technologies", font="baloobhai2 8 bold", fill="Red2")
can_widget.create_line(1, 80, 10000, 80, fill="white")
can_widget.create_line(1, 75, 10000, 75, fill="white")
e1 = Entry(can_widget)
can_widget.create_window(350, 100, window=e1, width=600, height=30, )
e1.focus()
btn1 = Button(can_widget, text="Search", bg="white", font="baloobhai 15 bold", fg="blue", command=search_box)
can_widget.create_window(720, 100, window=btn1, width=100, height=30)
can_widget.create_line(800, 80, 800, 1000, fill="white")
can_widget.create_line(805, 80, 805, 1000, fill="white")
#==============================================================================custn=================================================
def custn(entry=0):
    conn = sqlite3.connect('TC_billing.db')
    c = conn.cursor()

    c.execute("SELECT Customer_name FROM history WHERE Mobile_no = (?)", (f"{ent_mn.get()}",))
    name = c.fetchall()
    if len(name)==0:
        print("no match")
        C_name=" "
    else:
        global mname
        for row in name:
            print(row[0])
            mname=row[0]
        print(mname)
        C_name = StringVar(value=mname)
    global ent_n
    ent_n = Entry(root, textvariable=C_name, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(1090, 130, window=ent_n, width=250)
    conn.commit()
    c.close()
#====================================bn==================================================
def bn(entry=0):
    conn = sqlite3.connect("TC_billing.db")
    c = conn.cursor()
    c.execute("SELECT bno FROM billno WHERE idx = 0")
    bno = c.fetchall()
    # global Bn
    for row in bno:
        print(row[0])
        Bn = row[0]
    print(Bn)
    global B_no
    B_no = StringVar(value=Bn)
    global ent_bn
    ent_bn = Entry(root, textvariable=B_no, bg="white", borderwidth=3, relief=SUNKEN)
    can_widget.create_window(1090, 160, window=ent_bn, width=250)
    c.execute("UPDATE billno SET bno = (?) WHERE idx = 0",(ent_bn.get(),))

    conn.commit()
    c.close()

# -------------------------------------------MENU---------------------------------------------------
menubar = Menu(root)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label=" Product Database", command=product_base)
menu1.add_command(label="Stocks", command=stks)
menu1.add_command(label="Billing History", command=billhist)
menu1.add_command(label="Sales", command=billsale)
menu1.add_command(label="Borrowing Accounts", command=billborrow)
menu1.add_separator()
menu1.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=menu1)
root.config(menu=menubar)
menubar.config(bg="gray", bd=6, font="helvetica 10 bold", relief=SUNKEN)

# results_box.bind('<Button-1>', selected)
# searchn=Label(root,text=("item search"))
# searchn.pack()
# searchval = StringVar()
# searchentry = Entry(root,textvariable=searchval)
# searchentry.pack()
btn2 = Button(can_widget, text="Update Server", bg="white", font="baloobhai 9 bold", fg="blue", command=update_server)
can_widget.create_window(100, 30, window=btn2, width=100, height=30)

results_box = Listbox(can_widget)
can_widget.create_window(350, 158, window=results_box, width=600, height=100)
scroll_a = Scrollbar(results_box)
scroll_a.pack(side=RIGHT, fill=Y)
scroll_a.config(command=results_box.yview)
results_box.bind('<<ListboxSelect>>', selected)

list_final = ttk.Treeview(can_widget)
can_widget.create_window(350, 400, window=list_final, width=600, height=300)
list_final['columns'] = ("ID", "Name", "Price", "Qty", "t_price")
# formate our columns
list_final.column("#0", width=0)
list_final.column("ID", anchor=W, width=120)
list_final.column("Name", anchor=CENTER, width=120)
list_final.column("Price", anchor=W, width=120)
list_final.column("Qty", anchor=W, width=120)
list_final.column("t_price", anchor=W, width=120)
#
# create headings
list_final.heading("#0", text="", anchor=W)
list_final.heading("ID", text="ID", anchor=W)
list_final.heading("Name", text="Name", anchor=CENTER)
list_final.heading("Price", text="Price", anchor=W)
list_final.heading("Qty", text="Qty", anchor=W)
list_final.heading("t_price", text="Total_price", anchor=W)

scroll_b = Scrollbar(list_final)
scroll_b.pack(side=RIGHT, fill=Y)
scroll_b.config(command=list_final.yview)

l4 = Label(can_widget, text="qty")
can_widget.create_window(600, 100, window=l4)
zx = StringVar(value=1)
en4 = Entry(can_widget, textvariable=zx)
can_widget.create_window(630, 100, window=en4, height=20, width=20)

# labels

lab1 = Label(can_widget, text="Final Price:", font="baloobhai2 9 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(100, 600, window=lab1, width=80, height=30)
lab2 = Label(can_widget, text="Paid:", font="baloobhai2 9 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(420, 600, window=lab2, width=80, height=30)
lab3 = Label(can_widget, text="Discount:", font="baloobhai2 9 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(100, 650, window=lab3, width=80, height=30)
lab4 = Label(can_widget, text="Items Count:", font="baloobhai2 9 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(420, 650, window=lab4, width=80, height=30)
# variables
discount = StringVar(value=0)

# ---------------------------customer details---------------------------------
lab_name = Label(can_widget, text="Customer Name:", font="baloobhai2 10 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(870, 130, window=lab_name)
lab_pn = Label(can_widget, text="Mobile No:", font="baloobhai2 10 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(870, 100, window=lab_pn, width=115, height=21)
lab_bnm = Label(can_widget, text="Bill Number:", font="baloobhai2 10 bold", bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(870, 160, window=lab_bnm, width=115)


M_no = StringVar()
ent_mn = Entry(root, textvariable=M_no, bg="white", borderwidth=3, relief=SUNKEN)
can_widget.create_window(1090, 100, window=ent_mn, width=250)
custn()
ent_mn.bind("<Return>",custn)
bn()
# ----------------------bill preview----------------------------
bill_preview = Label(can_widget, text="Bill Preview", fg="black", bg="white", font="baloobhai2 20 bold", borderwidth=5,
                     relief=SUNKEN)
can_widget.create_window(1030, 210, window=bill_preview, width=330)
preview_box = Listbox(can_widget)
can_widget.create_window(1030, 400, window=preview_box, width=330, height=350)

# ----------------------------btns----------------------------------------------


genbill = Button(can_widget, text="Gen. Bill", font="baloobhai2 10 bold", fg="blue", borderwidth=6, relief=SUNKEN)
can_widget.create_window(950, 600, window=genbill, width=100, height=30)
invoicebill = Button(can_widget, text="Invoice", font="baloobhai2 10 bold", fg="blue", borderwidth=6, relief=SUNKEN)
can_widget.create_window(1150, 600, window=invoicebill, width=100, height=30)
printbill = Button(can_widget, text="Print", font="baloobhai2 10 bold", fg="blue", borderwidth=6, relief=SUNKEN)
can_widget.create_window(950, 650, window=printbill, width=100, height=30)
clearbill = Button(can_widget, text="Clear", font="baloobhai2 10 bold", fg="blue", borderwidth=6, relief=SUNKEN)
can_widget.create_window(1150, 650, window=clearbill, width=100, height=30)

genbill.bind("<Button-1>", generatebill)
printbill.bind("<Button-1>", Print_bill)
clearbill.bind("<Button-1>", clear_data)
invoicebill.bind("<Button-1>", invoice_bill)

#==============================================================bindings================================================

e1.bind('<Return>', search_box)
# e1.bind("<Down>",searchdown)
e1.bind('<KeyRelease-Return>',lambda funct1:en4.focus())

root.mainloop()
