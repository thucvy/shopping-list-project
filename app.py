import pymysql
from flask import Flask, render_template, request
# from insertdatanew import mysqlconnect

def create_app():
    app = Flask(__name__)
    # Connect to DB
    # def dbconnection():
    connection = pymysql.connect(
        host='testshoppinglist.cehvmw6cebib.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='password1',
        db='ShoppingList'
    )
    cursor = connection.cursor()

    # cursor.execute("DROP TABLE IF EXISTS items")
    # cursor.execute("DROP TABLE IF EXISTS lists")

    #Create 'lists' table into the database.
    # list_create_sql = 'CREATE TABLE lists (id INT PRIMARY KEY AUTO_INCREMENT, listName VARCHAR(30) NOT NULL UNIQUE,' \
    #                 'Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)'
    # cursor.execute(list_create_sql)

    #Create 'items' table into the database.
    # item_create_sql = 'CREATE TABLE items (id INT PRIMARY KEY AUTO_INCREMENT,ItemName VARCHAR(30) NOT NULL,' \
    #             'Quantity INT, Unit VARCHAR(10), Notes VARCHAR(100), Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
    #             'list_id INT NOT NULL, FOREIGN KEY (list_id) REFERENCES lists (id))'
    # item_create_sql = 'CREATE TABLE items (id INT PRIMARY KEY AUTO_INCREMENT, ItemName VARCHAR(30) NOT NULL,' \
    #                 'Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
    #                 'list_id INT NOT NULL, CONSTRAINT List_ItemName UNIQUE (list_id,ItemName),' \
    #                 'CONSTRAINT FK_ListID FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE)'
    # cursor.execute(item_create_sql)
    # connection.commit()

    #Home page without input (to be redirected back when discard or create new list)
    @app.route("/", methods =["GET", "POST"])
    def home(): 
        return render_template('home.html',entries = "", listname = "")

    #Home page with inputs (require to save or discard before proceeding)
    @app.route("/display", methods =["GET", "POST"])
    def display():
        if request.method == "POST":
            # insert list name (one list at a time) to DB
            listname = request.form.get("list") #get the name of the list input which is "list"
            list_insert_sql = 'INSERT IGNORE INTO lists(listName) VALUES (%s)'
            cursor.execute(list_insert_sql,listname)
            
            #Get the corresponding list id based on list name
            list_sql = 'SELECT id FROM lists WHERE listName = %s'
            cursor.execute(list_sql,listname)
            last_id = cursor.fetchall()

            # insert items and details (multiple) to DB
            item_name = request.form.get("item") #get the name of the item input which is "item"
            list_item = (last_id, item_name) #list of (list_id, item_name) tuples
            item_insert_sql = "INSERT IGNORE INTO items(list_id,ItemName) VALUES(%s,%s)"
            cursor.execute(item_insert_sql,list_item)
            
            #Join lists table and items table to have the item_list table which contains item name and list name
            item_list_sql = 'SELECT i.ItemName, l.listName FROM items i JOIN lists l ON i.list_id = l.id WHERE l.listName = %s'
            cursor.execute(item_list_sql,listname)
            item_list = cursor.fetchall()

            # entries is a list of all items in the DB (consider entries as list)
            entries = [
                item_list[index][0] 
                for index in range(len(item_list)) #list all item names in the entries list
            ]         
            
            connection.commit()
            
        return render_template('home.html', entries = entries, listname = listname)

    #Home page with inputs AND with notice (to ask user to either save or discard the inputs)
    @app.route("/display/with-notice", methods =["GET", "POST"])
    def display_withnotice():
        # if request.method == "GET":
        #Create the joint table 'item_list'
        item_list_sql = 'SELECT i.ItemName, l.listName FROM items i JOIN lists l ON i.list_id = l.id'
        cursor.execute(item_list_sql)
        item_list = cursor.fetchall()
        
        #Display the last list name that user inputs from the joint table 'item_list'
        listname = item_list[len(item_list)-1][1] 
        
        #entries is a list of all items in the DB (consider entries as list)
        entries = [
            item_list[index][0] 
            for index in range(len(item_list)) #list all item names in the entries list
        ]
        connection.commit()
        
        return render_template('with-notice.html', entries = entries, listname = listname)

    #'Discard' button --> to remove the current list with items from DB
    @app.route("/discard", methods = ["GET", "POST"])
    def discard():
        #Create the joint table 'item_list'
        item_list_sql = 'SELECT i.ItemName, l.listName FROM items i JOIN lists l ON i.list_id = l.id'
        cursor.execute(item_list_sql)
        item_list = cursor.fetchall()
        
        #Display the last list name that user inputs from the joint table 'item_list'
        listname = item_list[len(item_list)-1][1] 
        
        #Delete current list from lists table in DB, then the corresponding items will also be deleted from items table
        list_delete_sql = "DELETE FROM lists WHERE listName = %s"
        cursor.execute(list_delete_sql,listname)

        connection.commit()
        
        return render_template('home.html', entries = "", listname = "")

    #Data was already saved in DB automatically when user inputs, this 'Save' button is only to redirect to the 'View history' page
    @app.route("/save", methods =["GET","POST"])
    def save():
        return 'go to View history page'
        
    # connection.close()
    return app