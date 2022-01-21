import pymysql
from flask import Flask, render_template, request, url_for, redirect

def create_app():
    app = Flask(__name__)
    # Connect to DB
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

    # #Create 'lists' table into the database.
    # list_create_sql = 'CREATE TABLE lists (id INT PRIMARY KEY AUTO_INCREMENT, listName VARCHAR(30) NOT NULL UNIQUE,' \
    #                 'Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)'
    # cursor.execute(list_create_sql)

    

    # #Create 'items' table into the database.
    # item_create_sql = 'CREATE TABLE items (id INT PRIMARY KEY AUTO_INCREMENT, ItemName VARCHAR(30) NOT NULL,' \
    #                 'Quantity INT, Unit VARCHAR(10), Notes VARCHAR(100),' \
    #                 'Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
    #                 'list_id INT NOT NULL, CONSTRAINT List_ItemName UNIQUE (list_id,ItemName),' \
    #                 'CONSTRAINT FK_ListID FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE)'
    # cursor.execute(item_create_sql)
    # connection.commit()

    recordslist = []

    #Home page without input
    @app.route("/", methods =["GET", "POST"])
    def home(): 
        return render_template('home.html',entries = "", listname = "")

    #Home page with inputs (require to save or discard before proceeding)
    @app.route("/display", methods =["GET", "POST"])
    def display():
        if request.method == "POST":
            # insert list name (one list at a time) to DB
            listname = request.form.get("list") #get the name of the list input which is "list"
            list_insert_sql = 'INSERT IGNORE INTO lists(listName) VALUES (TRIM(%s))'
            cursor.execute(list_insert_sql,listname)
            
            #Get the corresponding list id based on list name
            list_sql = 'SELECT id FROM lists WHERE listName = TRIM(%s)'
            cursor.execute(list_sql,listname)
            last_id = cursor.fetchall()

            # insert items and details (multiple) to DB
            item_name = request.form.get("item") #get the name of the item input which is "item"
            list_item = (last_id, item_name, 1, "pc","") #list of (list_id, item_name) tuples
            item_insert_sql = "INSERT IGNORE INTO items(list_id,ItemName,Quantity,Unit,Notes) VALUES(%s,TRIM(%s),%s,%s,%s)"
            cursor.execute(item_insert_sql,list_item)
            
            #Join lists table and items table to have the item_list table which contains item name and list name

            item_list_sql = 'SELECT i.Quantity, i.Unit, i.Notes, i.ItemName, l.id, l.listName FROM items i JOIN lists l ON i.list_id = l.id WHERE l.listName = TRIM(%s)'
            cursor.execute(item_list_sql,listname)
            item_list = cursor.fetchall()
            # entries is a list of all items in the DB (consider entries as list)
            
            entries = [
                item_list[index]
                for index in range(len(item_list)) #list all item names in the entries list
            ]         
            
            connection.commit()
            
        return render_template('home.html', entries = entries, listname = listname)


    #'Discard' button --> to remove the current list with items from DB
    @app.route("/discard/<listname>", methods = ["GET", "POST"])
    def discard(listname):
        print(listname)
        #Delete current list from lists table in DB, then the corresponding items will also be deleted from items table
        list_delete_sql = "DELETE FROM lists WHERE listName = TRIM(%s)"
        cursor.execute(list_delete_sql,listname)

        connection.commit()
        return redirect(url_for('home'))
        
    #Hit 'save' in order to save the additional info for items
    @app.route("/save-details/<lname>", methods =["GET","POST"])
    def save_details(lname):
        #Get the corresponding list id based on list name
        list_sql = 'SELECT id FROM lists WHERE listName = TRIM(%s)'
        cursor.execute(list_sql,lname)
        list_id = cursor.fetchall()[0][0]
        print(list_id)
       
        item_name = request.form.getlist('row_item')
        quantities = request.form.getlist('row_quantity')
        units = request.form.getlist('row_units')
        notes = request.form.getlist('row_note')
        new_details=[]

        for i, item in enumerate(item_name):
            quantity = int(quantities[i])
            unit = units[i]
            note = notes[i]
            new_details.append((quantity, unit, note,item,list_id))
            print(new_details)

        stmt = 'UPDATE items SET Quantity = %s, Unit = %s, Notes = %s WHERE ItemName = TRIM(%s) and list_id = %s'
        cursor.executemany(stmt,new_details)

        item_list_sql = 'SELECT i.Quantity, i.Unit, i.Notes, i.ItemName, l.id, l.listName FROM items i JOIN lists l ON i.list_id = l.id WHERE l.listName = TRIM(%s)'
        cursor.execute(item_list_sql,lname)
        item_list = cursor.fetchall()
     
        entries = [
            item_list[index]
            for index in range(len(item_list))  # list all item names in the entries list
        ]

        connection.commit()
        
        return render_template('home.html', entries=entries, listname=lname)

    #This route is to save and redirect to 'View list history' page (used for the Prompt Ask-History Modal)
    @app.route("/save", methods =["GET","POST"])
    def save():
        if request.method == "GET":
            # Get the list name and timestamp
            list_sql = 'SELECT listName, Date FROM lists'
            cursor.execute(list_sql)
            recordslist = cursor.fetchall()

            print("The records list is", recordslist)

            # return html page and list information
            return render_template('save.html', recordslist = recordslist)


    @app.route("/save/display/<lname>")
    def display_list(lname):
        sql_get_list_items = 'SELECT i.Quantity, i.Unit, i.Notes, i.ItemName, l.id, l.listName FROM items i JOIN lists l ON i.list_id = l.id WHERE l.listName = TRIM(%s)'
        cursor.execute(sql_get_list_items, lname)
        item_list = cursor.fetchall()
        # entries is a list of all items in the DB (consider entries as list)
        entries_list = [
            item_list[index]
            for index in range(len(item_list))  # list all item names in the entries list
        ]
        print("entries_list********** "+str(len(entries_list)))
        return render_template('home.html', entries=entries_list, listname=lname)

    #Updated for deleting item from the list
    @app.route("/delete/<item_name>/<list_name>", methods =["GET","POST"])
    def delete(item_name,list_name):
        print("Query has been updated")
        sql_delete_item = "DELETE FROM items WHERE ItemName = TRIM(%s) AND list_id IN(SELECT id FROM lists WHERE listName=TRIM(%s))"
        input_list = (item_name,list_name)
        cursor.execute(sql_delete_item, input_list)
        connection.commit()
        print("Deleted item rows : " + str(cursor.rowcount))
        response = display_list(list_name)
        return response

    # Updated for DELETE LIST
    @app.route("/list_delete/<lname>", methods =["POST","GET"])
    def list_delete(lname):
        print("in delete method")
        sql_delete_list = "DELETE from lists where listName = TRIM(%s)"
        cursor.execute(sql_delete_list, lname)
        connection.commit()
        print("Deleted rows : "+str(cursor.rowcount))

        return redirect(url_for('save'))   
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)