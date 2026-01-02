# from finacne
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from function import apology, login_required, usd  #Configure application, cs50 work
app = Flask(__name__)

app.jinja_env.filters["usd"] = usd


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///final.db")

# chat gpt put the emoji for me

category_income = [
    "💰 Allowance",
    "💼 Salary",
    "💵 Petty cash",
    "🎁 Bonus",
    " Other"
]

category_expense = [
    "🍔 Food",
    "🎉 Social Life",
    "🐾 Pets",
    "🚌 Transport",
    "🏠 Household",
    "💊 Health",
    "💅 Beauty",
    "📚 Education",
    "🎁 Gift",
    "💡 Other"
]

accounts = [
    "💵 Cash",
    "🏦 Bank account",
    "💳 Card"
]


# from finacne
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# from finacne
@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    total, income, expense = 0, 0, 0
    transaction = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    for item in  transaction:
        amount = float(item["amount"])
        if item["type"] == "🤑income":
            total += amount
            income += amount
        else:
            total -= amount
            expense += amount
    return render_template("index.html", trs=transaction, total=total, income=income, expense=expense)


    # Render the template with the accumulated stock information and grand total
    return render_template("index.html")
#cs50 work
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
        flash("You log in!", "succsess")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            flash("MISSING USERNAME!", "danger")
            return redirect("/register")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            flash("USERNAME TAKEN", "danger")
            return redirect("/register")

        if not request.form.get("password"):
            flash("MISSING PASSWORD!", "danger")
            return redirect("/register")
        if request.form.get("password") != request.form.get("confirmation"):
            flash("PASSWORDS DON'T MATCH", "danger")
            return redirect("/register")

        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)

        flash("Register succsess!", "succsess")
        return redirect("/login")

    else:
        return render_template("registers.html")

@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    #that's line from chatgpt
    render_args = {"category": category_income, "account": accounts}
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            flash("Missing amount", "danger")
            return render_template("income.html", **render_args)
        if float(amount) < 0:
            flash("Enter vaild amount", "danger")
            return render_template("income.html", **render_args)
        category = request.form.get("category")
        if not category:
            flash("Missing category", "danger")
            return render_template("income.html", **render_args)
        if category not in category_income:
            flash("Invaild category", "danger")
            return render_template("income.html", **render_args)
        account = request.form.get("account")
        if not account:
            flash("Missing account", "danger")
            return render_template("income.html", **render_args)
        if account not in accounts:
            flash("Invaild account", "danger")
            return render_template("income.html", **render_args)
        db.execute(
            "INSERT INTO transactions (user_id, type, category, account, amount, note) VALUES (?, ?, ?, ?, ?, ?)"
            ,session["user_id"], "🤑income", category, account, amount, request.form.get("note"))
        flash("Income add successfully!", "success")
        return redirect("/")
    else:
        return render_template("income.html", **render_args)

@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    #that's line from chatgpt
    render_args = {"category": category_expense, "account": accounts}
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            flash("Missing amount", "danger")
            return render_template("expense.html", **render_args)
        if float(amount) <= 0:
            flash("Enter vaild amount", "danger")
            return render_template("expense.html", **render_args)
        category = request.form.get("category")
        if not category:
            flash("Missing category", "danger")
            return render_template("expense.html", **render_args)
        if category not in category_expense:
            flash("Invaild category", "danger")
            return render_template("expense.html", **render_args)
        account = request.form.get("account")
        if not account:
            flash("Missing account", "danger")
            return render_template("expense.html", **render_args)
        if account not in accounts:
            flash("Invaild account", "danger")
            return render_template("expense.html", **render_args)

        db.execute(
            "INSERT INTO transactions (user_id, type, category, account, amount, note) VALUES (?, ?, ?, ?, ?, ?)"
            ,session["user_id"], "💸expense", category, account, amount, request.form.get("note"))
        flash("Expense add successfully!", "success")
        return redirect("/")
    else:
        return render_template("expense.html", **render_args)
#chat gpt
@app.route("/delete/<int:transaction_id>", methods=["POST"])
@login_required
def delete(transaction_id):
    user_id = session["user_id"]

    # Only delete the user’s own transactions
    db.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", transaction_id, user_id)
    return redirect("/")
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("You log out!", "info")
    return redirect("/")

@app.route("/change_password", methods = ["GET", "POST"])
def change_password():
    if request.method == "POST":
        user_id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("name"))
        if not user_id:
            flash("No user name in data base!", "danger")
            return redirect("/change_password")
        if not request.form.get("password"):
            flash("Please enter password!", "danger")
            return redirect("/change_password")
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password not match!", "danger")
            return redirect("/change_password")
        db.execute("UPDATE users SET hash = ? WHERE id = ?",generate_password_hash(request.form.get("password")), int(user_id[0]["id"]))
        flash("Password changed successfully!", "success")
        return redirect("/")
    else:
        return render_template("change_password.html")

