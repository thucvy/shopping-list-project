from flask import Flask, render_template, request
app = Flask(__name__)

entries = []

@app.route("/", methods =["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("item") #get the name of the input field which is "item"
        entries.append(entry_content)
        
    return render_template('home.html', entries = entries)

if __name__ == '__main__':
    app.run(debug=True)