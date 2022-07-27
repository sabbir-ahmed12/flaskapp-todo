from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/todo'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"#{self.id} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodos = Todo.query.all()
    return render_template('index.html', allTodos=allTodos)


@app.route('/completed')
def all_completed_todos():
    completed_todos = Todo.query.filter_by(is_completed=True).all()
    return render_template('completed.html', completed_todos=completed_todos)

@app.route('/completed/<int:id>')
def completed(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.is_completed = not todo.is_completed
    db.session.add(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


# TODO-1: Implement user login and logout feature.
# TODO-2: Implement paginate feature to display 5-10 todos in a page.