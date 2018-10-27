from flask import Flask,render_template,request,redirect,session,url_for
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

#数据库相关
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # truename = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    # sex = db.Column(db.String(80), unique=True, nullable=False)
    

def __repr__(self):
    return '<User %r>' % self.truename
#创建表
#db.create_all()



@app.route('/',methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        uemail = request.form.get('email')
        upassword = request.form.get('password')
        # user = User.query.filter(User.username == username, User.password == password).first()
        user = User.query.filter(User.email == uemail).first()
        if user and upassword == user.password:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session.permanent = True
            return redirect(url_for("blog_main"))
        else:
            flash('用户名或密码不正确,请检查!')
            return render_template('login.html')


@app.route("/blog_main")
def blog_main():
    return render_template("blog_main.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        #获取数据
        uemail = request.form.get('email')
        # utruename = request.form.get('truename')
        upassword = request.form.get('password')
        # uage = request.form.get('age')
        if User.query.filter(User.email==uemail).first():
            flash("账号已存在，请重新注册")
        else:
            #转存数据库
            newmes = User(email=uemail,password=upassword)
            db.session.add(newmes)
            #提示注册成功和返回登陆页面
            flash("注册成功请登录")
            return redirect(url_for('login'))
    return render_template("/register.html")

if __name__=="__main__":
    app.run(debug=True)
