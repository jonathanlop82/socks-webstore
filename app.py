
from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///socks-store.db"
db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    image = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Items %r>' % self.name

db.create_all()

# item = Items(name='Sock One', image='https://knousshe.sirv.com/Images/1.jpeg', price='5.00')
# db.session.add(item)
# db.session.commit()

# item = Items(name='Sock Two', image='https://knousshe.sirv.com/Images/2.jpeg', price='5.50')
# db.session.add(item)
# db.session.commit()

# item = Items(name='Sock Three', image='https://knousshe.sirv.com/Images/3.jpeg', price='4.50')
# db.session.add(item)
# db.session.commit()

year = datetime.now().year

@app.route('/')
def index():
    all_items = db.session.query(Items).all()
    total_items = len(all_items)
    return render_template('index.html', all_items=all_items, total_items=total_items)

@app.route('/add', methods=("POST","GET"))
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
def delete():
    return render_template('delete.html')


@app.route('/update')
def update():
    all_items = db.session.query(Items).all()
    total_items = len(all_items)
    return render_template('update.html', all_items=all_items)

@app.route('/store')
def store():
    all_items = db.session.query(Items).all()
    return render_template('store.html', all_items=all_items)


if __name__ == '__main__':
    app.run(debug=True)