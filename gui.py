import customtkinter
import tkinter
import database



app = customtkinter.CTk()
app.title('Employee Management System')
app.geometry('1200x700')
app.columnconfigure(0,weight=1)
app.columnconfigure(1,weight=7)
app.rowconfigure(0,weight=1)

def clear():
    for entry in entry_list:
            entry.delete(0,tkinter.END)

def clear_selection():
    table.selection_remove(table.focus())
    id_entry.configure(state='normal')
    clear()

def add_to_table():
    employees = database.fetch_employees()
    table.delete(*table.get_children())
    for employee in employees:
        table.insert(parent='',index = tkinter.END,values=employee)

def insert_to_table():
    id = id_entry.get()
    name = name_entry.get()
    role = role_entry.get()
    gender = variable1.get()
    status = status_entry.get()

    if not (id and name and role and gender and status):
        tkinter.messagebox.showerror('Error','Enter all the fields')
    elif database.id_exists(id):
        tkinter.messagebox.showerror('Error','ID already exists')
    else:
        database.insert_employees(id, name, role, gender, status)
        add_to_table()
        clear()
        tkinter.messagebox.showinfo('Success','Inserted Employee')

def display_data(event):
    selected_item = table.focus()
    if selected_item:
        row = table.item(selected_item)['values']
        clear()
        id_entry.insert(0,row[0])
        id_entry.configure(state='readonly')
        name_entry.insert(0,row[1])
        role_entry.insert(0,row[2])
        variable1.set(row[3])
        status_entry.insert(0,row[4])
    else:
        pass

def delete():
    selected_item = table.focus()
    if not selected_item:
        tkinter.messagebox.showerror('Error','Select an employee to delete')
    else:
        id = id_entry.get()
        database.delete_employee(id)
        add_to_table()
        id_entry.configure(state='normal')
        clear()
        tkinter.messagebox.showinfo('Success','Employee has been deleted')

def update():
    selected_item = table.focus()
    if not selected_item:
        tkinter.messagebox.showerror('Error','Select an employee to update')
    else:
        id = id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        gender = variable1.get()
        status = status_entry.get()
        database.update_employee(name,role,gender,status,id)
        add_to_table()
        id_entry.configure(state='normal')
        clear()
        tkinter.messagebox.showinfo('Success','Employee has been updated')


font1 = ('Arial',20,'bold')
font2 = ('Arial',12,'bold')

left_frame = customtkinter.CTkFrame(app)
left_frame.grid(row=0,column=0,sticky="nsew")
left_frame.columnconfigure(0,weight=1)
left_frame.columnconfigure(1,weight=1)

right_frame = customtkinter.CTkFrame(app)
right_frame.grid(row=0,column=1,sticky="nsew")
right_frame.columnconfigure(0,weight=1)
right_frame.rowconfigure(0,weight=1)

id_label = customtkinter.CTkLabel(left_frame,font=font1,text='ID',text_color='white')
id_label.grid(row=0,column=0,sticky="ew")

id_entry = customtkinter.CTkEntry(left_frame,font=font1,text_color='black',fg_color='white',width=150)
id_entry.grid(row=0,column=1,padx=10,pady=10,sticky = 'nsew')

name_label = customtkinter.CTkLabel(left_frame,font=font1,text='NAME',text_color='white')
name_label.grid(row=1,column=0,sticky="ew")

name_entry = customtkinter.CTkEntry(left_frame,font=font1,text_color='black',fg_color='white',width=150)
name_entry.grid(row=1,column=1,padx=10,pady=10,sticky = 'nsew')


role_label = customtkinter.CTkLabel(left_frame,font=font1,text='ROLE',text_color='white')
role_label.grid(row=2,column=0,sticky="ew")

role_entry = customtkinter.CTkEntry(left_frame,font=font1,text_color='black',fg_color='white',width=150)
role_entry.grid(row=2,column=1,padx=10,pady=10,sticky = 'nsew')

gender_label = customtkinter.CTkLabel(left_frame,font=font1,text='GENDER',text_color='white')
gender_label.grid(row=3,column=0,sticky="ew")

options = ['Male','Female']
variable1 = tkinter.StringVar()

gender_options = customtkinter.CTkComboBox(left_frame,font=font1,variable=variable1,values=options,fg_color='white',text_color='black',state='readonly',width=150)
gender_options.set('Male')
gender_options.grid(row=3,column=1,padx=10,pady=10,sticky = 'nsew')

status_label = customtkinter.CTkLabel(left_frame,font=font1,text='STATUS',text_color='white')
status_label.grid(row=4,column=0,sticky="ew")

status_entry = customtkinter.CTkEntry(left_frame,font=font1,text_color='black',fg_color='white',width=150)
status_entry.grid(row=4,column=1,padx=10,pady=10,sticky = 'nsew')

add_button = customtkinter.CTkButton(left_frame,command=insert_to_table,font=font1,text='ADD Employee',text_color='white',fg_color='green',width=200,hover_color='darkgreen')
add_button.grid(row=5,column=0,padx=10,columnspan=2,pady=10,sticky = 'nsew')

update_button = customtkinter.CTkButton(left_frame,command=update,font=font1,text='UPDATE Employee',text_color='white',fg_color='skyblue',width=200)
update_button.grid(row=6,column=0,padx=10,columnspan=2,pady=10,sticky = 'nsew')

delete_button = customtkinter.CTkButton(left_frame,command=delete,font=font1,text='DELETE Employee',text_color='white',fg_color='red',width=200,hover_color='darkred')
delete_button.grid(row=7,column=0,padx=10,columnspan=2,pady=10,sticky = 'nsew')

clear_button = customtkinter.CTkButton(left_frame,command=clear_selection,font=font1,text='Clear selection',text_color='white',fg_color='skyblue',width=200)
clear_button.grid(row=8,column=0,padx=10,columnspan=2,pady=10,sticky = 'nsew')

s = tkinter.ttk.Style()
s.theme_use('clam')

s.configure('Treeview', font=font2,background="black", fieldbackground="grey", foreground="white")
s.map('Treeview',background=[('selected','green')])
table = tkinter.ttk.Treeview(right_frame, height=15,columns = ('ID','Name',"Role","Gender","Status"), show = 'headings',selectmode="extended")

heading = ['ID','Name',"Role","Gender","Status"]
for i in heading:
    table.heading(i,anchor=tkinter.CENTER, text = i)
    table.column(i,width=150)
table.grid(row=0,column=0,padx=10,pady=10,sticky = 'nsew')

table.bind('<ButtonRelease>', display_data)

entry_list = [id_entry,name_entry,role_entry,status_entry]


if __name__ =='__main__':
    
    database.create_table()
    
    add_to_table()

    app.mainloop()