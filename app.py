
from crypt import methods
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
    all_items = db.session.query(Items).all()
    return render_template('delete.html', all_items=all_items)

@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete_item(id):
    item = Items.query.filter_by(id=id).first()
    if request.method == "POST":
        item_to_delete = Items.query.get(id)
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/delete')
    return render_template('deleteitem.html', item=item)


@app.route('/update')
def update():
    all_items = db.session.query(Items).all()
    total_items = len(all_items)
    return render_template('update.html', all_items=all_items)

@app.route('/store')
def store():
    all_items = db.session.query(Items).all()
    return render_template('store.html', all_items=all_items)

@app.route('/update/<int:id>', methods=["POST","GET"])
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