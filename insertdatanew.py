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
                 ("Clothes")]

    itemname = [("1", "Milk", "2", "L", "With Less Saturated Fat"),
                ("1", "Sugar", "5", "Kg", "BrownSugar"),
                ("2", "T-Shirt", "2", "S", "Cotton")]

    cursor = connection.cursor()
    print("Connection established")

    try:
        print("inside try")
        cursor.executemany("INSERT INTO lists(listName) VALUES (%s)", listsname)
        cursor.executemany("INSERT INTO items(list_id,ItemName,Quantity,Unit,Notes) VALUES(%s,%s,%s,%s,%s) ", itemname)
        connection.commit()
        cursor.execute('SELECT i.ItemName, l.listName ,l.Date FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.listName')
        result = cursor.fetchall()
        for r in result:
            print(r[0], ':', r[1], ':', r[2])
    except:
        print("inside except")
        # Rollback in case there is any error
        connection.rollback()
    connection.close()


if __name__ == "__main__":
    mysqlconnect()
