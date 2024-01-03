import os
import datetime
from cs50 import SQL
from flask import *
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///finance.db")
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


items = db.execute("SELECT * FROM category")
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        rows = db.execute("SELECT id, title, price, category, sellerid FROM listing ORDER BY created_date")
        return render_template("index.html", items=items, rows=rows)
    else:
        id =request.form.get("id")
        rows = db.execute("SELECT id, title, price, category, sellerid FROM listing WHERE category = ? ORDER BY created_date", id)
        return render_template("index.html", items=items, rows=rows)

#CREATE TABLE listing (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT NOT NULL, price TEXT, category INTEGER, created_date TEXT, sellerid INTEGER, FOREIGN KEY(sellerid) REFERENCES users(id),FOREIGN KEY(category) REFERENCES category(id));
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, hostel TEXT, year TEXT, course TEXT);
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        sem = ["I","II","III","IV","V","VI","VII","VIII"]
        return render_template("register.html", semesters=sem)
    else:
        if not request.form.get("username"):
            return apology("must provide 1username", 400)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            return apology("username already exists", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("the passwords do not match", 400)
        hostel = request.form.get("hostel")
        if not hostel:
            return apology("must provide hostel", 400)
        course = request.form.get("course")
        sem = request.form.get("semester")
        if not course:
            return apology("must provide course", 400)
        if not sem:
            return apology("must select semester", 400)
        db.execute("INSERT INTO users(username, hash, hostel, year, course)VALUES (?, ?,?,?,?)",request.form.get("username"),
            generate_password_hash(request.form.get("password"), method="pbkdf2", salt_length=16),hostel,sem,course)
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        rows = db.execute("SELECT id, title, price, category, sellerid FROM listing WHERE sellerid = ? ORDER BY created_date",session["user_id"])
        return render_template("sell.html",items=items,rows = rows)
    else:
        if not request.form.get("title"):
            return apology("must provide title", 400)
        price = request.form.get("price")
        category = request.form.get("category")
        if not price or not category:
            return apology("must provide title", 400)

        db.execute("INSERT INTO listing(title, price, category, created_date, sellerid ) VALUES (?, ?,?,?,?)",request.form.get("title")
                   ,price,category, datetime.datetime.now(), session["user_id"])
        return redirect("/sell")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")
    db.execute("DELETE FROM messages WHERE listingid = ?",id)
    db.execute("DELETE FROM request WHERE listingid = ?",id)
    db.execute("DELETE FROM listing WHERE id = ? AND sellerid = ?",id,session["user_id"])

    return redirect("/")

@app.route("/chat", methods=["GET","POST"])
@login_required
def chat():
    if request.method == "GET":
        users = db.execute("SELECT id, username FROM users")
        names = {}
        for user in users:
            names[user["id"]] = user["username"]
        messages = db.execute("SELECT * FROM request WHERE buyerid = ? OR listingid IN (SELECT id FROM listing WHERE sellerid = ?)", session["user_id"], session["user_id"])
        rows = db.execute("SELECT id, title, price, category, sellerid FROM listing")
        listing = request.args.get("listing")
        if not listing:
            return render_template("chat.html", items=items, rows=rows, messages=messages, names=names)
        else:
            buyerid = request.args.get("buyerid")
            chats = db.execute("SELECT * FROM messages WHERE (senderid = ? OR recieverid = ?) AND listingid = ? ORDER BY dateandtime", buyerid, buyerid, listing)
            sellerid = db.execute("SELECT sellerid FROM listing WHERE id =?", listing)
            return render_template("chats.html", items=items, rows=rows, chats=chats, listing=listing, messages=messages, buyerid=buyerid, sellerid=sellerid, names=names)


    else:
        reciever = request.form.get("id")
        listing = request.form.get("listing")
        content = request.form.get("content")
        db.execute("INSERT INTO messages (senderid, recieverid, listingid, content, dateandtime) VALUES(?, ?, ?, ?, ?)", session["user_id"],  reciever, listing, content, datetime.datetime.now())
        return redirect("/chat?listing="+str(listing)+"&buyerid="+str(reciever))
#CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, senderid INTEGER, recieverid INTEGER, listingid INTEGER, content TEXT, dateandtime TEXT, FOREIGN KEY(listingid) REFERENCES listing(id), FOREIGN KEY(recieverid) REFERENCES users(id), FOREIGN KEY(senderid) REFERENCES users(id));
#CREATE TABLE request (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, buyerid INTEGER, listingid INTEGER, FOREIGN KEY(buyerid) REFERENCES users(id), FOREIGN KEY(listingid) REFERENCES listing(id))

@app.route("/requests", methods=["GET","POST"])
@login_required
def requests():
    if request.method == "POST":
        listing = request.form.get("listing")
        messages = db.execute("SELECT * FROM request WHERE buyerid = ? AND listingid = ?", session["user_id"],  listing)
        if len(messages) == 0:
            db.execute("INSERT INTO request (buyerid, listingid) VALUES (?, ?)", session["user_id"], listing)
            return redirect("/chat?listing="+str(listing)+"&buyerid="+str(session["user_id"]))
        else:
            return redirect("/chat?listing="+str(listing)+"&buyerid="+str(session["user_id"]))


