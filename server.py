from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import json


app = Flask(__name__)

app.config["MYSQL_DATABASE_USER"] = "restart"
app.config["MYSQL_DATABASE_PASSWORD"] = "Azerty123!"
app.config["MYSQL_DATABASE_DB"] = "archive"

mysql = MySQL(app)

connection = mysql.connect()
connection.autocommit(True)

cursor = connection.cursor()

drop = "DROP TABLE IF EXISTS emails;"
createTable = "CREATE TABLE emails(id int not null auto_increment, email varchar(50), primary key (id));"
cursor.execute(drop)
cursor.execute(createTable)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/email", methods=["POST"])
def storeEmails():
    email = request.form.get("email")
    print(email)
    insert = f"INSERT INTO emails (email) values('{email}');"
    out = cursor.execute(insert)
    print(out)
    return {"msg": "Uploaded successfully"}


@app.route("/getAll", methods=["GET"])
def getAll():
    cursor.execute("SELECT * from emails;")
    allEmails = cursor.fetchall()
    print(str(allEmails))
    return json.dumps(allEmails)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False )