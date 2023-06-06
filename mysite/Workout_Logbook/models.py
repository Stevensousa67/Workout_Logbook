from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField


class BaseExercise(models.Model):
    """
    Abstract class to register an exercise
    """

    class MuscleGroupChoices(models.TextChoices):
        abdominals = "abs", "abdominals",
        hamstrings = "ham", "hamstrings",
        calves = "cal", "calves",
        shoulders = "sho", "shoulders",
        adductors = "add", "adductors",
        glutes = "glu", "glutes",
        quadriceps = "qua", "quadriceps",
        biceps = "bic", "biceps",
        forearms = "for", "forearms",
        abductors = "abd", "abductors",
        triceps = "tri", "triceps",
        chest = "che", "chest",
        middle_back = "mbk", "middle back",
        lower_back = "lbk", "lower back",
        traps = "tra", "traps",
        lats = "lat", "lats",
        neck = "nec", "neck",

    class ForceChoices(models.TextChoices):
        pull = "pull", "Pull",
        push = "push", "Push",
        static = "stat", "Static",

    class LevelChoices(models.TextChoices):
        beginner = "beg", "beginner",
        intermediate = "int", "intermediate",
        expert = "exp", "expert",

    class MechanicChoices(models.TextChoices):
        compound = "comp", "compound",
        isolation = "isol", "isolation",

    class EquipmentChoices(models.TextChoices):
        body = "bod", "body only",
        machine = "mac", "machine",
        kettlebells = "ket", "kettlebells",
        dumbbell = "dum", "dumbbell",
        cable = "cab", "cable",
        barbell = "bar", "barbell",
        bands = "ban", "bands",
        medicine_ball = "med", "medicine ball",
        exercise_ball = "exe", "exercise ball",
        e_z_curl_bar = "cba", "e-z curl bar",
        foam_roll = "fro", "foam roll",

    class CategoryChoices(models.TextChoices):
        strength = "stren", "strength",
        stretching = "stret", "stretching",
        plyometrics = "plyom", "plyometrics",
        strongman = "stron", "strongman",
        powerlifting = "power", "powerlifting",
        cardio = "cardi", "cardio",
        olympic_weightlifting = "olwei", "olympic weightlifting",
        crossfit = "cross", "crossfit",
        weighted_bodyweight = "weibw", "weighted bodyweight",
        assisted_bodyweight = "assbw", "assisted bodyweight",

    name = models.CharField(verbose_name="Exercise Name", max_length=100)
    aliases = models.CharField(verbose_name="Aliases", max_length=100, null=True, blank=True, help_text="(optional)")
    primary_muscles = MultiSelectField(verbose_name="Primary Muscles", choices=MuscleGroupChoices.choices, max_length=3, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    secondary_muscles = MultiSelectField(verbose_name="Secondary Muscles", choices=MuscleGroupChoices.choices, max_length=3, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    force = models.CharField(verbose_name="Force", max_length=4, choices=ForceChoices.choices, default=ForceChoices.pull)
    level = models.CharField(verbose_name="Level", max_length=3, choices=LevelChoices.choices, default=LevelChoices.intermediate)
    mechanic = models.CharField(verbose_name="Mechanic", max_length=4, choices=MechanicChoices.choices, default=MechanicChoices.compound)
    equipment = models.CharField(verbose_name="Equipment", max_length=3, choices=EquipmentChoices.choices, default=EquipmentChoices.machine)
    category = models.CharField(verbose_name="Category", max_length=5, choices=CategoryChoices.choices, default=CategoryChoices.strength)
    instructions = models.TextField(verbose_name="Instructions", null=True, blank=True, help_text="(optional)")
    description = models.TextField(verbose_name="Description", null=True, blank=True, help_text="(optional)")
    tips = models.TextField(verbose_name="Tips", null=True, blank=True, help_text="(optional)")

    class Meta:
        abstract = True


class CustomUserExercise(BaseExercise):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Custom User Exercise"
        verbose_name_plural = "Custom User Exercises"

    def __str__(self):
        return self.name
