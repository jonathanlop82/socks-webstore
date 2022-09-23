
from crypt import methods
from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from flask_bcrypt import Bcrypt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from datetime import datetime

login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///socks-store.db"
db = SQLAlchemy(app)

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    image = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Items %r>' % self.name

db.create_all()

# user = User( email="jonathanlop82@gmail.com", password=bcrypt.generate_password_hash('J2n1th1n')) 
# db.session.add(user)
# db.session.commit()


year = datetime.now().year


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.

    """
    # print db
    # form = LoginForm()
    if request.method == "POST":
        user = User.query.get(request.form.get("email"))
        if user:
            if bcrypt.check_password_hash(user.password, request.form.get("password")):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect( url_for('index'))

@app.route('/')
def index():
    all_items = db.session.query(Items).all()
    total_items = len(all_items)
    return render_template('index.html', all_items=all_items, total_items=total_items)

@app.route('/add', methods=("POST","GET"))
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name")
        url_image = request.form.get("urlimage")
        price = request.form.get("price")
        new_item = Items(name=name, image=url_image, price=price)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/delete')
@login_required
def delete():
    all_items = db.session.query(Items).all()
    return render_template('delete.html', all_items=all_items)

@app.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def delete_item(id):
    item = Items.query.filter_by(id=id).first()
    if request.method == "POST":
        item_to_delete = Items.query.get(id)
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/delete')
    return render_template('deleteitem.html', item=item)


@app.route('/update')
@login_required
def update():
    all_items = db.session.query(Items).all()
    total_items = len(all_items)
    return render_template('update.html', all_items=all_items)

@app.route('/store')
def store():
    all_items = db.session.query(Items).all()
    return render_template('store.html', all_items=all_items)

@app.route('/update/<int:id>', methods=["POST","GET"])
@login_required
def update_item(id):
    if request.method == "POST":
        item_to_update = Items.query.get(id)
        item_to_update.name = request.form.get("name")
        item_to_update.image = request.form.get("urlimage")
        item_to_update.price = request.form.get("price")
        db.session.commit()
        return redirect('/update')
    item = Items.query.filter_by(id=id).first()
    return render_template('updateitem.html', item=item)



if __name__ == '__main__':
    app.run(debug=True)