import tkinter as tk
from main_with_dates import Program
from DBManager_class import DBManager
from Timer_class import Timer

# ============= FUNCTIONS ==================

def start_program_button():

    #start the timer
    global formated_time_var, date_of_study_var
    if program.timer.start_time is None:
        program.timer.start()
        print('Timer has started')
        status_label.config(fg='Green')
        status_label_text.set("Timer has started")
        start_button_text.set("Press here to stop timer")
        pause_button.config(state=tk.NORMAL)

    elif program.timer.start_time is not None:
        formated_time_var = program.timer.stop()
        date_of_study_var = program.timer.get_date()
        status_label.config(fg='Red')
        status_label_text.set("Timer has stopped")
        start_button_text.set("Press here to start timer")



        pause_button.config(state=tk.DISABLED)

def pause_program_button():
    #pause button
    if program.timer.is_paused:
        pause_duration = program.timer.resume()
        print(f"Timer resumed after a pause of {pause_duration}. Type 'exit' to stop the timer or 'p' to pause it again.")
        pause_button_text.set("Click here to pause counter")
        status_label_text.set("Timer is running after the pause")
        status_label.config(fg='red')
    elif program.timer.is_paused is False:
        elapsed_time = program.timer.pause()
        print(f'Timer paused after {elapsed_time}. Type "p" again to resume')
        pause_button_text.set("Click here to resume counter")
        status_label_text.set("Timer is paused")
        status_label.config(fg='Green')

def check_user_input(*args):
    user_input_value = user_input_text.get()
    if user_input_value and user_input_value != "Entry topic description here...":
        update_db_button.config(state=tk.NORMAL)
    else:
        update_db_button.config(state=tk.DISABLED)

def handle_click_user_input(event):
    #clears the text when user clicks on it
    user_input_text.set("")

def add_db_entry():
    global formated_time_var, date_of_study_var
    user_input_value = user_input_text.get()

    if user_input_value != "Entry topic description here...":
        update_db_button.config(state=tk.NORMAL)
        user_input_value = user_input_text.get()

        program.db_manager.connect()
        program.db_manager.write_to_db(formated_time_var, date_of_study_var, user_input_value)
        program.db_manager.disconnect()
    else:
        update_db_button.config(state=tk.DISABLED)

def update_listbox_with_DB():
    #
    if listbox.size() == 0:
        program.db_manager.connect()
        rows = db_manager.fetch_all()
        if rows is not None:
            for row in rows:
                listbox.insert(tk.END, str(row))
        refresh_db_button_text.set('Refresh current data from DB')
        program.db_manager.disconnect()
    else:
        
        listbox.delete(0, tk.END)
        rows = db_manager.fetch_all()
        if rows is not None:
            for row in rows:
                listbox.insert(tk.END, str(row))

def dummy_command():
    print('Command executed')

def exit_program():
    db_manager.disconnect()
    print('DB connection closed')
    root.quit()


# ================= SETUP ===================

# Creating instances of the classes

db_manager = DBManager('LoggingDB.db')
db_manager.connect()
timer = Timer()
program = Program(db_manager, timer)

# Main window
root = tk.Tk() #creates root window
root.geometry("500x500") #set width=500 and height 200 px


# Global Variables
formated_time_var = None
date_of_study_var = None

# String Variables
pause_button_text = tk.StringVar(value = "Click here to pause the counter")
start_button_text = tk.StringVar(value = "Press here to start timer")
status_label_text = tk.StringVar(value = "Timer not yet started")
user_input_text = tk.StringVar(value = "Entry topic description here...")
update_db_button_text = tk.StringVar(value = "Add study session to DB")
refresh_db_button_text = tk.StringVar(value= "Load all entries from DataBase")

# Buttons
start_button = tk.Button(root, textvariable=start_button_text, command=start_program_button, width=25, height=1)
pause_button = tk.Button(root, textvariable=pause_button_text, command=pause_program_button, width=25, height=1, state=tk.DISABLED)
update_db_button = tk.Button(root, textvariable=update_db_button_text, command=add_db_entry, width=25, height=1, state=tk.DISABLED)
refresh_db_button = tk.Button(root, textvariable=refresh_db_button_text, command=update_listbox_with_DB, width=25, height=1 )

# Traces
user_input_text.trace_add("write", check_user_input)

# Labels
hello_label = tk.Label(root, text="Hello, welcome to study tracker")
status_label = tk.Label(root, textvariable=status_label_text)

# User input
user_input = tk.Entry(root,textvariable=user_input_text , width=50)
user_input.bind('<FocusIn>', handle_click_user_input)

# Menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Exit', command=exit_program)
menubar.add_cascade(label='File', menu=filemenu)


# Listbox and Scrollbox
scrollbar = tk.Scrollbar(root)
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, width=500)

# Packing widgets
hello_label.pack(pady=2)
start_button.pack(pady=2)
pause_button.pack(pady=2)
status_label.pack(pady=2)
user_input.pack(pady=3)
refresh_db_button.pack(pady=10)
update_db_button.pack(pady=2)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT)
scrollbar.config(command=listbox.yview)


#Final config
root.config(menu=menubar)
root.mainloop() #main loop which waits for user input
