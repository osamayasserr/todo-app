import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Instanciate the flask application
app = Flask(__name__)

# Configure the flask application
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.getenv('DB_PASS')}@localhost:5432/todoapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get the ORM database interface
db = SQLAlchemy(app)


# The todos model (Table)
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f"<id: {self.id}, description: {self.description}>"


# Create the table in the database if it is not existing
db.create_all()


# Handle the '/' endpoint via the index function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        # Get the user's data submitted in the form
        description = request.form.get('description', '')

        # Create a Todo object and add it to the database
        todo = Todo(description)
        db.session.add(todo)
        db.session.commit()

        # Avoid leaving the last request as a POST
        return redirect(url_for('index'))

    # Fetch all todos and update the view
    todos = Todo.query.all()
    return render_template('index.html', data=todos)


# Run the flask application using the python interperter
if __name__ == "__main__":
    app.run(debug=True)
