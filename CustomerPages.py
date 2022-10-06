from os import X_OK
import tkinter as tk
from RequestPages import *
from tkinter import StringVar, messagebox, ttk
from Customers import *
from Admins import *

WIDTH = 500
HEIGHT = 350
HEIGHT2 = 500

class Login_Cust_Page(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self.title("Login the system")
        
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        tk.Label(self, text="Your User ID").pack()
        self.usrentry = tk.Entry(self, textvariable=self.username)
        self.usrentry.pack()
        tk.Label(self, text="password").pack()
        self.passentry = tk.Entry(self, textvariable=self.password)
        self.passentry.pack()

        tk.Button(self, text="Login", font=("Arial", 12), width=12, height=1, command=self.login).pack()

    def login(self):
        userid = self.username.get()
        password = self.password.get()

        result = Customer().login(userid, password)
        if result[1]:
            messagebox.showinfo("showinfo", result[0])
            self.call_next(userid)
        else:
            messagebox.showinfo("showinfo", result[0])
            self.usrentry.delete(0, tk.END)
            self.passentry.delete(0, tk.END)

    def call_next(self, userid):
        self.clear_widgets()
        Cust_Page(self, userid)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

class Register_Cust_Page(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self.master.title("Register Page")
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT2/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT2, x, y))

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.name = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.address = tk.StringVar()
        self.email = tk.StringVar()

        tk.Label(self, text="Your User ID").pack()
        self.usrentry = tk.Entry(self, textvariable=self.username)
        self.usrentry.pack()

        tk.Label(self, text="Password").pack()
        self.passentry = tk.Entry(self, textvariable=self.password)
        self.passentry.pack()

        tk.Label(self, text="Name").pack()
        self.namentry = tk.Entry(self, textvariable=self.name)
        self.namentry.pack()

        tk.Label(self, text="Gender").pack()
        self.gender = ttk.Combobox(self, width="10", values=("Female", "Male"))
        self.gender.pack()

        tk.Label(self, text="Phone Number").pack()
        self.phonentry = tk.Entry(self, textvariable=self.phone_number)
        self.phonentry.pack()

        tk.Label(self, text="address").pack()
        self.adressentry = tk.Entry(self, textvariable=self.address)
        self.adressentry.pack()

        tk.Label(self, text="Email").pack()
        self.emailentry = tk.Entry(self, textvariable=self.email)
        self.emailentry.pack()

        tk.Button(self, text="Register", font=("Arial", 12), width=15, height=1, command=self.register_user).pack()
        tk.Button(self, text="Close", font=("Arial", 12), width=15, height=1, command=self.close).pack()

    def close(self):
        self.destroy()

    def register_user(self):
        try:
            userid = self.username.get()
            password = self.password.get()
            name = self.name.get()
            gender = self.gender.get()
            number = self.phone_number.get()
            address = self.address.get()
            email = self.email.get()
            result = Customer().registration(userid, password, name, gender, number, address, email)
            if result[1]:
                messagebox.showinfo("showinfo", result[0])
                ###TODO add close
                self.close()
            else:
                messagebox.showwarning("showwarning", result[0])
        except:
            messagebox.showwarning("showwarning", "sth wrong")
        self.usrentry.delete(0, tk.END)
        self.passentry.delete(0, tk.END)
        self.namentry.delete(0, tk.END)
        self.gender.delete(0, tk.END)
        self.phonentry.delete(0, tk.END)
        self.emailentry.delete(0, tk.END)
        self.adressentry.delete(0, tk.END)

class Cust_Page(tk.Toplevel):
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.master = master
        self.userid = userid
        self.master.destroy()
        self.title("Customer Page")
        
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        tk.Button(self, text="Request", font=("Arial", 12), width=12, height=1, command=self.request).pack()
        tk.Button(self, text="All Items", font=("Arial", 12), width=12, height=1, command=self.allItems).pack()
        tk.Button(self, text="Search", font=("Arial", 12), width=12, height=1, command=self.search).pack()
    
    def request(self):
        Request_Page(self, self.userid)

    def allItems(self):
        See_items_buy(self, self.userid)
        
    def search(self):
        Search_Cust_Page(self, self.userid)

    def close(self):
        self.destroy()

class Search_Result_Page(tk.Toplevel):#After search page
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master

        result = self.master.results
        
        self.title('Search Result')

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT2/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT2, x, y))

        tv = ttk.Treeview(self, columns=(1, 2, 3, 4, 5), show = 'headings', height=8)

        tv.heading(1, text='Category')
        tv.heading(2, text='Model')
        tv.heading(3, text='Warranty')
        tv.heading(4, text='Price')
        tv.heading(4, text='Inventory Level')

        if self.master.searchby.get() == "Category":
            self.label7 = tk.Label(self, text="which model do you want").pack()
        elif self.master.searchby.get()== "Model":
            self.label7 = tk.Label(self, text="which category do you want").pack()
        else:
            print("no searchby")


        for i in range(len(result)):
            tv.insert(parent='', index=i, iid=i, values=result[i])
        tv.pack()

        self.MorC = StringVar()
        self.MorCentry = tk.Entry(self, textvariable = self.MorC)
        self.MorCentry.pack()

        tk.Button(self, text="Purchase", font=("Arial", 12), width=12, height=1, command=self.purchase).pack()

    def purchase(self):
        C = Customer()
        requirement = self.master.addfilter()
        requirement[self.master.searchby.get()] = self.master.searchvalue.get()
        if self.master.searchby.get() == "Category":
            requirement["Model"]= self.MorC.get()
        elif self.master.searchby.get()== "Model":
            requirement["Category"]= self.MorC.get()
            

        p = C.purchase(requirement)
        print(requirement)
        if p == None:
            messagebox.showwarning("showwarning", "No such item exists.")
        else:
            messagebox.showwarning("showwarning", str(p) + "is purchased by" + self.master.userid  )
            C.purchaseDB(p, self.master.userid)

class Search_Cust_Page(tk.Toplevel):#After customer page
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.master = master
        self.userid = userid
        self.title("Search Page")
        
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT2/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT2, x, y))

        tk.Label(self, text="Search your item", font=("Calibri", 20)).pack()

        self.label1 = tk.Label(self, text="Search By").pack()
        self.searchby = ttk.Combobox(self, width="10", values=("Category", "Model"))
        self.searchby.pack()

        self.label7 = tk.Label(self, text="Category/Model Name").pack()
        self.searchvalue = StringVar()
        self.searchvalueentry = tk.Entry(self, textvariable = self.searchvalue)
        self.searchvalueentry.pack()

        self.label2 = tk.Label(self, text="Color").pack()
        self.colors = ttk.Combobox(self, width="10", values=("White", "Black", "Green", "Yellow"))
        self.colors.pack()

        self.begin_year = StringVar()
        self.end_year = StringVar()
        self.begin_yearentry = tk.Entry(self, textvariable=self.begin_year)
        self.end_yearentry = tk.Entry(self, textvariable=self.end_year)
        self.label3 = tk.Label(self, text="Begin year").pack()
        self.begin_yearentry.pack()
        self.label4 = tk.Label(self, text="End year").pack()
        self.end_yearentry.pack()

        self.label2 = tk.Label(self, text="Factory").pack()
        self.factory = ttk.Combobox(self, width="10", values=("China", "Malaysia", "Philippines"))
        self.factory.pack()

        self.begin_price = StringVar()
        self.end_price = StringVar()
        self.begin_pricentry = tk.Entry(self, textvariable=self.begin_price)
        self.end_pricentry = tk.Entry(self, textvariable=self.end_price)
        self.label5 = tk.Label(self, text="Begin Price").pack()
        self.begin_pricentry.pack()
        self.label6 = tk.Label(self, text="End Price").pack()
        self.end_pricentry.pack()

        
        tk.Button(self, text="Search", font=("Arial", 12), width=11, height=1, command=self.showResult).pack()
        tk.Button(self, text="Exit", font=("Arial", 12), width=11, height=1, command=self.close).pack()
    
    def close(self):
        self.destroy()
    
    def addfilter(self):
        x ={}
        if self.colors.get() == "":
            x=x
        else:
            x["Color"]= self.colors.get()

        if self.begin_year.get() =="":
            x=x
        else:
            x["ProductionYear"]= {"$gte":self.begin_year.get()}

        if self.end_year.get() =="":
            x=x
        elif "ProductionYear" in x.keys():
            x["ProductionYear"]["$lte"]=self.end_year.get()
        else:
            x["ProductionYear"]= {"$lte":self.end_year.get()}

        if self.begin_price.get() =="":
            x=x
        else:
            x["Price"]= {"$gte":self.begin_price.get()}

        if self.end_price.get() =="":
            x=x
        elif "Price" in x.keys():
            x["Price"]["$lte"]=self.end_price.get()
        else:
            x["Price"]= {"$lte":self.end_price.get()}

        if self.factory.get() == "":
            x=x
        else:
            x["Factory"]=self.factory.get()

        self.filter = x
        return x

    def search(self):
        dic = self.addfilter()
        resultS = {}
        if self.searchby.get() == "Category" :
            resultS = Customer().C_categories_Search(self.searchvalue.get(), dic)
        else:
            resultS = Customer().C_models_Search(self.searchvalue.get(), dic)

        ans = []
        for key in resultS:
            attribute = []
            for i in key:
                if i != 'Cost':
                    attribute.append(key[i])
            ans.append(tuple(attribute))

        return ans

    def showResult(self):
        self.results = self.search()
        Search_Result_Page(self)
