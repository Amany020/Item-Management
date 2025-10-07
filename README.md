# Item-Management
Code to create a software in which python is connected with MySQL.<br>
Item_Management-System<br>
Pharmacy Management System in Python<br>
Requirements and Installation<br>
Use pip3 instead of pip for Linux and Mac.<br>
Install PyMySQL<br>
☛pip install PyMySQL<br>
Install Tkinter<br>
☛pip install tk<br>

Install MySQL server<br>

Create a Database and a Table<br>
Create a database with this name: "Item_management"<br>
☛create database Item_management;<br>
Create a table "item_register" under the "Item_management" database.<br>
☛create table item_register( <br>
Item_Name VARCHAR(50) NOT NULL, <br>
Item_Price int NOT NULL, <br>
Item_Quantity int NOT NULL, <br>
Item_Category VARCHAR(15) NOT NULL, <br>
Discount int NOT NULL); 
