from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.date.today)
    mark = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Todo {self.content}>'

with app.app_context():
    db.init_app(app)
    db.create_all()
    



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_content = request.form.get('content')
        new_todo = Todo(content=todo_content)
        try:
            db.session.add(new_todo)
            db.session.commit()
        except:
            return 'There was an issue adding your task'
        return redirect('/')
    else:
        #Creating A List of Todos That are not done
        todoNotDone = Todo.query.filter_by(mark=False).all()
        todos = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', todos=todos, todoNotDone=todoNotDone)
    

#Deleting a task
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo_to_delete = Todo.query.get_or_404(todo_id)
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
    except:
        return 'There was a problem deleting that task'
    return redirect('/')

#Updating a task
@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update(todo_id):
    todoToUpdate = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todoToUpdate.content = request.form['content']
        try:
            db.session.commit()
        except:
            return 'There was a problem updating that todo'
        return redirect('/')
    else:
        #Creating A List of Todos That are not done
        todoNotDone = Todo.query.filter_by(mark=False).all()
        return render_template('update.html', todo=todoToUpdate)
    

#mark as done
@app.route('/mark/<int:todo_id>')
def mark(todo_id):
    todoToUpdate = Todo.query.get_or_404(todo_id)
    todoToUpdate.mark = not todoToUpdate.mark
    try:
        db.session.commit()
    except:
        return 'There was a problem marking that todo'
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


