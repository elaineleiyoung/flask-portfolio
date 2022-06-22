import os
from flask import Flask, render_template, request, abort
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

STAR_USER_INFO = {
    'hobbies':{
        'hobby 1': ['logo.jpg'],
        'hobby 2': ['smallcats.png'],
        'hobby 3': ['logo.jpg'],
        'hobby 4': ['smallcats.png']
     },
    'experiences':{
        'Software Developer Intern @ RBC': ['Currently working on improving IAM processes with a security team of 10'],
        'Meta x MLH Production Engineer Fellow': ['Creating a flask website using Jinja with a portfolio', 'Learning how to use Python and Flask to create a webpage!']
    },
    'education':{
        'University of Waterloo': ['waterloo.jpg'],
        'Pierre Elliott Trudeau High School': ['peths.jpg']
    },
    'images':[
        'waterloo.jpg',
        'peths.jpg'
    ]
}

ELAINE_USER_INFO = {
        'hobbies':{
        'hobby 1': ['logo.jpg'],
        'hobby 2': ['smallcats.png'],
        'hobby 3': ['logo.jpg'],
        'hobby 4': ['smallcats.png']
     },
    'experiences':{
        'Teaching Assistant': ['Graded exams and homework for the classes Geometry, Algebra 2, Precalculus, and SAT preparatory',
                'Documented and tracked students’ assignments and scores using spreadsheets',
                'Communicated with students']
    },
    'education':{
        'Boston University': ['bu.jpg'],
        'Mission San Jose High School': ['msj.jpg']
    },
    'images':[
        'logo.jpg',
        'smallcats.png'
    ]
}

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/elaine_about')
def about():
    return render_template('elaine_about.html', user = ELAINE_USER_INFO)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/education')
def education():
    return render_template('education.html', user = STAR_USER_INFO)

@app.route('/star_about')
def star_about():
    return render_template('star_about.html', user = STAR_USER_INFO)

@app.route('/countries')
def countries():
    return render_template('countries.html')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', user = STAR_USER_INFO)
