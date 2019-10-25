#Import dependencies
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Create instance of Flask App
app = Flask(__name__)

#Connect to the Database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://katya:IamN01b01dy@localhost/datacollecter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Data(db.Model):
    #create a table
    __tablename__ = "lids"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

#Define Route and Contant of that page
@app.route("/")
def index():
    return render_template("index.html")

#Define 2nd Route and Content
@app.route("/success", methods = ['POST'])
def success():
    if(request.method == 'POST'):
        name_ = request.form["name"]
        email_ = request.form("email")
        data = Data(name_, email_)
        db.session.add(data)
        db.session.commit()
        return render_template("success.html")

#Running and Controlling the script
if (__name__ =="__main__"):
    app.run(debug=True)