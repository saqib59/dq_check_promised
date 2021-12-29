import abfragen
from abfragen import *
import mysql.connector
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import time
import json
from PIL import ImageTk, Image
import os

host = input("hostname eingeben: ")
user = input("username eingeben: ")
passwd = input("passwort eingeben: ")
database = input("datenbankname eingeben: ")
#host = "3.69.64.100"
#user = "admin_landus"
#passwd = "RAmxaYYtbXwfzcf3"
#database = "admin_pland"


# define root
root = Tk()
root.title('Promised Dataquality')
# Frames
frame = Frame(master=root)  # Farbe geben: bg='cyan'
frame.pack()
frame2 = Frame(master=root)
frame2.pack()
frame3 = Frame(master=root)
frame3.pack()

my_tree = ttk.Treeview(root, height=30, selectmode='extended')

# scrollbar
sb_y = Scrollbar(root, orient=VERTICAL)
sb_y.pack(side=RIGHT, fill=Y)
my_tree.config(yscrollcommand=sb_y.set)
sb_y.config(command=my_tree.yview)

sb_x = Scrollbar(root, orient=HORIZONTAL)
sb_x.pack(side=BOTTOM, fill=X)
my_tree.config(xscrollcommand=sb_x.set)
sb_x.config(command=my_tree.xview)

# Button
main_cat_empty_Button = Button(master=frame, text="Objektkategorie(Main)(main_cat_) leer?",
                               command=lambda: main_cat_empty(my_tree),
                               padx=15,
                               pady=8,
                               bg='#081947',
                               fg='#fff',
                               font=('Times BOLD', 8)
                               ).pack(side=LEFT)

# Button
land_not_von_Button = Button(master=frame, text="Grundbuch beginnend mit -von- ?",
                             command=lambda: land_not_von(my_tree),
                             padx=15,
                             pady=8,
                             bg='#081947',
                             fg='#fff',
                             font=('Times BOLD', 8)
                             ).pack(side=LEFT)

# Button
new_cat_notlike_main_cat_Button = Button(master=frame, text="Objektkategorien(Main)&(wird Kunden gezeigt) gleich?",
                                         command=lambda: new_cat_notlike_main_cat(my_tree),
                                         padx=15,
                                         pady=8,
                                         bg='#081947',
                                         fg='#fff',
                                         font=('Times BOLD', 8)
                                         ).pack(side=LEFT)

# Button
komma_in_object_address_Button = Button(master=frame, text="Komma in Objektadresse?",
                                        command=lambda: komma_in_object_address(my_tree),
                                        padx=15,
                                        pady=8,
                                        bg='#081947',
                                        fg='#fff',
                                        font=('Times BOLD', 8)
                                        ).pack(side=LEFT)

# Button
Lat_and_Long_filled_Button = Button(master=frame, text="Lat und lng ausgefüllt?",
                                    command=lambda: Lat_and_Long_filled(my_tree),
                                    padx=15,
                                    pady=8,
                                    bg='#081947',
                                    fg='#fff',
                                    font=('Times BOLD', 8)
                                    ).pack(side=LEFT)

# Button
object_desc_not_filled_Button = Button(master=frame2, text="Objektbeschreibung ausgefüllt?",
                                       command=lambda: object_desc_not_filled(my_tree),
                                       padx=15,
                                       pady=8,
                                       bg='#081947',
                                       fg='#fff',
                                       font=('Times BOLD', 8)
                                       ).pack(side=LEFT)

# Button
object_val_not_numeric_Button = Button(master=frame2, text="Objektwert nicht nummerisch?",
                                       command=lambda: object_val_not_numeric(my_tree),
                                       padx=15,
                                       pady=8,
                                       bg='#081947',
                                       fg='#fff',
                                       font=('Times BOLD', 8),
                                       ).pack(side=LEFT)

# Button
etw_got_flatcount_Button = Button(master=frame2, text="etw hat mehrere Wohneinheiten?",
                                  command=lambda: etw_got_flatcount(my_tree),
                                  padx=15,
                                  pady=8,
                                  bg='#081947',
                                  fg='#fff',
                                  font=('Times BOLD', 8)
                                  ).pack(side=LEFT)

# Button
denkmalschutz_Button = Button(master=frame2, text="Denkmalschutz gleich ausgefüllt?",
                              command=lambda: denkmalschutz(my_tree),
                              padx=15,
                              pady=8,
                              bg='#081947',
                              fg='#fff',
                              font=('Times BOLD', 8)
                              ).pack(side=LEFT)

# Button
dubble_aktenzeichen = Button(master=frame2, text="Aktenzeichen doppelt vorhanden?",
                              command=lambda: az_dubble(my_tree),
                              padx=15,
                              pady=8,
                              bg='#081947',
                              fg='#fff',
                              font=('Times BOLD', 8)
                              ).pack(side=LEFT)

# Button
nebengebaeude_more_expensive_Button = Button(master=frame2, text="Außer Betrieb! Nebengebäude zu teuer",
                                             command=lambda: nebengebäude_more_expensive(my_tree),
                                             padx=15,
                                             pady=8,
                                             bg='#081947',
                                             fg='#fff',
                                             font=('Times BOLD', 8)
                                             ).pack(side=LEFT)

# Label
inspection_after_Label = Label(master=frame3, text="Inspektionsdatum nach:",
                               padx=15,
                               pady=8,
                               bg='#081947',
                               fg='#fff',
                               font=('Times BOLD', 8)
                               ).pack(side=LEFT)

# inputbox
e = Entry(master=frame3,
          font=('Times BOLD', 8))
e.insert(0, '01.09.2021')
e.pack(side=LEFT)
# eingabe-bestätigung-button
add_answer_button = Button(master=frame3, text='bestätigen', command=lambda: inspection_after(my_tree, root, e),
                           font=('Times BOLD', 8)
                           ).pack(side=LEFT)


#Image and Label for green light
imggreen = ImageTk.PhotoImage(Image.open("green_light.jpg"))
workinglabel = Label(root, image=imggreen)
canvas = Canvas(root, width=200, height=200)
scraper_good_label = Label(root, text='Scraper arbeitet', image=imggreen, compound='top')

#Image and Label for red light
imgred = ImageTk.PhotoImage(Image.open("red_light.jpg"))
notworkinglabel = Label(root, image=imgred)
canvas = Canvas(root, width=200, height=200)
scraper_bad_label = Label(root, text='Scraper arbeitet vermutlich nicht', image=imgred, compound='top')



def check_if_scraper_is_running():
    # checks if scraper is still running


    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database,
        port=3306
    )
    global my_cursor
    my_cursor = mydb.cursor()


        #print("Verbindung mit db fehlgeschlagen")

    critical_time = datetime.now() - timedelta(hours=4)
    sql = "SELECT insert_at FROM admin_pland.listing where updated_at >= %(critical_time)s and insert_at >= %(critical_time)s"
    my_cursor.execute(sql, {'critical_time': critical_time})
    result = my_cursor.fetchall()

    if result:
        print(print(result, critical_time, "Scraper status: In den letzten 4 Stunden wurden Listings hinzugefügt oder geupdated"))
        scraper_bad_label.pack_forget()
        scraper_good_label.pack(side="top")

    if not result:
        print(result, critical_time, "Scraper status: Keine Listings über inserted oder updated seit min. 4 Stunden")
        scraper_good_label.pack_forget()
        scraper_bad_label.pack(side="top")

    root.after(100000, check_if_scraper_is_running)


root.after(3000, check_if_scraper_is_running())

# textbox
# text_box = Tk.Text(root,height=10,width=50, padx=15, pady=15)
# text_box.insert(1.0, outputlist)
# tree for treeview

"""
#add style
style = ttk.style()
style.theme_use('default')
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")
"""
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# mainloop
root.mainloop()
