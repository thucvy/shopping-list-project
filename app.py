import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)
try:
    conn = pymysql.connect(
        host='testshoppinglist.cehvmw6cebib.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='password1',
        db='ShoppingList'
    )

    print("The database is connected")
except:
    print("Database connection failed")

cur = conn.cursor()

entries =[]

recordslist = []

@app.route("/", methods =["GET", "POST"])
def home():
    # if request.method == "POST":
        # listname = request.form.get("list") #get the name of the list input which is "list"
        # entry_content = request.form.get("item") #get the name of the item input which is "item"
        # if not request.form.get("list") and not entry_content:
        #     print("You need to save or discard the current list in order to proceed")
    return render_template('home.html')


@app.route("/display", methods =["GET", "POST"])
def display():
    if request.method == "POST":
        listname = request.form.get("list") #get the name of the list input which is "list"
        entry_content = request.form.get("item") #get the name of the item input which is "item"
        if entry_content not in entries:
            entries.append(entry_content)

        print(entries)

        #feed input to database
        #cur.execute("INSERT INTO lists (list,item) VALUES (%s,%s)", (listname, entry_content))
        #conn.commit()

        #Display entries from database
        # entries = cur.execute("SELECT item FROM Details")
    return render_template('home.html', entries = entries, listname=request.form.get("list"))

@app.route("/display/save-discard", methods =["GET", "POST"])
def displaysavediscard():
    if request.method == "POST":
        # listname = request.form.get("list") #get the name of the list input which is "list"
        entry_content = request.form.get("item") #get the name of the item input which is "item"
        if entry_content not in entries:
            entries.append(entry_content)
                 
        #feed input to database
        # cur.execute("INSERT INTO Details (list,item) VALUES (%s,%s)", (listname, entry_content))
        # conn.commit()

        #Display entries from database
        # entries = cur.execute("SELECT item FROM Details")
    return render_template('save-discard.html', entries = entries, listname = request.form.get("list"))

@app.route("/save", methods =["GET","POST"])
def save():
    if request.method == "GET":
        # Get the list name and timestamp
        list_sql = 'SELECT listName, Date FROM lists'
        cur.execute(list_sql)
        recordslist = cur.fetchall()

        print("The records list is", recordslist)

        # return html page and list information
        return render_template('save.html', recordslist = recordslist)


@app.route("/save/display/<lname>")
def display_list(lname):
    sql_get_list_items = "SELECT i.ItemName FROM items i JOIN lists l ON i.list_id = l.id WHERE l.listName = %s"
    cur.execute(sql_get_list_items, lname)
    item_list = cur.fetchall()
    # entries is a list of all items in the DB (consider entries as list)
    entries_list = [
        item_list[index][0]
        for index in range(len(item_list))  # list all item names in the entries list
    ]
    print("entries_list********** "+str(len(entries_list)))
    return render_template('home.html', entries=entries_list, listname=lname)

#Updated for deleting item from the list
@app.route("/delete/<item_name>/<list_name>", methods =["GET","POST"])
def delete(item_name,list_name):
    print("Query has been updated")
    sql_delete_item = "DELETE FROM items WHERE ItemName = %s AND list_id IN(SELECT id FROM lists WHERE listName=%s)"
    input_list = (item_name,list_name)
    cur.execute(sql_delete_item, input_list)
    conn.commit()
    print("Deleted item rows : " + str(cur.rowcount))
    response = display_list(list_name)
    return response

# Updated for DELETE LIST
@app.route("/list_delete/<lname>", methods =["GET","POST"])
def list_delete(lname):
    print("in delete method")
    sql_delete_list = "DELETE from lists where listName = %s"
    cur.execute(sql_delete_list, lname)
    conn.commit()
    print("Deleted rows : "+str(cur.rowcount))
    list_sql = 'SELECT listName, Date FROM lists'
    cur.execute(list_sql)
    result_record = cur.fetchall()

    print("The records list is", recordslist)

    # return html page and list information
    return render_template('save.html', recordslist=result_record)


if __name__ == '__main__':
    app.run(debug=True)