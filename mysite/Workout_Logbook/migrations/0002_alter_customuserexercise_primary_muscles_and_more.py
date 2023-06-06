# Generated by Django 4.2.2 on 2023-06-06 01:38

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Workout_Logbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserexercise',
            name='primary_muscles',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('abs', 'abdominals'), ('ham', 'hamstrings'), ('cal', 'calves'), ('sho', 'shoulders'), ('add', 'adductors'), ('glu', 'glutes'), ('qua', 'quadriceps'), ('bic', 'biceps'), ('for', 'forearms'), ('abd', 'abductors'), ('tri', 'triceps'), ('che', 'chest'), ('mbk', 'middle back'), ('lbk', 'lower back'), ('tra', 'traps'), ('lat', 'lats'), ('nec', 'neck')], default='sho', max_length=3, null=True, verbose_name='Primary Muscles'),
        ),
        migrations.AlterField(
            model_name='customuserexercise',
            name='secondary_muscles',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('abs', 'abdominals'), ('ham', 'hamstrings'), ('cal', 'calves'), ('sho', 'shoulders'), ('add', 'adductors'), ('glu', 'glutes'), ('qua', 'quadriceps'), ('bic', 'biceps'), ('for', 'forearms'), ('abd', 'abductors'), ('tri', 'triceps'), ('che', 'chest'), ('mbk', 'middle back'), ('lbk', 'lower back'), ('tra', 'traps'), ('lat', 'lats'), ('nec', 'neck')], default='sho', max_length=3, null=True, verbose_name='Secondary Muscles'),
        ),
    ]
