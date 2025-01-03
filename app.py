from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
basedir = os.path.abspath('D:/FLASK')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todo.db')
db = SQLAlchemy(app)


class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(150), nullable=False)
    Desc = db.Column(db.String(350), nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SNo} - {self.Title}"


@app.route('/', methods=['POST', 'GET'])
def home():
    # todo=Todo(Title='First Todo', Desc='Start stufying mad2')
    # db.session.add(todo)
    # db.session.commit()
    if request.method == 'POST':
        print('post')

        title = request.form["title"]
        desc = request.form["desc"]

        todo = Todo(Title=title, Desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()

    return render_template('index.html', allTodo=allTodo)


@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)


@app.route('/delete/<int:SNo>', methods=['GET', 'POST'])
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:SNo>", methods=['GET', 'POST'])
def update(SNo):
    if request.method == 'POST':
        title = request.form["title"]
        desc = request.form["desc"]

        todo = Todo.query.filter_by(SNo=SNo).first()
        todo.Title = title
        todo.Desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(SNo=SNo).first()
    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)
