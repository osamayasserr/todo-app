import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instanciate the flask application
app = Flask(__name__)

# Configure the flask application
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{os.getenv('DB_PASS')}@localhost:5432/todoapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get the ORM database interface
db = SQLAlchemy(app)

# Instanciate the migration object
migrate = Migrate(app, db)


# The todos model (Table)
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f"<id: {self.id}, description: {self.description}>"


# Handle the '/' endpoint via the index function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:

            # Get the user's data submitted by the fetch (AJAX)
            description = request.get_json().get('description')

            # Create a Todo object and add it as pending
            todo = Todo(description)
            db.session.add(todo)
            db.session.commit()

        except Exception:

            # Undo any pending changes and log errors
            print(sys.exc_info())
            db.session.rollback()

        else:

            # Return the JSON response to the view
            return jsonify({
                'id': todo.id,
                'description': todo.description
            })

        finally:

            # Close the connection
            db.session.close()

    # Fetch all todos and update the view
    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', data=todos)


# Handle the '/check' endpoint via the index function
@app.route('/check/<id>', methods=['POST'])
def check(id):
    try:

        # Get the user's json data
        checked = request.get_json()['checked']

        # Update the todo with id = 'id'
        todo = Todo.query.get(id)
        todo.completed = checked
        db.session.commit()

    except Exception:

        # Undo any pending changes and log errors
        print(sys.exc_info())
        db.session.rollback()

    else:

        # Return the JSON response to the view
        return jsonify({
            'success': True
        })

    finally:

        # Close the conenection
        db.session.close()


# Run the flask application using the python interperter
if __name__ == "__main__":
    app.run(debug=True)
