from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET"] = "enijwneicjwoenmcuiw"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
all_books_old = []


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), unique=True, nullable=False)
    author = db.Column(db.String(280), nullable=False)
    rating = db.Column(db.Float(5), nullable=False)


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Books(title=request.values.get("name"),
                         author=request.values.get("author"),
                         rating=request.values.get("rating"))
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")

    return render_template("add.html")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    url_id = request.args.get("id")

    if request.method == "POST":
        book_to_update = Books.query.get(url_id)
        book_to_update.rating = request.values.get("new_rating")
        db.session.commit()
        return redirect("/")

    elif url_id is not None:
        book_to_update = Books.query.get(url_id)
        if request.method == ["POST"]:
            book_to_update.rating = request.values.get("new_rating")
            db.session.commit()
            return redirect("/")
        return render_template("edit.html", title=book_to_update.title, rating=book_to_update.rating, url_id=url_id)

    else:
        return redirect("/")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    book_to_delete = Books.query.get(post_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
