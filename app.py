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


# The categories model (Table)
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', backref='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<id: {self.id}, name: {self.name}>"


# The todos model (Table)
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)

    def __init__(self, description, category_id):
        self.description = description
        self.category_id = category_id

    def __repr__(self):
        return f"<id: {self.id}, description: {self.description}>"


# Render the homepage HTML
@app.route('/')
def index():
    return redirect(url_for('get_todos', category_id=1))


# Render the todos with specific category id
@app.route('/categories/<int:category_id>')
def get_todos(category_id):

    # Fetch all todos with id = 'id'
    todos = Todo.query.filter(
        Todo.category_id == category_id).order_by(Todo.id).all()

    # Fetch all categories
    categories = Category.query.all()
    active_category = Category.query.get(category_id)
    return render_template(
        'index.html', todos=todos, categories=categories, active_category=active_category)


# Create a new categorized todo item
@app.route('/categories/<int:category_id>/todos', methods=['POST'])
def create_todo(category_id):
    try:

        # Get the user's data submitted by the fetch (AJAX)
        description = request.get_json().get('description')

        # Create a Todo object and add it as pending
        todo = Todo(description, category_id)
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
            'description': todo.description,
            'category_id': todo.category_id
        })

    finally:
        db.session.close()


# Update the completed state of a todo usnig PATCH
@app.route('/todos/<int:id>', methods=['PATCH'])
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

        # Return a success message to the view
        return jsonify({
            'success': True
        })

    finally:
        db.session.close()


# Delete a specific todo by id using DELETE
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:

        # Perform a delete of the todo in the database
        Todo.query.filter(Todo.id == id).delete()
        db.session.commit()

    except Exception:

        # Undo any pending changes and log errors
        print(sys.exc_info())
        db.session.rollback()

    else:

        # Return a success message
        return jsonify({
            'id': id,
            'success': True
        })

    finally:
        db.session.close()


# Run the flask application using the python interperter
if __name__ == "__main__":
    app.run(debug=True)
