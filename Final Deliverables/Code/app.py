from flask import Flask,render_template,request,redirect, session, url_for,flash
import database,send_email,datetime,get_dates
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

register_email = send_email.Register()

db = database.Database()
date = get_dates.DateTime() 

app = Flask(__name__)
app.secret_key = "a very secret  key"

@app.route("/")
def index():
    return redirect(url_for('register'))

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

            register_email.get_email(email)
            register_email.SendDynamic()

            flash(" Successfully Registerd, Please login")
            return redirect(url_for("login"))
    else:
        return render_template('register.html')

@app.route("/login",methods = ['GET',"POST"])
def login():
    if request.method == 'POST':

        email = request.form['email_id']
        pwd = request.form['password']
        result = db.lg_view(email)

        if not result:
            return render_template('login.html',usr_error = "Email id does'nt exists!")
            
        if pwd != result:
            return render_template('login.html',usr_error = "Password doesn't match")
        else:
            session['loggedin'] = True
            session['username'] = email
            return redirect(url_for("dashboard"))
    else:
        return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    
    x_axis = date.get_week()
    y_axis = db.chart(x_axis) 

    fig =figure(
        x_range=x_axis,  
        title="Your Weekly Expenses",
        toolbar_location=None, 
        tools="",
        x_axis_label = "Dates of your Past 7 days",
        y_axis_label = "Amount you have spent"
        )

    fig.vbar(x=x_axis, top=y_axis, width=0.9)

    fig.xgrid.grid_line_color = None
    fig.y_range.start = 0

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)   
    email = session['username']
    user_id = db.uid_view(email)
    expense_table = db.expense_view(user_id)

    return render_template("dashboard.html",
        details = expense_table,
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources)

@app.route("/wallet",methods = ['GET',"POST"])
def wallet():
    try:
        email = session['username']
        if request.method == 'POST':
            
            user_id = db.uid_view(email)   
            expense_name = request.form['exp_name']
            amount = request.form['exp_amt']
            date = request.form['exp_date']

            db.wallet_insert(user_id,amount,expense_name,date)
            flash("Expense Added Successfully!!")
            return render_template('Wallet.html')
        else:
            return render_template('Wallet.html')
    except:
        flash('Login before you want to access wallet page')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("Logged out Successfully,please login again")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()
