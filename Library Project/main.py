from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7Cffdffggfg0sKR6b'

class Books(db.Model):
    # create the required fields/columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating


# Create the database
db.create_all()


# input records
# entry_data1 = Books(title='Benjamin books', author='Benji', rating='44.5')
# entry_data2 = Books(title='grishan', author='fgfgf', rating='90.6')
# Inserts records into a database table
# db.session.add(entry_data1)
# db.session.add(entry_data2)
# db.session.commit()

@app.route('/')
def home():
    return render_template('index.html', books=Books.query.all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        # input records
        entry_data = Books(title=data['name'], author=data['author'], rating=data['rating'])
        # add them to the db
        db.session.add(entry_data)
        # save them
        db.session.commit()
        flash('New record added')
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    book_id = id
    if request.method == 'POST':
        new_rating = request.form['new_rating']
        # get the specific book by id
        specific_book = Books.query.get(book_id)
        specific_book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    else:
        book_details = Books.query.get(book_id)
        title = book_details.title
        author = book_details.author
        rating = book_details.rating
        return render_template('edit.html', title=title, author=author, rating=rating, book_id=book_id)


@app.route('/<int:id>')
def delete(id):
    book_id = id
    # get the specific book by  id
    specific_book = Books.query.get(book_id)
    # then delete it
    db.session.delete(specific_book)
    # save changes in the db
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
