import os
from flask import Flask, render_template, request, abort, Response
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta: 
            database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])
print(mydb)
#

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
        'Exploring the city': ['boston.jpg'],
        'Playing': ['golf.jpg'],
        'Visiting cafes': ['cafe.jpg'],
        'Finding new music': ['music.jpg']
     },
    'experiences':{
        'Teaching Assistant': ['Graded exams and homework for the classes Geometry, Algebra 2, Precalculus, and SAT preparatory',
                'Documented and tracked students’ assignments and scores using spreadsheets',
                'Communicated with students regularly about progress through weekly emails'], 
        'Meta x MLH Production Engineer Fellow': ['Creating a flask website using Jinja with a portfolio', 'Learning how to use Python and Flask to create a webpage!']
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

@app.route('/education')
def education():
    return render_template('education.html', user = STAR_USER_INFO)

@app.route('/star_about')
def star_about():
    return render_template('star_about.html', user = STAR_USER_INFO)

@app.route('/elaine_about')
def about():
    return render_template('elaine_about.html', user = ELAINE_USER_INFO)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', user = ELAINE_USER_INFO)

@app.route('/timeline')
def timeline():
    posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

    return render_template('timeline.html', title = "Timeline", url=os.getenv("URL"), posts=posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    #fixing test cases
    if 'name' not in request.form:
        return Response("Invalid name", status=400)
    if 'email' not in request.form or '@' not in request.form['email']:
        return Response("Invalid email", status=400)
    if 'content' not in request.form or request.form['content'] == '':
        return Response("Invalid content", status=400)
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
   temp = [
	model_to_dict(p)
	for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
   
   return {
       'timeline_posts': temp }
       
@app.route("/api/timeline_post/<id>", methods=["DELETE"])
def delete_time_line_post(id):
    data = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    counter = 1
    for post in data:
        if counter == int(id):
            post.delete_instance()
            break
        else:
            counter += 1
   
    return "Post deleted"



