from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# python -m pip install psycopg2 # to install psycopg2

app = Flask(__name__)

# python dictionary
app.config.update(
    #SECRET_KEY = 'neymar12345678',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:neymar12345678@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

# We can add multiple routes to the weblink
@app.route('/index') # localhost:5000/index
@app.route('/') # localhost:5000
def hello_flask():
    return 'Hello flask!'

### HAVE QUERY STRING ###
@app.route('/new/')
# Here we key in a default value greeting='hello', so if user don't key in any value, it will be hello (need to add in query_val also)
def query_strings(greeting = 'hello'):
    # Take in a variable key in by user and store it in query_val
    query_val = request.args.get('greeting', greeting)   # localhost:5000/new/?greeting=hola!
    # Then display the value in the browser
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

### NO QUERY STRING ###
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='mina'): # Need a default value inside, #http://localhost:5000/user/
    return '<h1> hello there ! {} </h1>'.format(name)

### 1) STRING: DEFAULT DATA TYPE IS ALWAYS STRING ###
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'

### 2) NUMBERS: need to convert numbers to string ###
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> the number you picked is ' + str(num) + '</h1>'

### NUMBERS ###
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1>the sum is : {}'.format(num1 + num2) + '</h1>'

### 3) FLOATS ###
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return '<h1> the product is {}'.format(num1 * num2) + '</h1>'

### USING TEMPLATES ###
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

### JINJA TEMPLATES ###
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon deomn',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']

    return render_template('movie.html',
                           movies=movie_list,
                           name='Harry')

@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                  'neon deomn': 3.20,
                  'ghost in a shell': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.48}

    return render_template('table_data.html',
                           movies=movies_dict,
                           name='Sally')

@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                  'neon deomn': 3.20,
                  'ghost in a shell': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')

@app.route('/countries')
def countries_data():
    countries_dict = {"United States":325084756,
                      "China":1421021791,
                      "Japan":127502725,
                      "Germany":82658409,
                      "India":1338676785}

    return render_template('countries.html',
                           countries_d = countries_dict)

# Instead of using CREATE_TABLE in sql, we can use class in python
class Publication(db.Model):
    __tablename__ = 'publication'  # Name of the table we going to create

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)

    # __init__(): called when new instances are created
    # self indicates an instance that we are creating on any class
    def __init__(self, id, name):
        self.id = id
        self.name = name

    # __repr__(): string representation of an instance
    def __repr__(self):
        return 'The id is {}, Name is {}'.format(self.id, self.name)

@app.route('/bmi_calculator', methods=['GET','POST'])
def bmi_calculator():
    # if a form is submitted
    if request.method == "POST":

        # Get values through input bars
        height = request.form["Height"]
        weight = request.form["Weight"]
        if weight is None:
            height = "Not Submitted"
        if weight is None:
            weight = "Not Submitted"

        # Define BMI formula
        bmi = float(weight)/(float(height)**2)
    else:
        bmi = ""

    return render_template("bmi_calculator.html", output = bmi)


if __name__ == '__main__':
    db.create_all() # Creates all the table if it doesn't exist already
    app.run(debug=True)

