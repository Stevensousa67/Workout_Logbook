# Generated by Django 4.2.2 on 2023-06-16 01:16

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Workout_Logbook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrefilledExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Exercise Name')),
                ('aliases', models.CharField(blank=True, help_text='(optional)', max_length=100, null=True, verbose_name='Aliases')),
                ('primary_muscles', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('abs', 'abdominals'), ('ham', 'hamstrings'), ('cal', 'calves'), ('sho', 'shoulders'), ('add', 'adductors'), ('glu', 'glutes'), ('qua', 'quadriceps'), ('bic', 'biceps'), ('for', 'forearms'), ('abd', 'abductors'), ('tri', 'triceps'), ('che', 'chest'), ('mbk', 'middle back'), ('lbk', 'lower back'), ('tra', 'traps'), ('lat', 'lats'), ('nec', 'neck')], default='sho', max_length=3, null=True, verbose_name='Primary Muscles')),
                ('secondary_muscles', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('abs', 'abdominals'), ('ham', 'hamstrings'), ('cal', 'calves'), ('sho', 'shoulders'), ('add', 'adductors'), ('glu', 'glutes'), ('qua', 'quadriceps'), ('bic', 'biceps'), ('for', 'forearms'), ('abd', 'abductors'), ('tri', 'triceps'), ('che', 'chest'), ('mbk', 'middle back'), ('lbk', 'lower back'), ('tra', 'traps'), ('lat', 'lats'), ('nec', 'neck')], default='sho', max_length=3, null=True, verbose_name='Secondary Muscles')),
                ('force', models.CharField(choices=[('pull', 'Pull'), ('push', 'Push'), ('stat', 'Static')], default='pull', max_length=4, verbose_name='Force')),
                ('level', models.CharField(choices=[('beg', 'beginner'), ('int', 'intermediate'), ('exp', 'expert')], default='int', max_length=3, verbose_name='Level')),
                ('mechanic', models.CharField(choices=[('comp', 'compound'), ('isol', 'isolation')], default='comp', max_length=4, verbose_name='Mechanic')),
                ('equipment', models.CharField(choices=[('bod', 'body only'), ('mac', 'machine'), ('ket', 'kettlebells'), ('dum', 'dumbbell'), ('cab', 'cable'), ('bar', 'barbell'), ('ban', 'bands'), ('med', 'medicine ball'), ('exe', 'exercise ball'), ('cba', 'e-z curl bar'), ('fro', 'foam roll')], default='mac', max_length=3, verbose_name='Equipment')),
                ('category', models.CharField(choices=[('stren', 'strength'), ('stret', 'stretching'), ('plyom', 'plyometrics'), ('stron', 'strongman'), ('power', 'powerlifting'), ('cardi', 'cardio'), ('olwei', 'olympic weightlifting'), ('cross', 'crossfit'), ('weibw', 'weighted bodyweight'), ('assbw', 'assisted bodyweight')], default='stren', max_length=5, verbose_name='Category')),
                ('instructions', models.TextField(blank=True, help_text='(optional)', null=True, verbose_name='Instructions')),
                ('description', models.TextField(blank=True, help_text='(optional)', null=True, verbose_name='Description')),
                ('tips', models.TextField(blank=True, help_text='(optional)', null=True, verbose_name='Tips')),
            ],
            options={
                'verbose_name': 'Pre-filled Exercise',
                'verbose_name_plural': 'Pre-filled Exercises',
            },
        ),
        migrations.AddField(
            model_name='customuserexercise',
            name='reference',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Workout_Logbook.prefilledexercise'),
        ),
    ]
