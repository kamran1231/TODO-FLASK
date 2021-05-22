

from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(400),nullable=False)
    date_created = db.Column(db.DateTime,default= datetime.utcnow)

    def __repr__(self):
        return f'{self.sno}--{self.title}'


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']


        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    print(alltodo)

    return  render_template('index.html',alltodo=alltodo)
    # return 'Hello, World!'

@app.route('/delete/<int:sno>')
def delete_todo(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()

    db.session.delete(alltodo)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:sno>',methods=['GET','POST'])
def edit_todo(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')


    todo = Todo.query.filter_by(sno=sno).first()

    return render_template('update.html',todo=todo)



@app.route('/show')
def product():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is product page'

if __name__ == "__main__":
    app.run(debug=True)