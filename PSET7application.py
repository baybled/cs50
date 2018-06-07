import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# export FLASK_APP=application.py
# export API_KEY=8PNTWN68T5091PKQ
# export FLASK_DEBUG=ON

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Find data from portfolio table
    rows = db.execute("SELECT * from portfolio WHERE id = :id", id=session["user_id"])

    # Make lists from sql data

    shares = []
    stock = []

    for l in rows:
        stock.append(l['stock'])
        shares.append(l['shares'])

    # Iterate over values to find current price and total held value

    prices = []
    holding = []

    for i in range(len(stock)):
        temp = lookup(stock[i])
        prices.append(temp['price'])
        holding.append(prices[i]*shares[i])

    # Make dictionary from lists for jinja for loop

    rows = []

    for i in range(len(stock)):
        rows.append(dict(stock=stock[i], shares=shares[i], prices=prices[i], holding=holding[i]))

    # Find data from user table
    user = db.execute("SELECT * from users where id = :id", id=session["user_id"])
    balance = usd(user[0]["cash"])
    total_assets = usd(user[0]["cash"] + sum(holding))

    return render_template("index.html", rows = rows, balance = balance, total_assets = total_assets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method =="POST":

        # Ensure proper usage for symbol
        if not request.form.get("symbol"):
            return apology("Please enter a symbol", 403)

        symbol = request.form.get("symbol")

        # Convert case if necessary
        if symbol.islower():
            symbol = symbol.upper()

        quoted = lookup(symbol)

        if quoted == None:
            return apology("{0} unavailable".format(symbol), 403)

        # Ensure proper usage for shares

        shares = int(request.form.get("shares"))

        if not request.form.get("shares") or shares < 1:
            return apology("Please enter a positive number of shares", 403)

        #Get current user 

        # Check there are sufficient funds
        price = quoted['price'] * shares

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        needed = price - cash[0]["cash"]

        remaining = cash[0]["cash"] - price

        if remaining < 0:
            return apology("Balance too low ${0} needed".format(needed), 403)


        # Update cash after purchase
        try:
            db.execute("UPDATE users SET cash = :new WHERE id = :id", id=session["user_id"], new=remaining)
        except:
            return apology("Transaction failed, money returned", 403)
        
        # Check if stock exists, if so update row, else create new row
        check = db.execute("SELECT stock FROM portfolio WHERE id = :id", id=session["user_id"])

        symcheck = []
        for i in check:
            symcheck.append(i["stock"])

        if symbol in symcheck:
            try:
                db.execute("UPDATE portfolio SET shares = shares + :shares WHERE id = :id AND stock= :stock", shares=shares, id=session["user_id"], stock=symbol)
            except:
                return apology("Transaction failed, shares returned", 403)
        else:
            try:
                db.execute("INSERT INTO portfolio(id, shares, stock) VALUES(:id, :shares, :stock)", id=session["user_id"], shares=shares, stock=symbol)
            except:
                return apology("Transaction failed, shares not added", 403)       

        transactions_update = db.execute("INSERT INTO transactions(price, id, shares, stock) VALUES(:price, :id, :shares, :stock)", id=session["user_id"], shares=shares, price=price/shares, stock=symbol)
        
        return redirect("/")

    # Users reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # FORMAT: {{date time}} : {{bought or sold}} {{ shares }} of {{ symbol }} at {{ price }}

    # Find data from sql table

    query = db.execute("SELECT * FROM transactions WHERE id = :id", id=session["user_id"])

    # Create lists

    datetime = []
    buysell = []
    shares = []
    symbol = []
    price = []

    for l in query:
        date = l['timestamp'][0:10]
        time = l['timestamp'][11:19]
        timedate = "{0} on {1}".format(time, date)
        datetime.append(timedate)
        symbol.append(l['stock'])
        price.append(l['price'])

        # Determine whether bought or sold and always make shares a positive number
        if l['shares'] > 0:
            shares.append(l['shares'])
            buysell.append('Bought')
        else:
            shares.append(l['shares']*-1)
            buysell.append('Sold')

    # Create dictionary
    history = []

    for i in range(len(datetime)):
        history.append(dict(datetime=datetime[i], buysell=buysell[i], shares=shares[i], symbol=symbol[i], price=price[i]))

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # Ensure proper usage
        if not request.form.get("symbol"):
            return apology("Please enter a symbol", 403)

        symbol = request.form.get("symbol")

        # Convert case as necessary
        if symbol.islower():
            symbol = symbol.upper()

        # Look up stock symbol
        quoted = lookup(symbol)

        # If symbol is wrong
        if quoted == None:
            return apology("{0} unavailable".format(symbol), 403)

        return render_template("quoted.html", symbol=quoted['symbol'], price=usd(quoted['price']))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("No username was entered", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("No password was entered", 403)
        # Ensure password and passconf matched
        elif request.form.get("password") != request.form.get("passconf"):
            return apology("Passwords entered did not match", 403)

        # Add user to database if username unique
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :passhash)", username=request.form.get("username"), passhash=generate_password_hash(request.form.get("passconf")))
        
        if not result:
            return apology("Please select a different username", 403)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page     
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    
    # Intialise list from portfolio to query
    symbols = []
    shares = []
    query = db.execute("SELECT * from portfolio WHERE id = :id", id=session["user_id"])
    for i in query:
        symbols.append(i['stock'])
        shares.append(i['shares'])
    
    # User reached route via POST(as by submitting form via POST)
    if request.method == "POST":

        # Check if number of shares selected exceeds current holding
        for i in range(len(symbols)):
            if request.form.get("symbol") == symbols[i]:
                if int(request.form.get("shares")) >shares[i]:
                    return apology("you can only sell {0} shares".format(shares), 403)
                
                # If sale is legal, 
                elif int(request.form.get("shares")) <= shares[i]:
                    sold = lookup(symbols[i])

                    # Update transactions with a minus sale
                    try:
                        db.execute("INSERT INTO transactions(id, shares, price, stock) VALUES(:id, :shares*-1, :price, :stock)", id=session["user_id"], shares=int(request.form.get("shares")), price=sold['price'], stock=symbols[i])
                    except:
                        return apology("Transaction update failed", 403)

                    # Update portfolio and remove row if all shares are sold
                    try:
                        if int(request.form.get("shares")) == shares[i]:
                            db.execute("DELETE FROM portfolio WHERE id = :id AND stock = :stock", id=session["user_id"], stock=symbols[i])
                        else:
                            diff = shares[i] - int(request.form.get("shares"))
                            db.execute("UPDATE portfolio SET shares = :diff WHERE id = :id AND stock = :stock", id=session["user_id"], stock=symbols[i], diff=diff)
                    except:
                        return apology("Portfolio update failed", 403)

                    # Update user's cash with proceeds from sale
                    try:
                        db.execute("UPDATE users SET cash = cash + :sold WHERE id = :id", id=session["user_id"], sold=sold['price']*int(request.form.get("shares")))
                    except:
                        return apology("Cash update failed", 403)
        
        return redirect("/")             

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", symbols=symbols)

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Allows user to change account settings"""

    # User reached route via POST (as by submitting form via POST)
    if request.method == "POST":

        # Ensure proper usage
        if not request.form.get("oldpass") or not request.form.get("newpass") or not request.form.get("passconf"):
            return apology("Please complete the form", 403)

        # Ensure passwords match
        if not request.form.get("newpass") == request.form.get("passconf"):
            return apology("New passwords did not match", 403)

        query = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])

        # Check old password is valid
        if not check_password_hash(query[0]['hash'], request.form.get("oldpass")):
            return apology("Wrong password entered", 403)

        # Change password if old password is correct and both new passwords match
        db.execute("UPDATE users SET hash = :password WHERE id = :id", id=session["user_id"], password=generate_password_hash(request.form.get("passconf")))        

        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("password.html")




def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
