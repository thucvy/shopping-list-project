import pymysql


def dbconnection():
    connection = pymysql.connect(
        host='testshoppinglist.cehvmw6cebib.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='password1',
        db='ShoppingList'
    )
    cursor = connection.cursor()
    print("Connection created")
    # Prepare SQL query to Create a lists table into the database.
    sqlList = 'CREATE TABLE lists (id INT  PRIMARY KEY AUTO_INCREMENT,listName VARCHAR(30) NOT NULL,' \
              'Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)'

    sqlItems = 'CREATE TABLE items (id INT  PRIMARY KEY AUTO_INCREMENT,ItemName VARCHAR(30) NOT NULL,' \
               'Quantity INT ,Unit VARCHAR(10),Notes VARCHAR(100),Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
               'list_id INT  NOT NULL,FOREIGN KEY (list_id) REFERENCES lists (id))'

    # cursor.execute("DROP TABLE IF EXISTS items")
    # cursor.execute("DROP TABLE IF EXISTS lists")

    print("Table dropped")

    try:
        # Execute the SQL command
        cursor.execute(sqlList)
        print("List table is created")
        cursor.execute(sqlItems)
        print("Item table is created")
        # To display the tables
        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())
        connection.commit()
    except:
        # Rollback in case there is any error
        connection.rollback()

    connection.close()
    print("Table has been created")


if __name__ == "__main__":
    dbconnection()
