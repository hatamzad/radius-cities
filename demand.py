from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, scrolledtext
import mysql.connector
import csv
import os
from pyzipcode import ZipCodeDatabase


mydata = []
data = []
distance = []

def update(rows):
    global mydata
    mydata = None 
    mydata = rows
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

def up(row):
    global data
    data = row
    trv1.delete(*trv1.get_children())
    for i in row:
        trv1.insert('', 'end', values=i)    


def zipcode(zip_code, distance):
    mycursor.execute("SELECT lat,lng FROM radius.sample WHERE zip LIKE '%"+zip_code +"%'")            
    rows = mycursor.fetchall()
    array = [0, 0]
    for i in rows:
        array[0] = i[0]
        array[1] = i[1]
    zipcodebyradiance(distance, array[0], array[1])    
    return array

def zipcodebyradiance(distance, lat, lng):
    long_max = str(lng + (distance * (1/54.6)))
    long_min = str(lng - (distance  * (1/54.6)))
    lat_max = str(lat + (distance  * (1/69)))
    lat_min = str(lat - (distance  * (1/69)))
    mycursor.execute("Select zip,city, state_name, income_household_median, population from radius.sample where\
     lng < '"+long_max +"' AND lng > '"+long_min+"' AND lat < '"+lat_max +"' AND lat > '"+lat_min +"'")            
    rows = mycursor.fetchall()
    # for i in rows:
        # print(i) 
    # update(rows)
    return rows

def search2():
    zip_code = e4.get()
    distance = int(e5.get()) 
    array = zipcode(zip_code, distance)
    rows = zipcodebyradiance(distance, array[0], array[1]) 
    update(rows)                       

def search():
    state_name = box.get()
    city = e2.get()
    income = e3.get() 
    mycursor.execute("SELECT zip,city, state_name, income_household_median, population FROM radius.sample WHERE income_household_median > %s\
                      AND state_name LIKE '%"+state_name+"%'\
                      AND city LIKE '%"+city+"%'\
                      ORDER BY income_household_median DESC ", ( income,))            
    rows = mycursor.fetchall()
    update(rows)


def total():
    state_name = box.get()
    city = e2.get()
    income= e3.get()  
    mycursor.execute("SELECT SUM(population) FROM radius.sample WHERE income_household_median > %s\
                      AND state_name LIKE '%"+state_name+"%'\
                      AND city LIKE '%"+city+"%'\
                      ORDER BY income_household_median DESC ", ( income,))            
    row = mycursor.fetchall()
    up(row)
        

def clear():
    mycursor.execute("SELECT zip, city, state_name, income_household_median, population FROM radius.sample")
    rows = mycursor.fetchall()
    update(rows)  


def export():
    if len(mydata) < 1:
        if len(data) < 1:
            messagebox.showerror("No Data", "No data availbale to export")
            return False

    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV file", "*.csv"), ("All files", "*.*"))) 
    with open(fln, mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')  
        for i in mydata:
            exp_writer.writerow(i)  
        for j in data:  
            exp_writer.writerow(j)    
    messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ "successfully. ")   

def exportdistace():
    if len(mydata) < 1:
        messagebox.showerror("No Data", "No data availbale to export")
        return False

    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV file", "*.csv"), ("All files", "*.*"))) 
    with open(fln, mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',')  
        for i in mydata:
            exp_writer.writerow(i)      
    messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ "successfully. ")                        
                              
       

df = mysql.connector.connect(user='root', password='amir', 
                            host='127.0.0.1', 
                            database='radius')

root = Tk()
q = StringVar()

wrapper1 = LabelFrame(root, text="")
wrapper2 = LabelFrame(root, text="City Data")


wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)


trv = ttk.Treeview(wrapper2, columns=(1,2,3,4,5), show="headings", height=10)
trv.pack()
trv1 = ttk.Treeview(wrapper2, columns=(1), show="headings", height=1)
trv1.pack()
trv1.place(x=800, y=270)

trv1.heading(1, text="Total Population")

trv.heading(1, text="ZipCode")
trv.heading(2, text="City")
trv.heading(3, text="State Name")
trv.heading(4, text="Income Household Median")
trv.heading(5, text="Population")



mycursor = df.cursor()
mycursor.execute("SELECT zip, city, state_name, income_household_median, population FROM radius.sample")
rows = mycursor.fetchall()
update(rows)

mycursor = df.cursor()
mycursor.execute("SELECT SUM(population) FROM radius.sample")
row = mycursor.fetchall()
up(row)

#search section

Label(root, text="Select State").place(x=30, y=60)
us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
            'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 'Florida', 
            'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
            'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
            'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 
            'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
            'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
            'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ]
box = ttk.Combobox(root, values=us_states)
box.place(x=30, y=60)    
Label(root, text="City").place(x=70, y=100)
Label(root, text="Income").place(x=250, y=100)
Label(root, text="ZipCode").place(x=550, y=60)
Label(root, text="Mile").place(x=550, y=100)


#e1 = Entry(root)
box.place(x=100, y=60)

e2 = Entry(root)
e2.place(x=100, y=100)

e3 = Entry(root)
e3.place(x=300, y=100)

e4 = Entry(root)
e4.place(x=600, y=60)

e5 = Entry(root)
e5.place(x=600, y=100)


btn = Button(wrapper1, text="Search", command=search)
btn.pack(side=tk.LEFT, padx=20)
btn.place(x=90, y=125)
btn = Button(wrapper1, text="Search", command=search2)
btn.pack(side=tk.LEFT, padx=20)
btn.place(x=580, y=125)
cbtn = Button(wrapper1, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=20)
cbtn.place(x=150, y=125)
expbtn = Button(wrapper1, text="Export CSV", command=export)
expbtn.pack(side=tk.LEFT, padx=10, pady=10)
expbtn.place(x=200, y=125)
expbtn = Button(wrapper1, text="Export Zipcodes", command=exportdistace)
expbtn.pack(side=tk.LEFT, padx=10, pady=10)
expbtn.place(x=650, y=125)
expbtn = Button(wrapper2, text="Total Population", command=total)
expbtn.pack(side=tk.LEFT, padx=10, pady=10)
expbtn.place(x=800, y=330)


root.title("Data Search")
root.geometry("1300x700")
root.mainloop()