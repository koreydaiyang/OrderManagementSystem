import tkinter as tk
from tkinter import Entry, StringVar, messagebox, ttk
from Customers import *
from Admins import *
from Request import *
from RequestPages import Request_Page

WIDTH = 500
HEIGHT = 350
HEIGHT2 = 500


class Login_Admin_Page(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self.title("Login the system as admin")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

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

        result = Administrator().login(userid, password)
        if result[1]:
            messagebox.showinfo("showinfo", result[0])
            self.call_search(userid)
        else:
            messagebox.showinfo("showinfo", result[0])
            self.usrentry.delete(0, tk.END)
            self.passentry.delete(0, tk.END)
        

    def call_search(self, userid):
        self.clear_widgets()
        Search_Admin_Page(self, userid)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        
class Register_Admin_Page(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self.master.title("Register Page")
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))


        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.name = tk.StringVar()
        self.phone_number = tk.StringVar()
        
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
        
        tk.Button(self, text="Register", font=("Arial", 12), width=15, height=1, command=self.register_user).pack()
        tk.Button(self, text="Close", font=("Arial", 12), width=15, height=1, command=self.close).pack()

    def close(self):
        self.destroy()

    def register_user(self):
        if self.checkcmbo():
            userid = self.username.get()
            password = self.password.get()
            name = self.name.get()
            gender = self.gender.get()
            number = self.phone_number.get()
            result = Administrator().registration(userid, password, name, gender, number)
            if result[1]:
                messagebox.showinfo("showinfo", result[0])
            else:
                messagebox.showwarning("showwarning", result[0])
        else:
            messagebox.showwarning("showwarning", "Plz fill all the box")
        self.usrentry.delete(0, tk.END)
        self.passentry.delete(0, tk.END)
        self.namentry.delete(0, tk.END)
        self.gender.delete(0, tk.END)
        self.phonentry.delete(0, tk.END)
        self.close()      

    def checkcmbo(self):
        if self.gender.get() == "Female":
            return "Female"
        elif self.gender.get() == "Male":
            return "Male"
        else:
            return False
    
class Search_Admin_Page(tk.Toplevel): #After Admin-Login
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.master = master
        self.userid = userid
        self.master.destroy()
        self.title("Admin Page")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        tk.Label(self, text="Administrator Management", font=("Calibri", 20)).pack()
        tk.Button(self, text="Search Items", font=("Arial", 12), width=20, height=1, command=self.search).pack()
        tk.Button(self, text="Display the sold items", font=("Arial", 12), width=20, height=1, command=self.display_items).pack()
        tk.Button(self, text="Items under service", font=("Arial", 12), width=20, height=1, command=self.under_service_items).pack()
        tk.Button(self, text="Customers with fee", font=("Arial", 12), width=20, height=1, command=self.customers_with_fee).pack()
        tk.Button(self, text="Exit", font=("Arial", 12), width=11, height=1, command=self.close).pack()

    def close(self):
        self.destroy()
    
    def search(self):
        Search_Admin_Page2(self, self.userid)

    def display_items(self):
        Display_Item_Page(self, self.userid)

    def under_service_items(self):
        Under_Service_Page(self, self.userid)
    
    def customers_with_fee(self):
        Customer_Fee_Page(self, self.userid)
      
class Display_Item_Page(tk.Toplevel):
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.userid = userid
        self.master = master
        self.title("Display the Items Page")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        tk.Label(self, text="Items Sold and Unsold", font=("Calibri", 20)).pack()
        table = ttk.Treeview(self)
        table["columns"] = ("IID", "Sold", "Unsold")
        table.column('#0', width=0, stretch=tk.NO)
        table.column('IID', anchor=tk.CENTER, width=100)
        table.column('Sold', anchor=tk.CENTER, width=100)
        table.column('Unsold', anchor=tk.CENTER, width=100)
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('IID', text='Product IID', anchor=tk.CENTER)
        table.heading('Sold', text='Sold', anchor=tk.CENTER)
        table.heading('Unsold', text='Unsold', anchor=tk.CENTER)

        values = Administrator().product_manage()
        for i in range(len(values)):
            table.insert(parent='', index=i, iid=i, text='', values=values[i])
        table.pack()
        tk.Button(self, text="Close", font=("Arial", 12), width=11, height=1, command=self.close).pack()
        # tk.Button(self, text="Search", font=("Arial", 12), width=11, height=1).pack()
        # tk.Button(self, text="Exit", font=("Arial", 12), width=11, height=1, command=self.close).pack()
    
    def close(self):
        self.destroy()

class Under_Service_Page(tk.Toplevel):
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.master = master
        self.userid = userid
        self.title("Display the Items Under Service")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT2/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT2, x, y))

        tk.Label(self, text="Items Sold and Unsold", font=("Calibri", 20)).pack()
        table = ttk.Treeview(self)
        table["columns"] = ("1", "2", "3", "4")
        table.column('#0', width=0, stretch=tk.NO)
        table.column('1', anchor=tk.CENTER, width=100)
        table.column('2', anchor=tk.CENTER, width=100)
        table.column('3', anchor=tk.CENTER, width=100)
        table.column('4', anchor=tk.CENTER, width=100)
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('1', text='Request ID', anchor=tk.CENTER)
        table.heading('2', text='Item ID', anchor=tk.CENTER)
        table.heading('3', text='Service Status', anchor=tk.CENTER)
        table.heading('4', text='Request Status', anchor=tk.CENTER)

        results = Administrator().items_under_service()
        for i in range(len(results)):
            table.insert(parent='', index=i, iid=i, text='', values=results[i])
        table.pack()
        #approve request
        tk.Label(self, text="Request id of request to approve", font=("Calibri", 10)).pack()
        self.request = tk.StringVar()
        self.requestentry = tk.Entry(self, textvariable=self.request)
        self.requestentry.pack()
        tk.Button(self, text="Approve", font=("Arial", 12), width=11, height=1, command=self.approve).pack()
        #serve request
        tk.Label(self, text="Request id of item to serve", font=("Calibri", 10)).pack()
        self.item = tk.StringVar()
        self.itementry = tk.Entry(self, textvariable=self.item)
        self.itementry.pack()
        tk.Button(self, text="Serve", font=("Arial", 12), width=11, height=1, command=self.serve).pack()
        tk.Button(self, text="Close", font=("Arial", 12), width=11, height=1, command=self.close).pack()
    
    def approve(self):
        requestid = self.request.get()
        mess = Request().approve(requestid, self.userid)
        messagebox.showinfo("showinfo", mess)
        self.requestentry.delete(0, tk.END)
    def serve(self):
        requestid = self.item.get()
        mess = Request().complete(requestid, self.userid)
        messagebox.showinfo("showinfo", mess)
        self.itementry.delete(0, tk.END)

    def close(self):
        self.destroy()

class Customer_Fee_Page(tk.Toplevel):
    def __init__(self, master, userid) -> None:
        super().__init__()
        self.master = master
        self.title("Display the Customer with Unpaid Fee")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        tk.Label(self, text="Customer with unpaid fee", font=("Calibri", 20)).pack()
        table = ttk.Treeview(self)
        table["columns"] = ("ID", "Name", "Fee")
        table.column('#0', width=0, stretch=tk.NO)
        table.column('ID', anchor=tk.CENTER, width=100)
        table.column('Name', anchor=tk.CENTER, width=100)
        table.column('Fee', anchor=tk.CENTER, width=100)
        table.heading('#0', text='', anchor=tk.CENTER)
        table.heading('ID', text='Customer ID', anchor=tk.CENTER)
        table.heading('Name', text='Name', anchor=tk.CENTER)
        table.heading('Fee', text='Fee Amount', anchor=tk.CENTER)

        results = Administrator().customers_with_fee_unpaid()
        for i in range(len(results)):
            table.insert(parent='', index=i, iid=i, text='', values=results[i][:3])
        table.pack()

        tk.Button(self, text="Close", font=("Arial", 12), width=11, height=1, command=self.close).pack()
    
    def close(self):
        self.destroy()
    
class Search_Admin_Page2(tk.Toplevel):
    def __init__(self, master, userid):
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

        self.labe21 = tk.Label(self, text="Search by ItemID, please leave the rest blank").pack()
        self.ItemID = StringVar()
        self.ItemIDentry = tk.Entry(self, textvariable = self.ItemID)
        self.ItemIDentry.pack()

        self.label1 = tk.Label(self, text="Search By").pack()
        self.searchby = ttk.Combobox(self, width="10", values=("Category", "Model", "ItemID"))
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

        
        tk.Button(self, text="Search", font=("Arial", 12), width=11, height=1, command=self.display).pack()
        tk.Button(self, text="Exit", font=("Arial", 12), width=11, height=1, command=self.close).pack()

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

        return x

    def search(self):
        A = Administrator()
        dic = self.addfilter()
        result = {}
        if self.searchby.get() == "Category" :
            result = A.A_categories_Search(self.searchvalue.get(), dic)
        elif self.searchby.get() == "Model":
            result = A.A_models_Search(self.searchvalue.get(), dic)
        else:
            result = A.A_ID_Search(self.ItemID.get(), dic)

        ans = ""
        for i in range(len(result)):
            ans += str(i) + '\n'
            for key in result[i]:
                ans += key + " : " + str(result[i][key]) +"\n"
            
        #anstext = tk.Label(self, text=ans, font=("Calibri", 10)).pack()
        #tk.Label(self, text=self.searchby.get(), font=("Calibri", 20)).pack()
        #print(dic)
        return result
    
    def display(self):
        self.results = self.search()
        Display_Search_Page(self)

    def close(self):
        return self.destroy()

class Display_Search_Page(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self.title("Display Search Results")

        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        result = self.master.results
        #tk.Label(self, text="test", font=("Calibri", 10)).pack()
        ans = ""
        for i in range(len(result)):
            ans += str(i+1) + ': \n'
            for key in result[i]:
                ans += key + " : " + str(result[i][key]) +"\n"
        tk.Label(self, text=ans, font=("Calibri", 15)).pack()
    
    def close(self):
        self.destroy()


        





