from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import psycopg2

DB_NAME = 'kfc'
DB_USER = 'postgres'
DB_PASS = 'william1018'
DB_HOST = 'localhost'

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('首頁.html')
  
@app.route("/首頁")
def 首頁():
    return render_template('首頁.html')

@app.route("/個人餐.html")
def home1():
    return render_template('個人餐.html')


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
        cpassword = request.form['cPassword']
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

        # Check if email or phone already exists in the database
        cur.execute("SELECT * FROM user_table WHERE email = %s OR phone = %s", (email, mobile_phone))
        existing_user = cur.fetchone()
        
        if existing_user:
            conn.close()
            return render_template('資料重複.html')

        # Insert data into the database
        cur.execute("""
            INSERT INTO user_table (phone, email, pwd, user_name, sex, birth, on_line)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (mobile_phone, email, password, name, sex, birthday, False))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to a new page or render a template with a success message
        return render_template('會員登入.html')

    # If the request is GET, just render the registration form
    return render_template('加入會員.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form['acc']
        password = request.form['pw']

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT * FROM user_table WHERE email = %s OR phone = %s", (account, account))
        existing_user = cur.fetchone()
        
        if existing_user:
            # 如果帳戶符合電子郵件或手機號碼，則檢查密碼是否相符
            stored_password = existing_user['pwd']  # 假設 'password' 是資料表中的欄位名稱
            if password == stored_password:
                
                cur.execute("""
                    UPDATE user_table
                    SET on_line = %s
                    WHERE on_line = %s
                """, (True, False))

                conn.commit()
                conn.close()
                return render_template('首頁.html')  # 如果密碼相符，則呈現成功頁面
            else:
                conn.close()
                return render_template('會員登入.html', error_message=2)
        else:
            conn.close()
            return render_template('會員登入.html', error_message=1)

@app.route("/forgetpass", methods=['GET', 'POST'])
def forgetpass():
    if request.method == 'POST':
        account = request.form['acc']
        
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT * FROM user_table WHERE email = %s OR phone = %s", (account, account))
        existing_user = cur.fetchone()
        
        if existing_user:
            return render_template('修改密碼.html', Acc=account)
        else:
            conn.close()
            return render_template('忘記密碼.html', message=2)
        
@app.route("/changepass", methods=['GET', 'POST'])
def changepass():
    if request.method == 'POST':
        password = request.form['pwd']
        account = request.form['acc']

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
                    UPDATE user_table
                    SET pwd = %s
                    WHERE email = %s OR phone = %s
                """, (password, account, account))

        conn.commit()
        conn.close()
        return render_template('會員登入.html')
    
@app.route('/order_detail', methods=["GET", 'POST'])
def order_detail():
    print("a")
    if request.method == 'POST':
        print("b")
        data = request.get_json()
        restaurant = data.get('restaurant')
        date = data.get('date')
        time = data.get('time')
        method = data.get('method')
        
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        try:
            cur.execute("""
                INSERT INTO order_detail (pickup_method, address, order_date, order_time)
                VALUES (%s, %s, %s, %s)
            """, (method, restaurant, date, time))

            conn.commit()
            cur.close()
            conn.close()
            
            return render_template('個人餐.html')
        
        except Exception as e:
            return f"Error: {str(e)}"
if __name__ == "__main__":
    app.run(debug=True)
