from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2
import psycopg2.extras

DB_NAME = 'kfc'
DB_USER = 'postgres'
DB_PASS = 'edgc2959'
DB_HOST = 'localhost'
DB_PORT = '5432'

app = Flask(__name__, template_folder='templates')
app.secret_key = 'edgc2959'



@app.route("/")
def home():
    return render_template('首頁.html')
  
@app.route("/首頁.html")
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
    user_id = get_user_id()
    user_name = get_user_name()
    phone = get_phone()
    email = get_email()
    sex = get_sex()
    birth = get_birth()
    return render_template('會員已登入.html', user_name=user_name ,phone = phone, email = email,user_id = user_id,sex = sex,birth = birth)

  
@app.route("/結帳.html")
def page_8():
    user_name = get_user_name()
    phone = get_phone()
    email = get_email()
    method = get_method()
    restaurant = get_rest()
    date = get_date()
    time = get_time()
    return render_template('結帳.html', user_name=user_name ,phone = phone, email = email, method = method, restaurant = restaurant, time = time, date = date)
  
@app.route("/購物車.html")
def page_9():
    return render_template('購物車.html')

@app.route("/餐車.html")
def page_10():
    return render_template('餐車.html')
  
@app.route("/餐點內容.html")
def page_11():
    food_name = get_food_name()
    suit_price = get_suit_price()
    food_content = get_food_content()
    return render_template('餐點內容.html', food_name=food_name, suit_price=suit_price, food_content=food_content)

@app.route("/首頁2.html")
def page_12():
    return render_template('首頁2.html')

@app.route("/單點.html")
def page_13():
    return render_template('單點.html')

@app.route("/修改資料.html")
def page_14():
    Acc=get_phone() or get_email()
    return render_template('修改資料.html',Acc = Acc)

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
        if not all([mobile_phone, email, password, name, sex, birthday]):
            flash("未填寫所有欄位。", 'error')

        else:
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
                INSERT INTO user_table (phone, email, pwd, user_name, sex, birth)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (mobile_phone, email, password, name, sex, birthday))

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
            stored_password = existing_user['pwd']
            if password == stored_password:
                # 登錄成功，將 user_id 存儲到 session 中
                session['user_id'] = existing_user['user_id']

                
                conn.commit()
                conn.close()
                return redirect('/首頁2.html')
            else:
                conn.close()
                return render_template('會員登入.html', error_message=2)
        else:
            conn.close()
            return render_template('會員登入.html', error_message=1)

    return render_template('會員登入.html')

def get_method():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT pickup_method FROM order_detail ORDER BY order_id DESC LIMIT 1;")
        first_row = cur.fetchone()
        if first_row:
            pickup_method = first_row['pickup_method']
            return pickup_method
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving pickup method:", e)
    finally:
        cur.close()
        conn.close()
        
def get_date():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT order_date FROM order_detail ORDER BY order_id DESC LIMIT 1;")
        first_row = cur.fetchone()
        if first_row:
            date = first_row['order_date']
            return date
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving pickup method:", e)
    finally:
        cur.close()
        conn.close()
        
def get_time():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT order_time FROM order_detail ORDER BY order_id DESC LIMIT 1;")
        first_row = cur.fetchone()
        if first_row:
            time = first_row['order_time']
            return time
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving pickup method:", e)
    finally:
        cur.close()
        conn.close()
        
def get_rest():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT address FROM order_detail ORDER BY order_id DESC LIMIT 1;")
        first_row = cur.fetchone()
        if first_row:
            address = first_row['address']
            return address
        else:
            return None
    except psycopg2.Error as e:
        print("Error retrieving pickup method:", e)
    finally:
        cur.close()
        conn.close()

# 定義函數以獲取 user_name
def get_user_name():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT user_name FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['user_name']

    conn.close()
    return None

def get_phone():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT phone FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['phone']

    conn.close()
    return None

def get_email():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT email FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['email']

    conn.close()
    return None

def get_user_id():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT user_id FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['user_id']

    conn.close()
    return None

def get_sex():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT sex FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['sex']

    conn.close()
    return None

def get_birth():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT birth FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['birth']

    conn.close()
    return None

def get_pwd():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user_id = session.get('user_id', None)

    if user_id:
        cur.execute("SELECT pwd FROM user_table WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        if user:
            return user['pwd']

    conn.close()
    return None




@app.route("/forgetpass", methods=['GET', 'POST'])
def forgetpass():
    if request.method == 'POST':
        account = request.form['acc']
        
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("SELECT * FROM user_table WHERE email = %s OR phone = %s", (account, account))
        existing_user = cur.fetchone()
        
        if existing_user:
            return render_template('修改資料.html')
        else:
            conn.close()
            return render_template('忘記密碼.html', message=2)
        
@app.route("/changepass", methods=['GET', 'POST'])
def changepass():
    if request.method == 'POST':
        password = request.form['pwd']
    #    sex = request.form['sex']
   #     birth = request.form['birth']
        phone = request.form['phone']
        email = request.form['email']
        user_name = request.form['user_name']
        account = request.form['acc']

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
                    UPDATE user_table
                    SET pwd = %s,
                        phone = %s,
                        email = %s,
                        user_name = %s
                    WHERE email = %s OR phone = %s
                """, (password,  phone, email, user_name, account, account))
        
        

        conn.commit()
        conn.close()
        return render_template('會員登入.html')
    

    
@app.route('/order_detail', methods=["GET", 'POST'])
def order_detail():
    if request.method == 'POST':
        data = request.get_json()
        restaurant = data.get('restaurant')
        date = data.get('date')
        time = data.get('time')
        method = data.get('method')
        
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        
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
        
   


@app.route("/suit", methods=['GET', 'POST'])
def main():
    get_food_name_result = get_food_name()
    get_suit_price_result = get_suit_price()
    suit_result = suit()
    get_food_content_result = get_food_content()

    return f'{get_food_name_result} | {get_suit_price_result} | {suit_result}  | {get_food_content_result}'
    

def suit():
    if request.method == 'POST':
        套餐 = request.form['套餐']

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()

    

        cur.execute("""INSERT INTO suit_table (suit_name) VALUES (%s)""", (套餐,))  # Use the variable 套餐1 here

        

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        food_name = get_food_name()
    suit_price = get_suit_price()
    return render_template('餐點內容.html', food_name=food_name, suit_price=suit_price)
    
def get_food_name():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT suit_name FROM suit_table ORDER BY suit_id DESC LIMIT 1;")
        food = cur.fetchone()
        if food:
            name = food['suit_name']
            return name
        else:
            print('None')
            return None
    finally:
        cur.close()
        conn.close()
 
  
def get_suit_price():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:

        food_name = get_food_name()
        cur.execute("SELECT suit_price FROM suit_id WHERE suit_name = %s",(food_name,))
        food = cur.fetchone()

        if food:
            price = food['suit_price']
            return price
        else:
            return None
    finally:
        cur.close()
        conn.close()

def get_food_content():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        
        food_id = get_food_id()
        cur.execute("SELECT food_name FROM food_content JOIN suit_id ON food_id = id WHERE food_id = %s ;" % (food_id,))
        food = cur.fetchall()

        food_content = [item[0] for item in food]
        print(food_content[0])
        content1 = food_content[0]
        return content1

    finally:
        cur.close()
        conn.close()

def get_food_id():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        food_name = get_food_name()
        cur.execute("SELECT id FROM suit_id WHERE suit_name = %s",(food_name,))
        food = cur.fetchone()
        if food:
            id = food['id']
            return id
        else:
            print('None')
            return None
    finally:
        cur.close()
        conn.close()