from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

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

@app.route('/')
def index():
    all_items = db.session.query(Items).all()
    return render_template('index.html', all_items=all_items)


if __name__ == '__main__':
    app.run(debug=True)