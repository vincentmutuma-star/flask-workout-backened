from flask import Flask, request, make_response
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import *
from marshmallow import ValidationError
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)
db.init_app(app)
@app.route("/")
def index():
    return "<h1>Workout API - Flask SQLAlchemy Workout Application</h1>"
@app.route("/workouts")
def get_workouts():
    return make_response(workouts_schema.dump(Workout.query.all()), 200)
@app.route("/workouts/<int:id>")
def get_workout(id):
    w = Workout.query.filter_by(id=id).first()
    if not w: return make_response({"error":"Workout not found"},404)
    return make_response(workout_schema.dump(w),200)
@app.route("/workouts", methods=["POST"])
def post_workout():
    try:
        data = workout_schema.load(request.get_json())
        w = Workout(**data); db.session.add(w); db.session.commit()
        return make_response(workout_schema.dump(w),201)
    except ValidationError as e: return make_response({"errors":e.messages},400)
@app.route("/workouts/<int:id>", methods=["DELETE"])
def del_workout(id):
    w=Workout.query.get(id)
    if not w: return make_response({"error":"Not found"},404)
    db.session.delete(w); db.session.commit(); return make_response({},204)
@app.route("/exercises")
def get_exercises(): return make_response(exercises_schema.dump(Exercise.query.all()),200)
@app.route("/exercises/<int:id>")
def get_exercise(id):
    e=Exercise.query.get(id)
    if not e: return make_response({"error":"Not found"},404)
    return make_response(exercise_schema.dump(e),200)
@app.route("/exercises", methods=["POST"])
def post_exercise():
    try:
        data=exercise_schema.load(request.get_json())
        e=Exercise(**data); db.session.add(e); db.session.commit()
        return make_response(exercise_schema.dump(e),201)
    except ValidationError as e: return make_response({"errors":e.messages},400)
@app.route("/exercises/<int:id>", methods=["DELETE"])
def del_exercise(id):
    e=Exercise.query.get(id)
    if not e: return make_response({"error":"Not found"},404)
    db.session.delete(e); db.session.commit(); return make_response({},204)
@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>", methods=["POST"])
def add_ex_to_workout(workout_id, exercise_id):
    data=request.get_json(); data["workout_id"]=workout_id; data["exercise_id"]=exercise_id
    try:
        validated=workout_exercise_schema.load(data)
        we=WorkoutExercise(**validated); db.session.add(we); db.session.commit()
        return make_response(workout_exercise_schema.dump(we),201)
    except ValidationError as e: return make_response({"errors":e.messages},400)
if __name__ == "__main__": app.run(port=5555, debug=True)
