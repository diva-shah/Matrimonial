import os, datetime


from dateutil import relativedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Citation
# https://html5-tutorial.net/form-validation/validating-email/
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# distribution code
# https://pypi.org/project/validate_email/

# API_KEY
# export API_KEY=pk_21fabf0cf02c4637a3f0a094d4c1b465
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
db = SQL("sqlite:///matrimonial.db")

# Make sure API key is set

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show profiles"""

    if request.method == "POST":
        return redirect("/")

    else:
        user2 = []
        me = db.execute("""SELECT users.gender,users.username, users.profileStatus, contact.city, contact.state, contact.country FROM users
                        JOIN contact ON contact.userID = users.userID
                        WHERE users.userID = ?""", session["user_id"])
        users = db.execute("""SELECT users.userID, users.username, users.dob, users.gender, users.registered,
                            profile.profession, contact.city, contact.state, contact.country FROM users
                            JOIN profile ON profile.userID = users.userID
                            JOIN contact ON contact.userID = users.userID WHERE users.profileStatus = 'Live' AND users.username NOT IN
                            (SELECT whoGotBlocked FROM blockedUsers WHERE whoBlocked = ?)""", me[0]["username"])
        for user in users:
            user["age"] = calcAge(user["dob"])
            user["profage"] = calcProfileAge(user["registered"])

        return render_template("index.html", users=users, me=me)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():


    if request.method == "POST":

        aboutMe = request.form.get("aboutMe")
        lookingFor = request.form.get("lookingFor")
        citizenship = request.form.get("citizenship")
        origin = request.form.get("country")
        relocation = request.form.get("relocation")
        income = request.form.get("income")
        timeFrame = request.form.get("timeframe")
        marriageStatus = request.form.get("marriageStatus")
        haveChildren = request.form.get("haveChildren")
        wantChildren = request.form.get("wantChildren")
        living = request.form.get("livingArrangements")
        height = request.form.get("height")
        build = request.form.get("build")
        smoke = request.form.get("smoke")
        disability = request.form.get("disability")
        education = request.form.get("education")
        profession = request.form.get("profession")
        jobTitle = request.form.get("jobTitle")

        if not jobTitle:
            return apology("Fields cannot be blank", 400)

        # Query database for profile & preference
        profile = db.execute("SELECT * FROM profile WHERE userID = ?", session["user_id"])
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])

        if len(profile) != 1:
            db.execute("""INSERT INTO profile(userID,aboutMe,lookingFor,citizenship,origin,relocation,income,
                        timeframe,marriageStatus,haveChildren,wantChildren,livingArrangements,height,build,smoke,
                        disabilities,education,profession,jobTitle) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        session["user_id"],aboutMe,lookingFor,citizenship ,origin,relocation,income,timeFrame ,marriageStatus,
                        haveChildren, wantChildren ,living,height,build ,smoke ,disability,education ,profession,jobTitle)

        if len(preference) != 1:
            return redirect("preference")
        else:
            return redirect("/")

    else:
        profile = db.execute("SELECT * FROM profile WHERE userID = ?", session["user_id"])
        if len(profile) == 1:
            return redirect("/")
        else:
            return render_template("profile.html")


@app.route("/preference", methods=["GET", "POST"])
@login_required
def preference():


    if request.method == "POST":

        ageFrom = request.form.get("ageFrom")
        ageTo = request.form.get("ageTo")
        heightFrom = request.form.get("heightFrom")
        heightTo = request.form.get("heightTo")
        country = request.form.get("country")
        education = request.form.get("education")
        marriageStatus = request.form.get("marriage")
        income = request.form.get("income")

        if not education or not marriageStatus or not income or not country:
            return apology("All fields are required", 400)

        # Query database for preference & contact
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])
        contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])

        # Check if preference has been completed
        if len(preference) != 1:
            db.execute("INSERT INTO preference(userID,age,height,country,education,maritalStatus,income) VALUES(?,?,?,?,?,?,?)",
            session["user_id"],ageFrom + " - " + ageTo,heightFrom + " - " + heightTo, country, education, marriageStatus, income)
        if len(contact) != 1:
            return redirect("contact")
        else:
            return redirect("/")

    else:
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])
        if len(preference) == 1:
            return redirect("/")
        else:
            return render_template("preference.html")

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():

    # Query database for contact
    contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])

    if request.method == "POST":

        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        address = request.form.get("address")
        country = request.form.get("country")
        state = request.form.get("state")
        city = request.form.get("city")
        zipcode = request.form.get("zip")
        dob = request.form.get("dob")

        if not firstName or not lastName or not address or not country or not state or not city or not zipcode or not dob:
            return apology("All fields are required", 400)

        if len(contact) != 1:
            db.execute("""INSERT INTO contact(userID,firstName,lastName,address,country,state,city,zipcode,dob)
                        VALUES(?,?,?,?,?,?,?,?,?)""",
                        session["user_id"],firstName,lastName,address,country,state,city ,zipcode,dob)

        return redirect("/")

    else:
        if len(contact) == 1:
            return redirect("/")
        else:
            return render_template("contact.html")


@app.route("/user/<username>")
@login_required
def userProfile(username):
    """Show user"""
    user = db.execute("SELECT userID,username, dob, gender, country, reason, registered, profileStatus, showPictureGuidelines FROM users WHERE username = ?", username)
    profile = db.execute("SELECT * FROM profile WHERE profile.userID = ?", user[0]["userID"])
    location = db.execute("SELECT country, state, city FROM contact WHERE contact.userID = ?", user[0]["userID"])
    prefs = db.execute("SELECT * FROM preference WHERE preference.userID = ?", user[0]["userID"])
    age = calcAge(user[0]['dob'])
    user.extend(profile)
    user.extend(location)
    user.extend(prefs)
    info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
    plikes = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)

    blocked = db.execute("SELECT * from blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)
    length2 = len(blocked)
    choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]['username'])
    check = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)


    length = len(plikes)
    print(length)
    idu = session['user_id']
    otherPerson = db.execute("SELECT * FROM messaging WHERE username = ?", username)
    op = db.execute("SELECT * FROM users WHERE username = ?", username)
    return render_template("user.html", user=user, age=age, idu=idu, length=length, length2=length2, choice=choice, otherPerson=otherPerson, op=op)

@app.route("/search/")
@login_required
def searchprofiles():
    """search user"""
    info = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    users = db.execute("""SELECT users.userID, users.username, users.dob, users.gender, profile.height, profile.origin,
                            profile.citizenship,profile.income, profile.education, profile.profession, contact.state,
                            contact.country FROM users
                            JOIN profile ON profile.userID = users.userID
                            JOIN contact ON contact.userID = users.userID
                            WHERE users.userID <> ? AND users.profileStatus = 'Live' AND users.username NOT IN
                            (SELECT whoGotBlocked FROM blockedUsers WHERE whoBlocked = ?)""", session["user_id"], info[0]["username"])
    for user in users:
            user["age"] = calcAge(user["dob"])

    return render_template("search.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print("Log in", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        name = request.form.get("username")
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password, make sure your registered too!", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userID"]

        # Query database for profile
        profile = db.execute("SELECT * FROM profile WHERE userID = ?", session["user_id"])
        # Query database for preference
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])
        # Query database for contact
        contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])
        # Check if profile has been completed
        if not profile or len(profile) != 1:
            print("No profile")
            return redirect("/profile")

        # Check if preference has been completed
        elif not preference or len(preference) != 1:
            return redirect("preference")

        # Check if contact has been completed
        elif not contact or len(contact) != 1:
            return redirect("contact")

        # Redirect user to home page
        else:

            return redirect("/")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

def passwordCheck(password):
    """Check for requirement validation"""

    punctuation = False
    number = False
    length = False
    characters = False

    for x in password:
        if x == '!' or x == '?' or x == '.':
            punctuation = True
        if x.isnumeric() == True:
            number = True
        if isinstance(x, str) == True and x != '!' and x != '?' and x != '.':
            characters = True
        if len(password) >= 8:
            length = True

    if length == False or number == False or punctuation == False or characters == False:
        return False

def calcAge(date):

    bday = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    today = datetime.date.today()
    age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

    return age

def calcProfileAge(date):

    registered = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
    today = datetime.date.today()
    age = today.year - registered.year - ((today.month, today.day) < (registered.month, registered.day))

    return round(age * 12)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/change", methods = ["GET","POST"])
@login_required
def change():
    punctuation = False
    number = False
    length = False
    characters = False
    if request.method == "POST":
        confirm = request.form.get("confirmNewPassword")
        new = request.form.get("newPassword")
        old = request.form.get("currentPassword")
        info = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if not info:
            return apology("Incorrect username")

        if confirm != new:
            return apology("The new passwords are not the same")

        if not check_password_hash(info[0]["hash"], request.form.get("currentPassword")):
            return apology("The old password you entered is incorrect")
        if passwordCheck(new) == False:
            return apology("Password has to have and can only have punctuation, characters, numbers, and has to be at leats 8 characters long")


        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(new), request.form.get("username"))
        return redirect("/login")
    else:
        return render_template("changepassword.html")

@app.route("/forgotpassword", methods = ["GET", "POST"])
def forgotpassword():
    if request.method == "GET":
        return render_template("forgotpassword.html")
    else:
        username = request.form.get("username")
        information = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not information:
            return apology("Invalid Username")
        question = information[0]['question']
        return render_template("forgot.html", question = question)
        return redirect("/forgot")

@app.route("/forgot", methods = ["GET", "POST"])
def forgot():
    if request.method == "GET":
        information = db.execute("SELECT * FROM users WHERE username = ?")
        return render_template("forgot.html")
    else:
        username = request.form.get("username")
        newPassword = request.form.get("newPassword")
        confirm = request.form.get("confirmNewPassword")
        answer = request.form.get("answer")
        info = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not info:
            return apology("Wrong information")

        if newPassword != confirm:
            return apology("The two passwords don't match")

        if answer != info[0]['answer']:
            return apology("Incorrect answer to your question")

        if passwordCheck(newPassword) == False:
            return apology("Password has to have and can only have punctuation, characters, numbers, and has to be at leats 8 characters long")

        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(newPassword), request.form.get("username"))
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    punctuation = False
    number = False
    length = False
    characters = False
    if request.method == "POST":
        print(request.form.get("dob"))
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords are not the same!")
        check = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if (len(check) > 0):
            return apology("Username Taken")

        check3 = db.execute("SELECT email FROM users WHERE email = ?",request.form.get("email"))
        if len(check3) > 0:
            return apology("Email is Taken, try entering a different email")

        if passwordCheck(request.form.get("password")) == False:
            return apology("Password has to have and can only have punctuation, characters, numbers, and has to be at leats 8 characters long")

        dob = request.form.get("dob")
        if int(calcAge(dob)) < 18:
            return apology("You must be at least 18 years to be on this website!")
        db.execute("INSERT INTO users(email,username,hash,dob,gender,country,reason,source,question,answer) VALUES(?,?,?,?,?,?,?,?,?,?)",request.form.get("email"),request.form.get("username"),generate_password_hash(request.form.get("password")),request.form.get("dob"),request.form.get("gender"),request.form.get("country"),request.form.get("registration"),request.form.get("source"), request.form.get("question"), request.form.get("answer"))

        db.execute("INSERT INTO messaging(username) VALUES(?)", request.form.get("username"))
        return redirect("/profile")

    else:
        return render_template("register.html")



@app.route("/profile/edit", methods=["GET","POST"])
@login_required
def profileEdit():
    """Edit profile"""

    if request.method == "POST":
        return redirect("/")

    else:
        return render_template("shared/editlayout.html")
@app.route("/edittingprofile", methods = ["GET","POST"])
@login_required
def edittingprofile():
    if request.method == "POST":

        aboutMe = request.form.get("aboutMe")
        lookingFor = request.form.get("lookingFor")
        citizenship = request.form.get("citizenship")
        origin = request.form.get("country")
        relocation = request.form.get("relocation")
        income = request.form.get("income")
        timeframe = request.form.get("timeframe")
        marriageStatus = request.form.get("marriageStatus")
        haveChildren = request.form.get("haveChildren")
        wantChildren = request.form.get("wantChildren")
        livingArrangements = request.form.get("livingArrangements")
        height = request.form.get("height")
        build = request.form.get("build")
        smoke = request.form.get("smoke")
        disability = request.form.get("disability")
        education = request.form.get("education")
        profession = request.form.get("profession")
        jobTitle = request.form.get("jobTitle")

        info = db.execute("SELECT * FROM profile WHERE userID = ?", session['user_id'])

        if aboutMe != info[0]['aboutMe']:
            db.execute("UPDATE profile SET aboutMe = ? WHERE userID = ?", aboutMe, session['user_id'])

        if lookingFor != info[0]['lookingFor']:
            db.execute("UPDATE profile SET lookingFor = ? WHERE userID = ?", lookingFor, session['user_id'])

        if citizenship and citizenship != info[0]['citizenship']:
            db.execute("UPDATE profile SET citizenship = ? WHERE userID = ?", citizenship, session['user_id'])

        if origin and origin != info[0]['origin']:
            db.execute("UPDATE profile SET origin = ? WHERE userID = ?", origin, session['user_id'])

        if relocation and relocation != info[0]['relocation']:
            db.execute("UPDATE profile SET relocation = ? WHERE userID = ?", relocation, session['user_id'])

        if income and income != info[0]['income']:
            db.execute("UPDATE profile SET income = ? WHERE userID = ?", income, session['user_id'])

        if timeframe and timeframe != info[0]['timeframe']:
            db.execute("UPDATE profile SET timeframe = ? WHERE userID = ?", timeframe, session['user_id'])

        if marriageStatus and marriageStatus != info[0]['marriageStatus']:
            db.execute("UPDATE profile SET marriageStatus = ? WHERE userID = ?", marriageStatus, session['user_id'])

        if haveChildren and haveChildren != info[0]['haveChildren']:
            db.execute("UPDATE profile SET haveChildren = ? WHERE userID = ?", haveChildren, session['user_id'])

        if wantChildren and wantChildren != info[0]['wantChildren']:
            db.execute("UPDATE profile SET wantChildren = ? WHERE userID = ?", wantChildren, session['user_id'])

        if livingArrangements and livingArrangements != info[0]['livingArrangements']:
            db.execute("UPDATE profile SET livingArrangements = ? WHERE userID = ?", livingArrangements, session['user_id'])

        if height and height != info[0]['height']:
            db.execute("UPDATE profile SET height = ? WHERE userID = ?", height, session['user_id'])

        if build and build != info[0]['build']:
            db.execute("UPDATE profile SET build = ? WHERE userID = ?", build, session['user_id'])

        if smoke and smoke != info[0]['smoke']:
            db.execute("UPDATE profile SET smoke = ? WHERE userID = ?", smoke, session['user_id'])

        if disability and disability != info[0]['disability']:
            db.execute("UPDATE profile SET disability = ? WHERE userID = ?", disability, session['user_id'])

        if education and education != info[0]['education']:
            db.execute("UPDATE profile SET education = ? WHERE userID = ?", education, session['user_id'])

        if profession and profession != info[0]['profession']:
            db.execute("UPDATE profile SET profession = ? WHERE userID = ?", profession, session['user_id'])

        if jobTitle != info[0]['jobTitle']:
            db.execute("UPDATE profile SET jobTitle = ? WHERE userID = ?", jobTitle, session['user_id'])

        return redirect("/profile/edit")
    else:
        users = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
        profile = db.execute("SELECT * FROM profile WHERE userID = ?", session["user_id"])
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])
        contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])
        return render_template("editting.html", users=users, profile=profile, preference=preference, contact=contact)

@app.route("/edittingpreferences", methods = ["GET","POST"])
@login_required
def edittingpreferences():
    if request.method == "POST":
        ageFrom = request.form.get("ageFrom")
        ageTo = request.form.get("ageTo")
        heightFrom = request.form.get("heightFrom")
        heightTo = request.form.get("heightTo")
        education = request.form.get("education")
        marriage = request.form.get("marriage")
        income = request.form.get("income")
        country = request.form.get("country")

        age = ageFrom + " - " + ageTo

        info = db.execute("SELECT * FROM preference WHERE userID = ?", session['user_id'])
        if (ageFrom and not ageTo) or (ageTo and not ageFrom) or (heightFrom and not heightTo) or (heightTo and not heightFrom):
            return apology("If you fill out age from you must fill out age to and vice versa. Same with height from and height to")

        if ageFrom and ageTo and age != info[0]['age']:
            db.execute("UPDATE preference SET age = ? WHERE userID = ?", ageFrom + " - " + ageTo, session["user_id"])

        if heightFrom and heightTo and heightFrom + " - " + heightTo != info[0]['height']:
            db.execute("UPDATE preference SET height = ? WHERE userID = ?", heightFrom + "-" + heightTo, session["user_id"])

        if education and education != info[0]['education']:
            db.execute("UPDATE preference SET education = ? WHERE userID = ?", education, session["user_id"])

        if marriage and marriage != info[0]['maritalStatus']:
            db.execute("UPDATE preference SET maritalStatus = ? WHERE userID = ?", marriage, session["user_id"])

        if income and income != info[0]['income']:
            db.execute("UPDATE preference SET income = ? WHERE userID = ?", income, session["user_id"])

        if country and country != info[0]['country']:
            db.execute("UPDATE preference SET country = ? WHERE userID = ?", country, session["user_id"])
        return redirect("/profile/edit")
    else:
        users = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
        profile = db.execute("SELECT * FROM profile WHERE userID = ?", session["user_id"])
        preference = db.execute("SELECT * FROM preference WHERE userID = ?", session["user_id"])
        contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])
        return render_template("editpreferences.html", users=users, profile=profile, preference=preference, contact=contact)

@app.route("/edittingcontact", methods = ["GET","POST"])
@login_required
def edittingcontact():
    if request.method == "POST":
        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        address = request.form.get("address")
        country = request.form.get("country")
        state = request.form.get("state")
        city = request.form.get("city")
        zipcode = request.form.get("zip")
        dob = request.form.get("dob")

        info = db.execute("SELECT * FROM contact WHERE userID = ?", session['user_id'])
        if firstName != info[0]['firstName'] :
            db.execute("UPDATE contact SET firstName = ? WHERE userID = ?", firstName, session['user_id'])

        if lastName != info[0]['lastName']:
            db.execute("UPDATE contact SET lastName = ? WHERE userID = ?", lastName, session['user_id'])

        if address != info[0]['address']:
            db.execute("UPDATE contact SET address = ? WHERE userID = ?", address, session['user_id'])

        if country and country != info[0]['country']:
            db.execute("UPDATE contact SET country = ? WHERE userID = ?", country, session['user_id'])

        if state and state != info[0]['state']:
            db.execute("UPDATE contact SET state = ? WHERE userID = ?", state, session['user_id'])

        if city and city != info[0]['city']:
            db.execute("UPDATE contact SET city = ? WHERE userID = ?", city, session['user_id'])

        if zipcode != info[0]['zipcode']:
            db.execute("UPDATE contact SET zipcode = ? WHERE userID = ?", zipcode, session['user_id'])

        if dob and dob != info[0]['dob']:
            db.execute("UPDATE contact SET dob = ? WHERE userID = ?", dob, session['user_id'])
        return redirect("/profile/edit")
    else:
        contact = db.execute("SELECT * FROM contact WHERE userID = ?", session["user_id"])
        return render_template("editcontact.html", contact=contact)


@app.route("/aesthetics",methods=["GET","POST"])
@login_required
def aesthetics():
    if request.method == "POST":
        profileStatus = request.form.get("profileStatus")
        showPG = request.form.get("showPG")
        message = request.form.get("messaging")

        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        messaging = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]['username'])

        if profileStatus and profileStatus != info[0]['profileStatus']:
            db.execute("UPDATE users SET profileStatus = ? WHERE userID = ?", profileStatus, session['user_id'])

        if showPG and showPG != info[0]['showPictureGuidelines']:
            db.execute("UPDATE users SET showPictureGuidelines = ? WHERE userID = ?", showPG, session['user_id'])

        if message and message != messaging[0]['status']:
            db.execute("UPDATE messaging SET status = ? WHERE username = ?", message, info[0]['username'])
        return redirect("/profile/edit")
    else:
        return render_template("aesthetics.html")

@app.route("/editusername", methods=["GET","POST"])
@login_required
def editusername():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        if not check_password_hash(info[0]['hash'], password):
            return apology("Incorrect Password")
        if username:
            db.execute("UPDATE users SET username = ? WHERE userID = ?", username, session['user_id'])
        return redirect("/profile/edit")
    else:
        users = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        return render_template("changeusername.html", users=users)

@app.route("/editemail", methods=["GET","POST"])
@login_required
def editemail():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        if not check_password_hash(info[0]['hash'], password):
            return apology("Incorrect Password")
        if email:
            db.execute("UPDATE users SET email = ? WHERE userID = ?", email, session['user_id'])
        return redirect("/profile/edit")
    else:
        users = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        return render_template("changeemail.html", users=users)

@app.route("/editphotos")
@login_required
def photos():
    return render_template("photos.html")

@app.route("/photoaccess")
@login_required
def photoaccess():
    return render_template("photoaccess.html")

@app.route("/memborshiphistory")
@login_required
def memborshiphistory():
    return render_template("memborshiphistory.html")

@app.route("/blockedusers")
@login_required
def blockedusers():
    information = []
    user = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    info = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked IN (SELECT username FROM users WHERE profileStatus='Live')", user[0]["username"])
    length = len(info)
    for x in range(length):
        info2 = db.execute("SELECT * FROM users WHERE username = ?", info[x]["whoGotBlocked"])
        information.append(info2)
    return render_template("blockedusers.html", user=user, info=info, length=length, information = information)


@app.route("/deleteprofile", methods=["GET","POST"])
@login_required
def deleteprofile():
    if request.method == "POST":
        reasons = ["I found success", "I was just trying out the service", "I am going to re-register as another user", "I am concerened about my privacy", "Other"]
        selected = []
        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        password = request.form.get("password")
        if not check_password_hash(info[0]['hash'], password):
            return apology("Incorrect Password")
        combo = ""
        for x in reasons:
            reason = request.form.get(x)
            if reason:
                selected.append(x)
        if len(selected) == 0:
            return apology("Must select a 'reason for leaving'")
        if len(selected) != 1:
            for c in range(len(selected)):
                if c == len(selected) - 1:
                    combo += selected[c]
                else:
                    combo += selected[c] + " and "
        db.execute("INSERT INTO deleteprofile(reason, feedback) VALUES(?,?)", combo, request.form.get("comments"))
        db.execute("DELETE FROM profileLikes WHERE fromMe = ? OR toUser = ?", info[0]['username'],info[0]['username'])
        db.execute("DELETE FROM preference WHERE userID = ?", session["user_id"])
        db.execute("DELETE FROM profile WHERE userID = ?", session["user_id"])
        db.execute("DELETE FROM contact WHERE userID = ?", session["user_id"])
        db.execute("DELETE FROM users WHERE userID = ?", session["user_id"])
        db.execute("DELETE FROM messaging WHERE username = ?", info[0]["username"])
        db.execute("DELETE FROM report WHERE whoReported = ? OR whoGotReported = ?", info[0]['username'])
        return redirect("/login")
    else:
        reasons = ["I found success", "I was just trying out the service", "I am going to re-register as another user", "I am concerened about my privacy", "Other"]
        return render_template("delete.html", reasons = reasons)


@app.route("/liked/<username>")
@login_required
def liked(username):
    info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
    plikes = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)
    user = db.execute("SELECT userID,username, dob, gender, country, reason, registered, profileStatus FROM users WHERE username = ?", username)
    profile = db.execute("SELECT * FROM profile WHERE profile.userID = ?", user[0]["userID"])
    location = db.execute("SELECT country, state, city FROM contact WHERE contact.userID = ?", user[0]["userID"])
    prefs = db.execute("SELECT * FROM preference WHERE preference.userID = ?", user[0]["userID"])
    age = calcAge(user[0]['dob'])
    user.extend(profile)
    user.extend(location)
    user.extend(prefs)

    idu = session['user_id']
    if len(plikes) == 0:
        db.execute("INSERT INTO profileLikes(fromMe, toUser) VALUES(?,?)", info[0]['username'], username)
    plikes2 = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)
    length = len(plikes2)
    blocked = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)
    length2 = len(blocked)
    choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]["username"])
    otherPerson = db.execute("SELECT * FROM messaging WHERE username = ?", username)
    return render_template("user.html", user=user, age=age, idu=idu, length=length, length2=length2, choice=choice, otherPerson=otherPerson)


@app.route("/mylikes")
@login_required
def myLikes():
    iliked = []
    age = []
    othersLiked= []
    ageOfOthers=[]
    info = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    liked = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser IN(SELECT username FROM users WHERE profileStatus = 'Live')", info[0]['username'])
    length = len(liked)
    for x in range(len(liked)):
        idNumber = db.execute("SELECT * FROM users WHERE username = ?", liked[x]['toUser'])
        allinfo = db.execute("SELECT * FROM users,contact,preference,profile WHERE users.userID = ? AND contact.userID = ? AND preference.userID = ? AND profile.userID = ?", idNumber[0]['userID'], idNumber[0]['userID'], idNumber[0]['userID'], idNumber[0]['userID'])
        iliked.append(allinfo)
        age2 = calcAge(idNumber[0]['dob'])
        age.append(age2)

    likedMe = db.execute("SELECT * FROM profileLikes WHERE toUser = ? AND fromMe IN(SELECT username FROM users WHERE profileStatus = 'Live')", info[0]['username'])
    length2 = len(likedMe)

    for y in range(len(likedMe)):
        distinction = db.execute("SELECT * FROM users WHERE username = ?", likedMe[y]["fromMe"])
        allINeed = db.execute("SELECT * FROM users,contact,preference,profile WHERE users.userID = ? AND contact.userID = ? AND preference.userID = ? AND profile.userID = ?", distinction[0]['userID'], distinction[0]['userID'], distinction[0]['userID'], distinction[0]['userID'])
        othersLiked.append(allINeed)
        ageOther = calcAge(distinction[0]['dob'])
        ageOfOthers.append(ageOther)
    return render_template("myLikes.html", liked=liked, length=length, likedMe=likedMe, length2=length2, iliked=iliked, age=age, othersLiked=othersLiked, ageOfOthers=ageOfOthers)


@app.route("/unliked/<username>")
@login_required
def unliked(username):
    info = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    db.execute("DELETE FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)
    user = db.execute("SELECT userID,username, dob, gender, country, reason, registered, profileStatus FROM users WHERE username = ?", username)
    profile = db.execute("SELECT * FROM profile WHERE profile.userID = ?", user[0]["userID"])
    location = db.execute("SELECT country, state, city FROM contact WHERE contact.userID = ?", user[0]["userID"])
    prefs = db.execute("SELECT * FROM preference WHERE preference.userID = ?", user[0]["userID"])
    age = calcAge(user[0]['dob'])
    user.extend(profile)
    user.extend(location)
    user.extend(prefs)
    blocked = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)
    length2 = len(blocked)
    plikes = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)
    length = len(plikes)
    choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]["username"])
    idu = session['user_id']
    otherPerson = db.execute("SELECT * FROM messaging WHERE username = ?", username)
    return render_template("user.html", user=user, age=age, idu=idu, length=length, length2=length2, choice=choice, otherPerson=otherPerson)

@app.route("/messages", methods=["GET","POST"])
@login_required
def messages():
    print("MESSAGES HERE")
    if request.method == "POST":
        return apology("GOING TO IMPLEMENT LATER ON")

    else:
        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        status = info[0]['membership']
        choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]['username'])
        if status != 'gold':
            return render_template("messages.html")

        else:
            return apology("GOING TO IMPLEMENT LATER ON")

@app.route("/report/<username>", methods=["GET","POST"])
@login_required
def report(username):
    if request.method == "POST":
        info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
        name = info[0]['username']
        explanation = request.form.get("explanation")
        r = ["Use of inappropriate language", "Use of inappropriate photos", "Other"]
        selected = []
        combo = ""
        for x in r:
            print(x)
            reason = request.form.get(x)
            if reason:
                selected.append(x)

        if len(selected) == 0:
            return apology("You must select a reason for reporting")

        for y in range(len(selected)):
            if y == len(selected) - 1:
                combo += selected[y]

            else:
                combo += selected[y] + " and "

        db.execute("INSERT INTO report(whoReported, whoGotReported, reasonOfReport, explanation) VALUES(?,?,?,?)", name, username,combo, explanation)
        return redirect("/")

    else:
        reasons = ["Use of inappropriate language", "Use of inappropriate photos", "Other"]
        return render_template("report.html", username=username, reasons=reasons)

@app.route("/blocked/<username>")
@login_required
def blocked(username):
    information = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    db.execute("INSERT INTO blockedUsers(whoBlocked, whoGotBlocked) VALUES(?,?)", information[0]["username"], username)
    db.execute("DELETE FROM profileLikes WHERE fromMe = ? AND toUser = ?", information[0]["username"], username)

    user = db.execute("SELECT userID,username, dob, gender, country, reason, registered, profileStatus, showPictureGuidelines FROM users WHERE username = ?", username)
    profile = db.execute("SELECT * FROM profile WHERE profile.userID = ?", user[0]["userID"])
    location = db.execute("SELECT country, state, city FROM contact WHERE contact.userID = ?", user[0]["userID"])
    prefs = db.execute("SELECT * FROM preference WHERE preference.userID = ?", user[0]["userID"])
    age = calcAge(user[0]['dob'])
    user.extend(profile)
    user.extend(location)
    user.extend(prefs)
    info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
    plikes = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)

    blocked = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)
    length2 = len(blocked)
    choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]['username'])
    length = len(plikes)
    print(length)
    idu = session['user_id']
    otherPerson = db.execute("SELECT * FROM messaging WHERE username = ?", username)
    return render_template("user.html", user=user, age=age, idu=idu, length=length, length2=length2, choice=choice, otherPerson=otherPerson)

@app.route("/unblocked/<username>")
@login_required
def unblocked(username):
    information = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    db.execute("DELETE FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", information[0]["username"], username)

    user = db.execute("SELECT userID,username, dob, gender, country, reason, registered, profileStatus, showPictureGuidelines FROM users WHERE username = ?", username)
    profile = db.execute("SELECT * FROM profile WHERE profile.userID = ?", user[0]["userID"])
    location = db.execute("SELECT country, state, city FROM contact WHERE contact.userID = ?", user[0]["userID"])
    prefs = db.execute("SELECT * FROM preference WHERE preference.userID = ?", user[0]["userID"])
    age = calcAge(user[0]['dob'])
    user.extend(profile)
    user.extend(location)
    user.extend(prefs)
    info = db.execute("SELECT * FROM users WHERE userID = ?", session['user_id'])
    plikes = db.execute("SELECT * FROM profileLikes WHERE fromMe = ? AND toUser = ?", info[0]['username'], username)

    blocked = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", info[0]["username"], username)
    length2 = len(blocked)
    choice = db.execute("SELECT * FROM messaging WHERE username = ?", info[0]['username'])
    length = len(plikes)
    print(length)
    idu = session['user_id']
    otherPerson = db.execute("SELECT * FROM messaging WHERE username = ?", username)
    return render_template("user.html", user=user, age=age, idu=idu, length=length, length2=length2, choice=choice, otherPerson=otherPerson)


@app.route("/unblockedpreferences/<username>")
@login_required
def unblockedpreferences(username):
    information = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    db.execute("DELETE FROM blockedUsers WHERE whoBlocked = ? AND whoGotBlocked = ?", information[0]["username"], username)
    information = []
    user = db.execute("SELECT * FROM users WHERE userID = ?", session["user_id"])
    info = db.execute("SELECT * FROM blockedUsers WHERE whoBlocked = ?", user[0]["username"])
    length = len(info)
    for x in range(length):
        info2 = db.execute("SELECT * FROM users WHERE username = ?", info[x]["whoGotBlocked"])
        information.append(info2)
    return render_template("blockedusers.html", user=user, info=info, length=length, information = information)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
