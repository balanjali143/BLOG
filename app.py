from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from cmail import sendmail
from otp import genotp
app=Flask(__name__)
app.config['SECRET_KEY']='my secret_key that no one to know'
mydb=mysql.connector.connect(host="localhost",user="root",password="system001",db="blog")
with mysql.connector.connect(host="localhost",user="root",password="system001",db="blog"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists reg(name varchar(20) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
    cursor.execute("create table if not exists posts(id int,title varchar(255),content text,date_posted datetime,slug varchar(255),poster_id int)")
mycursor=mydb.cursor()
@app.route("/regform",methods=["GET","POST"])
def reg():
    if request.method=="POST":
        name=request.form.get('name')
        mobile=request.form.get('mobile')
        email=request.form.get('email')
        address=request.form.get('address')
        password=request.form.get('password')
        otp=genotp()
        sendmail(to=email,subject='THANK YOU for Registration',body=f'otp is : {otp}')
        return render_template('verification.html',name=name,mobile=mobile,email=email,address=address,password=password,otp=otp)
    return render_template("registration.html")
@app.route('/otp/<name>/<mobile>/<email>/<address>/<password>/<otp>',methods=['GET','POST'])
def otp(name,mobile,email,address,password,otp):
    if request.method=='POST':
        uotp=request.form['uotp']
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("insert into reg values(%s,%s,%s,%s,%s)",[name,mobile,email,address,password])
            mydb.commit()
            cursor.close()  
            return redirect(url_for('login'))
    return render_template('verification.html',name=name,mobile=mobile,email=email,address=address,password=password,otp=otp)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        name=request.form.get('name')
        password=request.form.get('password')
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from reg where name=%s && password=%s",[name,password])
        data=cursor.fetchone()[0]
        print(data)
        if data==1:
            session['name']=name
            if not session.get(session['name']):
                session[session['name']]={}
            return redirect(url_for('homepage'))
        else:
            return 'Invalid username and password'    
    return render_template('login.html')
@app.route('/logout')
def logout():
    return redirect(url_for('login'))
@app.route('/')
def homepage():
    return render_template('homepage.html')
@app.route('/addpost',methods=['GET','POST'])
def addpost():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("insert into posts(title,content,slug) values(%s,%s,%s)",(title,content,slug))
        mydb.commit()
        cursor.close()  
        return redirect(url_for('view_post'))
    return render_template('addpost.html')

#create admin page
@app.route('/admin')
def admin():
    return  render_template('admin.html')
@app.route('/viewpost')
def view_post():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT * FROM posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['GET','POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM posts where id=%s",(id,))
    posts=cursor.fetchone()
    cursor.execute('DELETE FROM posts WHERE id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for("view_post"))
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("UPDATE posts SET title=%s,content=%s,slug=%s where id=%s",(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('view_post'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute("SELECT * FROM posts where id=%s",(id,))
        posts=cursor.fetchone()
        cursor.close()
        return render_template('update.html',post=posts)
app.run(debug=True,use_reloader=True) 