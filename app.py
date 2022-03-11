from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

# set up Flask app configuration

app = Flask(__name__)
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# each entry in the database is a Todo item
class Todo(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String(100))
     description = db.Column(db.String(200))
     # use status to track todo/doing/done status and to filter display
     status = db.Column(db.Integer)

# upon setup create a single todo item to display
def create_todo(*args, **kwargs):
    db.session.add(Todo(title = "Buy concert tickets.", description = "Tour tickets out at NOON on SATURDAY!!! Don't forget!", status = 1))
    db.session.commit()
event.listen(Todo.__table__, 'after_create', create_todo)

# set up index page, display all items by status
@app.route("/")
def index():
    todo_items = Todo.query.filter_by(status = 1).all()
    doing_items = Todo.query.filter_by(status = 2).all()
    done_items = Todo.query.filter_by(status = 3).all()
    # render HTML template, pass todo items
    return render_template('index.html', todo_items = todo_items, doing_items = doing_items, done_items = done_items)

# add new todo item using POST method
@app.route("/add", methods=["POST"])
def add():
    # get item fields from request form
    title = request.form.get("title")
    description = request.form.get("description")
    # add new todo item
    new_todo = Todo(title = title, description = description, status = 1)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

# change an item's status to todo
@app.route("/updatetodo/<int:todo_id>")
def updatetodo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status = 1
    db.session.commit()
    return redirect(url_for("index"))

# change an item's status to doing
@app.route("/updatedoing/<int:todo_id>")
def updatedoing(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status = 2
    db.session.commit()
    return redirect(url_for("index"))

# change an item's status to done
@app.route("/updatedone/<int:todo_id>")
def updatedone(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status = 3
    db.session.commit()
    return redirect(url_for("index"))

# delete an item
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
