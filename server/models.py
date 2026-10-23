from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
metadata = MetaData(naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"})
db = SQLAlchemy(metadata=metadata)
class Exercise(db.Model, SerializerMixin):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
    serialize_rules = ("-workout_exercises.exercise",)
    __table_args__ = (db.CheckConstraint("length(name) >= 3", name="name_length_constraint"), db.CheckConstraint("category IN (\"Strength\",\"Cardio\",\"Flexibility\",\"Balance\")", name="category_check"),)
    @validates("name")
    def validate_name(self, k, v):
        if not v or len(v.strip()) < 3: raise ValueError("Name must be >=3 chars")
        return v.strip()
    @validates("category")
    def validate_cat(self, k, v):
        if v not in ["Strength","Cardio","Flexibility","Balance"]: raise ValueError("Invalid category")
        return v
class Workout(db.Model, SerializerMixin):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    serialize_rules = ("-workout_exercises.workout",)
    __table_args__ = (db.CheckConstraint("duration_minutes > 0 AND duration_minutes <= 300", name="duration_check"),)
    @validates("duration_minutes")
    def validate_duration(self, k, v):
        if v <= 0: raise ValueError("Duration must be >0")
        return v
class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = "workout_exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")
    serialize_rules = ("-workout.workout_exercises","-exercise.workout_exercises",)
    __table_args__ = (db.CheckConstraint("reps IS NULL OR reps > 0", name="reps_check"), db.CheckConstraint("sets IS NULL OR sets > 0", name="sets_check"),)
    @validates("sets","reps","duration_seconds")
    def validate_pos(self, k, v):
        if v is not None and v <= 0: raise ValueError(f"{k} must be >0")
        return v
