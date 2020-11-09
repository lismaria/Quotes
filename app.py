from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHAME_DATABASE_URI']='sqlite:///users.sqlite3'#users is the table
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False#removes the warnings...we arent tracking everything to database


db=SQLAlchemy(app)#database object(db) equivalent to new sql database

class users(db.Model): #class represents user object in database; db.model is the inheritance i.e, its a database model which has few object and models inherited from it
    _id=db.Column("id",db.Integer,primary_key=True)#colname,datatype
    name=db.Column("name",db.String(100))
    favquote=db.Column(db.String(1000))#if no col name specified..it directly takes the value

    def __init__(self, name, favquote):
        #init methods takes the variable that we need to create a object
        self.name=name
        self.favquote=favquote

@app.route("/")
def home():
     return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method =="POST":
        session.permanent = True #by default its false
        user = request.form["nm"]#nm is the dictionary key i.e i can asccess all the value using key
        session["user"] = user

        found_user=users.query.filter_by(name=user).first()#filter by is looking for a specific user
        if found_user:
            session["favquote"] =found_user.favquote
        else:
            usr=users(user,"")
            db.session.add(usr)#add user model to a database
            db.session.commit()
        flash("Login Successful!")
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged In")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST","GET"])
def user():
    favquote=None
    if "user" in session:
        user=session["user"]

        if request.method=="POST":
            favquote=request.form["favquote"]#grab that favquote from favquote field
            session["favquote"]=favquote#use it in session
            found_user=users.query.filter_by(name=user).first()
            found_user.favquote=favquote
            db.session.commit()
            flash("Favourite Quote Saved!!")
        else:
            if "favquote" in session:
                favquote=session["favquote"]
        return render_template("user.html")
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
        
@app.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("favquote",None)
    if "user" in session:
        user=session["user"]
    flash("You have been logged out!","info")
    return redirect(url_for("login"))

if __name__=="__main__":
    db.create_all()#creates the database if doesnt exist
    app.run(debug=True)

