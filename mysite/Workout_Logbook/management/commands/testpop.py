from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Used to debug and test multiple things'

    def handle(self, *args, **options):
        from Workout_Logbook.models import PrefilledExercise
        import json
        f = open('exercises.json')
        data = json.load(f)
        exercises = data.get('exercises')
        fields = [field.name for field in PrefilledExercise._meta.fields]
        fields.remove('id')
        objs = []
        muscle_choices = PrefilledExercise.MuscleGroupChoices.__members__.values()
        for exercise in exercises:
            ex = PrefilledExercise()
            for muscle in muscle_choices:
                print(muscle.label) # abdominals
                print(exercise.get('primary_muscles')) # ['abdominals']
            # exercise.get('primary_muscles') can have more than 1 muscle group. ex.primary_muscles is a multiple choice
            # field. gotta find a way to set the choices as being all the labels in the json
            ex.primary_muscles = next((muscle for muscle in muscle_choices if muscle.label == exercise.get('primary_muscles')), None)
            # for field in fields:
            #     if hasattr(exercise, field):
            #         setattr(obj, field, getattr(exercise, field))
            # objs.append(obj)
            print(ex.primary_muscles)
            break
