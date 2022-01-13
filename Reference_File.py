import pymysql


def mysqlconnect():
    connection = pymysql.connect(
        host='testshoppinglist.cehvmw6cebib.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='password1',
        db='ShoppingList'
    )
    listsname = [("Groceries"),
                 ("Clothes"),
                 ]

    itemname = [("1","Milk", "2", "L", "With Less Saturated Fat"),
                ("Sugar", "5", "Kg", "BrownSuga"),
                ("T-Shirt", "2", "S", "Cotton")]
    cursor = connection.cursor()
    print("Connection established")
    # cursor.executemany("INSERT INTO lists(listName) VALUES (%s)", listsname)
    list_ins = "INSERT INTO lists(listName) VALUES (%s)"
    item_ins = "INSERT INTO items(list_id,ItemName,Quantity,Unit,Notes) VALUES (%s,%s,%s,%s,%s)"
    try:
        for res, name in enumerate(listsname):
            cursor.execute(list_ins, name)
            # returns the value generated for an AUTO_INCREMENT column by the previous INSERT
            # Use that PRIMARYKEY to insert records in items table
            last_id = cursor.lastrowid
            #Appending listId with tuples by iterating each item
            cursor.execute(item_ins, (last_id,) + itemname[res])

        connection.commit()
    except:
        connection.rollback()
    connection.close()
    # Rollback in case there is any error




if __name__ == "__main__":
    mysqlconnect()
