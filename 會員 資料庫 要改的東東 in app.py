from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras




DB_NAME = 'kfc會員'
DB_USER = 'postgres'
DB_PASS = 'Leo48923554'
DB_HOST = 'localhost'

app = Flask(__name__, template_folder='templates')


@app.route("/")
def home():
    return render_template('首頁.html')
  
@app.route("/首頁")
def firstpage():
    return render_template('首頁.html')

@app.route("/個人餐.html")
def home1():
    return render_template('個人餐.html')


@app.route("/會員.html")
def page_one():
    return render_template('會員.html')

@app.route("/多人餐.html")
def page_2():
    return render_template('多人餐.html')
  
@app.route("/早餐.html")
def page_3():
    return render_template('早餐.html')
  
@app.route("/加入會員.html")
def page_4():
    return render_template('加入會員.html')

@app.route("/忘記密碼.html")
def page_5():
    return render_template('忘記密碼.html')

@app.route("/會員登入.html")
def page_6():
    return render_template('會員登入.html')
  
@app.route("/會員已登入.html")
def page_7():
    return render_template('會員已登入.html')
  
@app.route("/結帳.html")
def page_8():
    return render_template('結帳.html')
  
@app.route("/購物車.html")
def page_9():
    return render_template('購物車.html')
  
@app.route("/餐車.html")
def page_10():
    return render_template('餐車.html')
  
@app.route("/餐點內容.html")
def page_11():
    return render_template('餐點內容.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        # Extract data from form
        mobile_phone = request.form['MobilePhone']
        email = request.form['Email']
        password = request.form['Password']
        name = request.form['Name']
        sex = request.form['Sex']
        birthday_y = request.form['BirthdayY']
        birthday_m = request.form['BirthdayM']
        birthday_d = request.form['BirthdayD']
        # You would construct the birthday from the three components here
        birthday = f"{birthday_y}-{birthday_m}-{birthday_d}"

        # Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


        # Insert data into the database
        cur.execute("""
            INSERT INTO user_table (phone, email, pwd, user_name, sex, birth)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (mobile_phone, email, password, name, sex, birthday))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to a new page or render a template with a success message
        return render_template('registration_success.html')

    # If the request is GET, just render the registration form
    return render_template('加入會員.html')


