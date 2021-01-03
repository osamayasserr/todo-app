from flask import Flask, render_template

# Instanciate the flask application
app = Flask(__name__)


# Handle the '/' endpoint via the index function
@app.route('/')
def index():
    return render_template('index.html', data=['todo 1', 'todo 2', 'todo 3'])


# Run the flask application using python interperter
if __name__ == "__main__":
    app.run(debug=True)
