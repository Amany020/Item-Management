''' Item management system project in python using Tkinter and MySQL Database'''
from functools import partial
from tkinter import *
from tkinter import ttk, messagebox
from turtle import width
import pymysql
import custom as cs
import credentials as cr


class Management:
    def __init__(self, root):
        self.window = root
        self.window.title("Item Management System")
        self.window.geometry("1500x600")
        self.window.config(bg = "white")
        
        # Customization
        self.color_1 = cs.color_1
        self.color_2 = cs.color_2
        self.color_3 = cs.color_3
        self.color_4 = cs.color_4
        self.color_5=cs.color_5
        self.font_1 = cs.font_1
        self.font_2 = cs.font_2
        self.columns = cs.columns

        # User Credentials
        self.host = cr.host
        self.user = cr.user
        self.password = cr.password
        self.database = cr.database

        # Left Frame
        self.frame_1 = Frame(self.window, bg=cs.color_1)
        self.frame_1.place(x=0, y=0, width=740, relheight = 1)
        self.label_1=Label(self.frame_1,text="ITEM MANAGEMENT SYSTEM ",bg="white",fg="black",font=("Times", 30))
        self.label_1.place(x=10,y=20)
        # Right Frame
        self.frame_2 = Frame(self.window, bg = cs.color_2)
        self.frame_2.place(x=740,y=0,relwidth=1, relheight=1)

        # Buttons
        self.add_new_bt = Button(self.frame_2, text='Add Item', font=(cs.font_1, 12), bd=2, command=self.AddRecord,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=40,width=100)
        self.display_bt = Button(self.frame_2, text='Display Item', font=(cs.font_1, 12), bd=2, command=self.DisplayRecords, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=100,width=100)
        self.search_bt = Button(self.frame_2, text='Search Item', font=(cs.font_1, 12), bd=2, command=self.GetItem_to_Search,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=160,width=100)
        self.clear_bt = Button(self.frame_2, text='Clear', font=(cs.font_1, 12), bd=2, command=self.ClearScreen,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=340,width=100)
        self.exit_bt = Button(self.frame_2, text='Exit', font=(cs.font_1, 12), bd=2, command=self.Exit, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=400,width=100)
        
        self.delete_bt = Button(self.frame_2, text='Delete Item', font=(self.font_1, 12), bd=2, command=self.Getitem_Delete, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=280,width=100)
        self.update_bt = Button(self.frame_2, text='Update Item', font=(self.font_1, 12), bd=2, command=self.Getitem_Update, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=220,width=100)
    '''This function displays all the item records from the database'''
    def DisplayRecords(self):
        self.ClearScreen()
        # Defining two scrollbars
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_1, columns=self.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        # vertical scrollbar: left side
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        # Horizontal scrollbar: at bottom
        scroll_x.pack(side=BOTTOM, fill=X)

        # Table headings
        self.tree.heading('Item_Name', text='Item Name', anchor=W)
        self.tree.heading('Item_Price', text='Item Price', anchor=W)
        self.tree.heading('Item_Quantity', text='Quantity', anchor=W)
        self.tree.heading('Item_Category', text='Category', anchor=W)
        self.tree.heading('Discount', text='Discount', anchor=W)
        self.tree.pack()
       

        try:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            curs = connection.cursor()
            curs.execute("select * from item_register")
            rows=curs.fetchall()
            if rows == None:
                messagebox.showinfo("Database Empty","There is no data to show",parent=self.window)
                connection.close()
                self.ClearScreen()
            else:
                connection.close()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
        # Inserting row values
        for list in rows:
            self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4]))
      
        

       
    '''It displays all the matched items searched by the user'''
    def ShowRecords(self, rows):
        self.ClearScreen()
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_1, columns=self.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        scroll_x.pack(side=BOTTOM, fill=X)

        # Table headings
        self.tree.heading('Item_Name', text='Item Name', anchor=W)
        self.tree.heading('Item_Price', text='Item Price', anchor=W)
        self.tree.heading('Item_Quantity', text='Quantity', anchor=W)
        self.tree.heading('Item_Category', text='Category', anchor=W)
        self.tree.heading('Discount', text='Discount', anchor=W)
        self.tree.pack()
        
        # Insert the data into the tree table
        for list in rows:
            self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4]))

    '''Widgets for adding item information'''
    def AddRecord(self):
        self.ClearScreen()

        self.name = Label(self.frame_1, text="Item Name", font=(self.font_2, 15, "bold"),fg=self.color_4 ,bg=self.color_5).place(x=220,y=30)
        self.name_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.name_entry.place(x=220,y=65, width=300)

        self.price = Label(self.frame_1, text="Item Price", font=(self.font_2, 15, "bold") ,fg=self.color_4, bg=self.color_5).place(x=220,y=100)
        self.price_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.price_entry.place(x=220,y=135, width=300)

        self.quantity = Label(self.frame_1, text="Item Quantity", font=(self.font_2, 15, "bold"),fg=self.color_4 , bg=self.color_5).place(x=220,y=170)
        self.quantity_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.quantity_entry.place(x=220,y=205, width=300)

        self.category = Label(self.frame_1, text="Item Category", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=220,y=240)
        self.category_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.category_entry.place(x=220,y=275, width=300)

        self.discount = Label(self.frame_1, text="Item Discount", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=220,y=310)
        self.discount_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.discount_entry.place(x=220,y=345, width=300)

        self.submit_bt_1 = Button(self.frame_1, text='Submit', font=(self.font_1, 12), bd=2, command=self.Submit, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=310,y=389,width=100)

    '''Get the item name to perform search operation'''
    def GetItem_to_Search(self):
        self.ClearScreen()
        getName = Label(self.frame_1, text="Item Name", font=(self.font_2, 18, "bold") ,fg=self.color_4, bg=self.color_5).place(x=160,y=70)
        self.name_entry = Entry(self.frame_1, font=(self.font_1, 12), bg=self.color_4, fg=self.color_3)
        self.name_entry.place(x=160, y=110, width=200, height=30)

        submit_bt_2 = Button(self.frame_1, text='Submit', font=(self.font_1, 10), bd=2, command=self.CheckItem_to_Search, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=220,y=160,width=80)
    '''Get the item name to perform update operation'''
    def Getitem_Update(self):
        self.ClearScreen()

        self.getInfo = Label(self.frame_1, text="Enter Item Name", font=(self.font_2, 18, "bold"),fg=self.color_4, bg=self.color_5).place(x=163,y=70)
        self.getInfo_entry = Entry(self.frame_1, font=(self.font_1, 12), bg=self.color_4, fg=self.color_3)
        self.getInfo_entry.place(x=163, y=110, width=200, height=30)
        self.submit_bt_2 = Button(self.frame_1, text='Submit', font=(self.font_1, 10), bd=2, command=self.Checkitem_Update, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=220,y=150,width=80)

    '''Get the item name to perform delete operation'''
    def Getitem_Delete(self):
        self.ClearScreen()

        self.getInfo = Label(self.frame_1, text="Enter Item Name", font=(self.font_2, 18, "bold"),fg=self.color_4, bg=self.color_5).place(x=163,y=70)
        self.getInfo_entry = Entry(self.frame_1, font=(self.font_1, 12), bg=self.color_4, fg=self.color_3)
        self.getInfo_entry.place(x=163, y=110, width=200, height=30)
        self.submit_bt_2 = Button(self.frame_1, text='Submit', font=(self.font_1, 10), bd=2, command=self.DeleteData, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=220,y=150,width=80)

            
    '''Remove all widgets from the frame 1'''
    def ClearScreen(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()

    '''Exit window'''
    def Exit(self):
        self.window.destroy()

    '''
    It checks whether the item is available or not. If available, 
    the function calls the 'ShowRecords' function to display matched records
    '''
    def CheckItem_to_Search(self):
        if self.name_entry.get() == "" :
            messagebox.showerror("Error!", "You must input Item name",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                curs = connection.cursor()
                curs.execute("select * from item_register where Item_Name=%s ", (self.name_entry.get()))
                rows=curs.fetchall()
                if len(rows) == 0:
                    messagebox.showerror("Error!","This Item doesn't exists",parent=self.window)
                    connection.close()
                    self.name_entry.delete(0, END)
                    
                else:
                    self.ShowRecords(rows)
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    '''
    This function is used to update an existing record
    '''
    def Checkitem_Update(self):
      if self.getInfo_entry.get() == "":
            messagebox.showerror("Error!", "Please enter Item name ",parent=self.window)
      else:
          try:
              connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
              curs = connection.cursor()
              curs.execute("select * from item_register where Item_Name=%s", self.getInfo_entry.get())
              row=curs.fetchone()
              if row == None:
                  messagebox.showerror("Error!","Item doesn't exists",parent=self.window)
              else:
                  self.GetUpdateDetails(row)
                  connection.close()
          except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window) 

    '''This function is used to delete a selected record'''
    def DeleteData(self):
        if self.getInfo_entry.get() == "":
            messagebox.showerror("Error!", "Please enter Item name",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                curs = connection.cursor()
                curs.execute("select * from item_register where Item_Name=%s", self.getInfo_entry.get())
                row=curs.fetchone()
                
                if row == None:
                    messagebox.showerror("Error!","Item doesn't exists",parent=self.window)
                else:
                    curs.execute("delete from item_register where Item_Name=%s", self.getInfo_entry.get())
                    connection.commit()
                    messagebox.showinfo('Done!', "The data has been deleted")
                    connection.close()
                    self.ClearScreen()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)         
            
    '''This function gets the data from the user for performing 
    the update operation'''
    def GetUpdateDetails(self, row):
        self.ClearScreen()
        self.ClearScreen()

        self.name = Label(self.frame_1, text="Item Name", font=(self.font_2, 15, "bold"),fg=self.color_4 , bg=self.color_5).place(x=40,y=30)
        self.name_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.name_entry.insert(0, row[0])
        self.name_entry.place(x=40,y=65, width=200)

        self.price = Label(self.frame_1, text="Item Price", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=300,y=30)
        self.price_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.price_entry.insert(0, row[1])
        self.price_entry.place(x=300,y=65, width=200)

        self.quantity = Label(self.frame_1, text="Item Quantity", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=40,y=100)
        self.quantity_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.quantity_entry.insert(0, row[2])
        self.quantity_entry.place(x=40,y=135, width=200)

        self.category = Label(self.frame_1, text="Item Category", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=300,y=100)
        self.category_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.category_entry.insert(0, row[3])
        self.category_entry.place(x=300,y=135, width=200)

        self.discount = Label(self.frame_1, text="Discount", font=(self.font_2, 15, "bold"),fg=self.color_4, bg=self.color_5).place(x=40,y=170)
        self.discount_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.discount_entry.insert(0, row[4])
        self.discount_entry.place(x=40,y=205, width=200)

        self.submit_bt_1 = Button(self.frame_1, text='Submit', font=(self.font_1, 12), bd=2, command=partial(self.UpdateDetails,row), cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=160,y=389,width=100)
        self.cancel_bt = Button(self.frame_1, text='Cancel', font=(self.font_1, 12), bd=2, command=self.ClearScreen, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=280,y=389,width=100)


       
    '''It updates a record in the database'''
    def UpdateDetails(self,row):
        if self.name_entry.get() == "" or self.price_entry.get() == "" or self.quantity_entry.get() == "" or self.category_entry.get() == "" or self.discount_entry.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("update Item_register set Item_Name=%s,Item_Price=%s,Item_Quantity=%s,Item_Category=%s , Discount=%s where Item_Name=%s",
                (
                      self.name_entry.get(),
                      self.price_entry.get(),
                      self.quantity_entry.get(),
                      self.category_entry.get(),
                      self.discount_entry.get(),
                      row[0]
                     ))
                messagebox.showinfo("Success!", "The data has been updated")
                connection.commit()
                connection.close()
                self.ClearScreen()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)  
    
    '''This function adds a new record'''
    def Submit(self):
        if self.name_entry.get() == "" or self.price_entry.get() == "" or self.quantity_entry.get() == "" or self.category_entry.get() == "" or self.discount_entry.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                curs = connection.cursor()
                curs.execute("select * from item_register where Item_Name=%s", self.name_entry.get())
                row=curs.fetchone()
                curs.execute("insert into item_register (Item_Name,Item_Price,Item_Quantity,Item_Category,Discount) values(%s,%s,%s,%s,%s)",
                                            (
                                                self.name_entry.get(),
                                                self.price_entry.get(),
                                                self.quantity_entry.get(),
                                                self.category_entry.get(),
                                                self.discount_entry.get()  
                                            ))
                connection.commit()
                connection.close()
                messagebox.showinfo('Done!', "The data has been submitted")
                self.reset_fields()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    '''Reset all the entry fields'''
    def reset_fields(self):
        self.name_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.category_entry.delete(0, END)
        self.discount_entry.delete(0, END)

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = Management(root)
    root.mainloop()
