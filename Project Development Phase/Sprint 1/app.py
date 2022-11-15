from flask import Flask,render_template,request,redirect
import database

db = database.Database()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register",methods = ['GET',"POST"])
def register():
    
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email_id']
        pwd = request.form['password']
        cpwd = request.form['confirm_pwd']
        
        if pwd != cpwd:    
            return render_template('register.html',usr_error = "Password does not match!")

        else:
            
            result = db.view(email)
            
            if result:
                return render_template('register.html',usr_error = "Email Id already Exists!")
            user_id = db.length_view() + 1
            db.insert(user_id,fname,lname,email,pwd)
            return redirect("login")
    else:
        return render_template('register.html')

@app.route("/login",methods = ['GET',"POST"])
def login():
    if request.method == 'POST':

        email = request.form['email_id']
        pwd = request.form['password']
        result = db.lg_view(email,pwd)

        if not result:
            return render_template('login.html',usr_error = "Email id does'nt exists!")
            
        if pwd != result[1]:
            return render_template('login.html',usr_error = "Password does'nt match")
        else:
            return redirect("dashboard")
    else:
        return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
