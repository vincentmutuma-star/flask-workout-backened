from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date
with app.app_context():
    db.drop_all(); db.create_all()
    e1=Exercise(name="Push Up", category="Strength", equipment_needed=False)
    e2=Exercise(name="Running", category="Cardio", equipment_needed=False)
    e3=Exercise(name="Yoga", category="Flexibility", equipment_needed=False)
    w1=Workout(date=date(2024,1,10), duration_minutes=45, notes="Morning")
    w2=Workout(date=date(2024,1,11), duration_minutes=30, notes="Cardio day")
    db.session.add_all([e1,e2,e3,w1,w2]); db.session.commit()
    we1=WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=3)
    we2=WorkoutExercise(workout_id=w2.id, exercise_id=e2.id, duration_seconds=1800)
    db.session.add_all([we1,we2]); db.session.commit()
    print("Seeded!")
