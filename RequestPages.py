import tkinter as tk
from tkinter import StringVar, messagebox, ttk
from Request import *

WIDTH = 500
HEIGHT = 350
HEIGHT2 = 500

class Request_Page(tk.Toplevel):
    def __init__(self, master, customerid) -> None:
        super().__init__()
        self.master = master
        self.customerid = customerid
        self.title("Request Page")
        
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        #Submit Request
        self.itemid = tk.StringVar()
        tk.Label(self, text="ID of item to submit request").pack()
        self.itemidentry = tk.Entry(self, textvariable=self.itemid)
        self.itemidentry.pack()
        tk.Button(self, text="Submit", font=("Arial", 12), width=12, height=1, command=self.submit).pack()
        #Cancel Request
        self.requestid = tk.StringVar()
        tk.Label(self, text="ID of request to cancel").pack()
        self.requestidentry = tk.Entry(self, textvariable=self.requestid)
        self.requestidentry.pack()
        tk.Button(self, text="Submit", font=("Arial", 12), width=12, height=1, command=self.cancel).pack()
        #tk.Button(self, text="Track my requests", font=("Arial", 12), width=12, height=1, command=self.track).pack()

        tv = ttk.Treeview(self, columns=(1, 2, 3, 4), show = 'headings', height=8)

        tv.column(1, anchor=tk.CENTER, width=100)
        tv.column(2, anchor=tk.CENTER, width=100)
        tv.column(3, anchor=tk.CENTER, width=100)
        tv.column(4, anchor=tk.CENTER, width=100)
        tv.heading(1, text='Request ID')
        tv.heading(2, text='Item ID')
        tv.heading(3, text='Service Status')
        tv.heading(4, text='Fee Amount')

        result = Request().track(int(self.customerid))
        for i in range(len(result)):
            tv.insert(parent='', index=i, iid=i, values=result[i])
        tv.pack()

    def submit(self):
        itemid = self.itemid.get()
        result = Request().submit_request(self.customerid, itemid)#ifwarranty need to be changed
        if result[0] == 0 or 1:
            messagebox.showinfo("showinfo", result[1])
            self.itemidentry.delete(0, tk.END)
        else:
            return result[1]
    
    def cancel(self):
        requestid = self.requestid.get()
        mess = Request().cancel(requestid, self.customerid)
        messagebox.showinfo("showinfo", mess)


class See_items_buy(tk.Toplevel):
    def __init__(self, master, customerid) -> None:
        super().__init__()
        self.master = master
        self.customerid = customerid
        self.title("All Items")
        
        wid_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (wid_screen/2) - (WIDTH/2)
        y = (height_screen/2) - (HEIGHT/2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        tv = ttk.Treeview(self, columns=(1, 2, 3, 4, 5), show = 'headings', height=8)

        tv.column(1, anchor=tk.CENTER, width=100)
        tv.column(2, anchor=tk.CENTER, width=100)
        tv.column(3, anchor=tk.CENTER, width=100)
        tv.column(4, anchor=tk.CENTER, width=100)
        tv.column(5, anchor=tk.CENTER, width=100)
        tv.heading(1, text='Item ID')
        tv.heading(2, text='Category')
        tv.heading(3, text='Model')
        tv.heading(4, text='Product ID')
        tv.heading(5, text='Purchase Date')
        result = Request().all_items(int(self.customerid))
        for i in range(len(result)):
            tv.insert(parent='', index=i, iid=i, values=result[i])
        tv.pack()

        tk.Button(self, text="Close", font=("Arial", 12), width=12, height=1, command=self.close).pack()

    def close(self):
        self.destroy()

#Request_Page(tk.Tk(), '1').mainloop()
#See_items_buy(tk.Tk(), '1').mainloop()