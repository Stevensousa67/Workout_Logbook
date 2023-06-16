# Generated by Django 4.2.2 on 2023-06-16 01:16

from django.db import migrations


def populate_table(apps, schema_editor):
    from Workout_Logbook.models import PrefilledExercise
    import json
    f = open('exercises.json')
    data = json.load(f)
    exercises = data.get('exercises')
    fields = [field.name for field in PrefilledExercise._meta.fields]
    fields.remove('id')
    objs = []
    for exercise in exercises:
        obj = PrefilledExercise()
        for field in fields:
            if hasattr(exercise, field):
                setattr(obj, field, getattr(exercise, field))
        objs.append(obj)
    print(objs)


class Migration(migrations.Migration):

    dependencies = [
        ('Workout_Logbook', '0002_prefilledexercise_customuserexercise_reference'),
    ]

    operations = [
        migrations.RunPython(populate_table)
    ]
