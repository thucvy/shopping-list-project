import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)
# conn = pymysql.connect(
#     host='testdb.cehvmw6cebib.us-east-1.rds.amazonaws.com',
#     port=3306,
#     user='admin',
#     password='password1',
#     db='testDataBase'
# )

# cur = conn.cursor()

entries =[]

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
        # listname = request.form.get("list") #get the name of the list input which is "list"
        entry_content = request.form.get("item") #get the name of the item input which is "item"
        if entry_content not in entries:
            entries.append(entry_content)

        #feed input to database
        # cur.execute("INSERT INTO Details (list,item) VALUES (%s,%s)", (listname, entry_content))
        # conn.commit()

        #Display entries from database
        # entries = cur.execute("SELECT item FROM Details")
    return render_template('home.html', entries = entries, listname = request.form.get("list"))

@app.route("/display/with-notice", methods =["GET", "POST"])
def display_withnotice():
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
    return render_template('with-notice.html', entries = entries, listname = request.form.get("list"))

        #feed input to database
        # cur.execute("INSERT INTO Details (list,item) VALUES (%s,%s)", (listname, entry_content))
        # conn.commit()

        #Display entries from database
        # entries = cur.execute("SELECT item FROM Details")
    return render_template('home.html', entries = entries, listname = request.form.get("list"))


@app.route("/save", methods =["GET","POST"])
def save():
    return 'save'
    
#     if request.method =="POST":
#         listname = request.form.get("list")
#         itemname = request.form.get("item")
#         cur.execute("INSERT INTO Details (list,item) VALUES (%s,%s)", (listname, itemname))
#         conn.commit()

#     return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)