import mysql.connector
from tkinter import *
from tkinter import ttk
import datetime
import json
from datetime import datetime, timedelta
import time





mydb = mysql.connector.connect(
    #host="3.69.64.100",
    #user = "admin_landus",
    #passwd = "RAmxaYYtbXwfzcf3",
    #database = "admin_pland"
    host= input("hostname eingeben: "),
    user= input("username eingeben: "),
    passwd= input("passwort eingeben: "),
    database= input("datenbankname eingeben: "),
)
global my_cursor
my_cursor = mydb.cursor()




def main_cat_empty(my_tree):
# checks if main_cat ist emty?
    my_tree.delete(*my_tree.get_children())

    print(
        "\n" "Prüfe auf leere Objektkategorie (Main)")

    try:
        my_cursor.execute("SELECT list.id, list.main_cat, list.new_cat FROM admin_pland.listing as list left join admin_pland.about as ab on "
                          "list.id = ab.listing_id where completed = 1 AND (main_cat is null or main_cat= ' ') ORDER BY `list`.`id` ASC")
        result = my_cursor.fetchall()
        counter = 0

        # create tree and define columns
        my_tree['columns'] = ("id", "main_cat", "new_cat")
        # formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
        my_tree.column("main_cat", width=150, minwidth=25, anchor=W)
        my_tree.column("new_cat", width=400, minwidth=25, anchor=W)
        # create Headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("id", text="id")
        my_tree.heading("main_cat", text="main_cat", anchor=W)
        my_tree.heading("new_cat", text="new_cat", anchor=W)

        for row in result:
            my_tree.insert(parent='', index='end', iid=counter, text="", values=row) #insert data in tree
            counter += 1
            print(row)


    except:
        print("Daten schon aufgerufen")
    return my_tree.pack(), print("\n" f"Bei {counter} Datensätzen ist die main_cat leer") #print tree to screen


def land_not_von(my_tree):
# checks if Objekttitel (about_type) is empty
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob -von- vor dem Grundbuchort steht")

    try:
        my_cursor.execute("SELECT list.id, land FROM admin_pland.listing as list  where completed = 1 and land not like 'von%' and land != ' ' ORDER BY `list`.`id` ASC")
        result = my_cursor.fetchall()
        counter = 0

        # create tree and define columns
        my_tree['columns'] = ("id", "land")
        # formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
        my_tree.column("land", width=1000, minwidth=25, anchor=W, stretch=NO) #bugg wenn wechsel zwischen tree
        # create Headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("id", text="id")
        my_tree.heading("land", text="land", anchor=W)

        if result[0] != 0:
            counter = 0
            for row in result:
                my_tree.insert(parent='', index='end', iid=counter, text="", values=row)  # insert data in tree
                counter += 1
                print(row)

        print("\n" f"Bei {counter} Datensätzen ist -von- nicht das erste Wort des Grundbuchortes. Leere Felder sind davon ausgenommen.")

    except:
        print("Alle Daten korrekt")

    #input("Leere felder mit -Enter-Taste- anzeigen: ")
    try:
        my_cursor.execute("SELECT list.id, land FROM admin_pland.listing as list  where completed = 1 and land = ' ' ORDER BY `list`.`id` ASC")
        result = my_cursor.fetchall()

        if result[0] != 0:
            counter = 0
            for row in result:
                my_tree.insert(parent='', index='end', iid=counter, text="", values=row)  # insert data in tree
                counter += 1
                print(row)
        print("\n" f"Bei {counter} Datensätzen ist der Grundbuchort nicht ausgefüllt.")

    except:
        print("Alle Daten korrekt")

    return my_tree.pack()

def new_cat_notlike_main_cat(my_tree):
# checks if new_cat is same as main_cat
    my_tree.delete(*my_tree.get_children())
    try:
        print("\n" "Prüfe ob die main_cat unterschieldlich zur new_cat ist")

        my_cursor.execute("SELECT list.id, main_cat, new_cat FROM admin_pland.listing as list left join admin_pland.about as ab on "
                          "list.id = ab.listing_id where completed = 1 and SUBSTRING(main_cat,1,4) != SUBSTRING(new_cat,3,4) ORDER BY `list`.`id` ASC")
        result = my_cursor.fetchall()
        counter=0

        #create tree and define columns
        my_tree['columns'] = ("id", "main_cat", "new_cat")
        #formate columns
        my_tree.column("#0", width=0, minwidth=0)
        my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
        my_tree.column("main_cat", width=200, minwidth=25)
        my_tree.column("new_cat", width=500, minwidth=25)
        #create Headings
        my_tree.heading("#0", text="Label")
        my_tree.heading("id", text="id")
        my_tree.heading("main_cat", text="main_cat", anchor=W)
        my_tree.heading("new_cat", text="new_cat", anchor=W)

        for row in result:
            my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
            counter += 1
            print(row)

        # Pack to the screen
        print("\n" f"Bei {counter} Datensätzen ist main_cat unterschieldlich zur new_cat oder die new cat nich in json")

    except:
        print("Daten schon aufgerufen")
    return my_tree.pack()

def komma_in_object_address(my_tree):
# checks if komma_in_object_address
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob mindestens ein Komma in der Objektadresse vorhanden ist")

    my_cursor.execute("SELECT list.id, object_address FROM admin_pland.listing as list where completed = 1 and object_address not like '%,%' and object_address != ' ' ORDER BY `list`.`id` ASC")
    result = my_cursor.fetchall()
    counter=0

    #create tree and define columns
    my_tree['columns'] = ("id", "object_address")
    #formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("object_address", width=600, minwidth=25)

    #create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("object_address", text="object_address", anchor=W)

    for row in result:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter+=1


    print("\n" f"Bei {counter} Datensätzen ist kein -Kommazeichen- in der Objektadresse vorhanden")

    return my_tree.pack()


def Lat_and_Long_filled(my_tree):
# checks if Lat und Long is filled
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob Lat und Long ausgefüllt ist")

    my_cursor.execute("SELECT list.id,  lat, lng FROM admin_pland.listing as list where completed = 1 and (lat is null or lng is null) ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    #create tree and define columns
    my_tree['columns'] = ("id", "lat", "lng")
    #formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("lat", width=60, minwidth=25)
    my_tree.column("lng", width=60, minwidth=25)
    #create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("lat", text="lat", anchor=W)
    my_tree.heading("lng", text="lng", anchor=W)

    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter+=1

    print("\n" f"Bei {counter} Datensätzen ist Lat oder Long nicht ausgefüllt")

    return my_tree.pack()


def object_desc_not_filled(my_tree):
# checks if object_desc is not filled
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob object_desc ausgefüllt ist")

    my_cursor.execute("SELECT list.id, object_desc FROM admin_pland.listing as list where completed = 1 and object_desc= ' ' ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    #create tree and define columns
    my_tree['columns'] = ("id", "object_desc")
    #formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("object_desc", width=200, minwidth=25)
    #create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("object_desc", text="object_desc", anchor=W)

    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter+=1

    print("\n" f"Bei {counter} Datensätzen ist object_desc nicht ausgefüllt")

    return my_tree.pack()


def object_val_not_numeric(my_tree):
# checks if object_desc is filled
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob object_val_not_numeric nicht nummerisch ist")

    my_cursor.execute("SELECT list.id,  object_val FROM admin_pland.listing as list where completed = 1 and object_val REGEXP '^[0-9]+$' =false ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    #create tree and define columns
    my_tree['columns'] = ("id", "object_val")
    #formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("object_val", width=200, minwidth=25)
    #create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("object_val", text="object_val", anchor=W)

    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter+=1

    print("\n" f"Bei {counter} Datensätzen ist object_val nicht rein nummerisch oder leer")

    return my_tree.pack()


def etw_got_flatcount(my_tree):
# checks if etw got flatcount
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob Eigentumswohnungen die Anzahl der Wohnungen befüllt haben")

    my_cursor.execute("SELECT list.id,  main_cat, listing_flats FROM admin_pland.listing as list left join admin_pland.details as det on list.id = det.listing_id where completed = 1 and main_cat= 'Eigentumswohnungen' and listing_flats != ' ' ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    # create tree and define columns
    my_tree['columns'] = ("id", "main_cat", "listing_flats")
    # formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("main_cat", width=200, minwidth=25)
    my_tree.column("listing_flats", width=500, minwidth=25)
    # create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("main_cat", text="main_cat", anchor=W)
    my_tree.heading("listing_flats", text="listing_flats", anchor=W)

    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter+=1

    print("\n" f"Bei {counter} Datensätzen besitzen die Eigentumswohnungen einen listing_flats Wert. Setzt die korrektheit der main_cat vorraus!!!")

    return my_tree.pack()


def inspection_after(my_tree, root,e):
# gives listings after the date of the userinput
    my_tree.delete(*my_tree.get_children())
    insert_time = e.get()

    try:
            newdate1 = datetime.datetime.strptime(str(insert_time), "%d.%m.%Y")

            sql= "SELECT list.id,  inspection_date FROM admin_pland.listing as list left join admin_pland.foreclosure as fore on list.id = fore.listing_id where inspection_date is not null and inspection_status = 0 ORDER BY inspection_date ASC "
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
            counter=0

            # create tree and define columns
            my_tree['columns'] = ("id", "inspection_date")
            # formate columns
            my_tree.column("#0", width=0, minwidth=0)
            my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
            my_tree.column("inspection_date", width=500, minwidth=25)
            # create Headings
            my_tree.heading("#0", text="Label")
            my_tree.heading("id", text="id")
            my_tree.heading("inspection_date", text="inspection_date", anchor=W)

            for row in result:
                if datetime.datetime.strptime(row[1], "%d.%m.%Y") > newdate1:
                    my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
                    print(row)
                    counter+=1

            print("\n" f"Bei {counter} Datensätzen bei welchen -Datum der Besichtigung nicht verfügbar-, NICHT ausgewählt wurde, liegt das Inspektionsdatum nach dem eingegebenen Datum.")
    except:
        print("Eingaben nur im Format: tt.mm.jjj wie z.B. 01.09.2020")

        inputdate=""
    return my_tree.pack()




def denkmalschutz(my_tree):
# checks if denkmalschutz is true, when denkmalschutz in equipment
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob Denkmalschutz ausgewählt ist. wenn Denkmalschutz(15) im equipment steht")

    my_cursor.execute("SELECT list.id,  denkmalschutz, listing_equipment FROM admin_pland.listing as list "
                      "left join admin_pland.details as det on list.id = det.listing_id "
                      "left join admin_pland.foreclosure as fore on list.id = fore.listing_id "
                      "where (completed = 1 and listing_equipment like '%15%' and denkmalschutz = 0 ) or (completed = 1 and listing_equipment not like '%15%' and denkmalschutz = 1) ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    # create tree and define columns
    my_tree['columns'] = ("id", "denkmalschutz", "listing_equipment")
    # formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("denkmalschutz", width=100, minwidth=25, anchor=CENTER)
    my_tree.column("listing_equipment", width=200, minwidth=25)
    # create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("denkmalschutz", text="denkmalschutz", anchor=W)
    my_tree.heading("listing_equipment", text="listing_equipment", anchor=W)


    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        print(row)
        counter +=1

    print("\n" f"Bei {counter} Datensätzen Stimmt der Haken bei Denkmalschutz mit dem Equipment: Denkmalschutz nicht überein")

    return my_tree.pack()


def az_dubble(my_tree):
# checks if denkmalschutz is true, when denkmalschutz in equipment
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe auf doppelte aktenzeichen")

    my_cursor.execute("SELECT foreclosure_date, listing_label, COUNT(listing_label) FROM admin_pland.listing as list GROUP BY listing_label HAVING COUNT(listing_label) > '1' ORDER BY `listing_label` ASC")
    result_label = my_cursor.fetchall()

    counter=0

    # create tree and define columns
    my_tree['columns'] = ("foreclosure_date", "listing_label", "count listing_label")
    # formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("foreclosure_date", width=0, minwidth=25, anchor=CENTER)
    my_tree.column("listing_label", width=100, minwidth=25, anchor=CENTER)
    my_tree.column("count listing_label", width=200, minwidth=25)


    # create Headings
    my_tree.heading("#0", text="")
    my_tree.heading("foreclosure_date", text="")
    my_tree.heading("listing_label", text="listing_label", anchor=W)
    my_tree.heading("count listing_label", text="count listing_label", anchor=W)


    #print(result_label)
    l1 = []
    for i in result_label:
        if i[0] and i[1] not in l1:
            l1.append(i[0] and i[1])
        else:
            print(i, end=' ')
            counter +=1
            my_tree.insert(parent='', index='end', iid=counter, text="", values=i)




#print("\n" f"Bei {counter} Datensätzen ist das Aktenzeichen doppelt")

    return my_tree.pack()



def nebengebäude_more_expensive(my_tree):
# checks if estimated in facility table is more expensive then the objectprice
    my_tree.delete(*my_tree.get_children())

    print("\n" "Prüfe ob der Geschätzte Wert der Nebengebäude den Verkehrswert übersteigen")

    my_cursor.execute("SELECT list.id,  object_price, facility_table FROM admin_pland.listing as list "
                      "left join admin_pland.facility as fac on list.id = fac.listing_id "
                      "left join admin_pland.acquisition as acq on list.id = acq.listing_id "
                      "where completed = 1 and object_price is not null and facility_table is not null and facility_table != 'null' ORDER BY `list`.`id` ASC")
    only_main_cat = my_cursor.fetchall()
    counter=0

    # create tree and define columns
    my_tree['columns'] = ("id", "object_price", "facility_table")
    # formate columns
    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("id", width=60, minwidth=25, anchor=CENTER)
    my_tree.column("object_price", width=200, minwidth=25)
    my_tree.column("facility_table", width=500, minwidth=25)
    # create Headings
    my_tree.heading("#0", text="Label")
    my_tree.heading("id", text="id")
    my_tree.heading("object_price", text="object_price")
    my_tree.heading("facility_table", text="facility_table")

    for row in only_main_cat:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=row)
        x = row[2]

        jsonobject = json.loads(x)
        if jsonobject[0]["estimated"] != "" or not None:
            money= jsonobject[0]["estimated"]
        #value = Decimal(sub(r'[^\d.]', '', money))


        if row[1]< jsonobject[0]["estimated"]:
            print(row[0],",",row[1],",",jsonobject[0]["estimated"])
            counter+=1

    print("\n" f"Funktioniert erst, wenn alle Zahlen rein nummerisch sind!!! Bei {counter} Datensätzen liegt der Nebengebäudewert über dem Verkehrswert. Errors erscheinen, wenn das Json Format in der Datenbank inkonsistent ist")

    return my_tree.pack()








