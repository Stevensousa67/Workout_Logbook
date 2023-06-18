from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


def get_photo_path(instance, filename):
    import os
    filename = f"{instance.status.user.email}/{instance.status.date.strftime('%Y-%m-%d')}"
    return os.path.join('user-photos', filename)


class WorkoutUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.height = 180
        user.birthday = '1999-01-01'
        user.gender = 'M'
        user.save(using=self._db)
        return user


class WorkoutUser(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMA = 'F', 'Female'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField('Email address', unique=True)
    height = models.PositiveSmallIntegerField(verbose_name='Height (cm)')
    birthday = models.DateField(verbose_name='Birth Day')
    gender = models.CharField(verbose_name='Gender', max_length=2, choices=GenderChoices.choices, default=GenderChoices.MALE)

    objects = WorkoutUserManager()


class UserPhisyqueStatus(models.Model):
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date')
    weight = models.DecimalField('Current Weight', decimal_places=2, max_digits=5, null=True, blank=True)
    neck = models.PositiveSmallIntegerField('Neck Size (cm)', null=True, blank=True)
    chest = models.PositiveSmallIntegerField('Chest Size (cm)', null=True, blank=True)
    shoulder = models.PositiveSmallIntegerField('Shoulder Size (cm)', null=True, blank=True)
    back = models.PositiveSmallIntegerField('Back Size (cm)', null=True, blank=True)
    waist = models.PositiveSmallIntegerField('Waist Size (cm)', null=True, blank=True)
    abdomen = models.PositiveSmallIntegerField('Abdomen Size (cm)', null=True, blank=True)
    hips = models.PositiveSmallIntegerField('Hips Size (cm)', null=True, blank=True)
    thigh_r = models.PositiveSmallIntegerField('Right Thigh Size (cm)', null=True, blank=True)
    thigh_l = models.PositiveSmallIntegerField('Left Thigh Size (cm)', null=True, blank=True)
    calf_r = models.PositiveSmallIntegerField('Right Calf Size (cm)', null=True, blank=True)
    calf_l = models.PositiveSmallIntegerField('Calf Left Size (cm)', null=True, blank=True)
    biceps_r = models.PositiveSmallIntegerField('Right Biceps Size (cm)', null=True, blank=True)
    biceps_l = models.PositiveSmallIntegerField('Left Biceps Size (cm)', null=True, blank=True)
    forearm_r = models.PositiveSmallIntegerField('Right Forearm Size (cm)', null=True, blank=True)
    forearm_l = models.PositiveSmallIntegerField('Left Forearm Size (cm)', null=True, blank=True)
    wrist_r = models.PositiveSmallIntegerField('Right Wrist Size (cm)', null=True, blank=True)
    wrist_l = models.PositiveSmallIntegerField('Left Wrist Size (cm)', null=True, blank=True)


class UserPhisyqueStatusPhoto(models.Model):
    status = models.ForeignKey(to=UserPhisyqueStatus, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Photo', upload_to=get_photo_path)
    label = models.CharField(verbose_name='Label', max_length=50, null=True, blank=True)


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

    name = models.CharField(verbose_name="Exercise Name", max_length=100, null=True, blank=True)
    aliases = models.CharField(verbose_name="Aliases", max_length=100, null=True, blank=True, help_text="(optional)")
    primary_muscles = MultiSelectField(verbose_name="Primary Muscles", choices=MuscleGroupChoices.choices, max_length=100, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    secondary_muscles = MultiSelectField(verbose_name="Secondary Muscles", choices=MuscleGroupChoices.choices, max_length=100, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    force = models.CharField(verbose_name="Force", max_length=4, choices=ForceChoices.choices, default=ForceChoices.pull, null=True)
    level = models.CharField(verbose_name="Level", max_length=3, choices=LevelChoices.choices, default=LevelChoices.intermediate)
    mechanic = models.CharField(verbose_name="Mechanic", max_length=4, choices=MechanicChoices.choices, default=MechanicChoices.compound, null=True)
    equipment = models.CharField(verbose_name="Equipment", max_length=3, choices=EquipmentChoices.choices, default=EquipmentChoices.machine, null=True)
    category = models.CharField(verbose_name="Category", max_length=5, choices=CategoryChoices.choices, default=CategoryChoices.strength)
    instructions = models.TextField(verbose_name="Instructions", null=True, blank=True, help_text="(optional)")
    description = models.TextField(verbose_name="Description", null=True, blank=True, help_text="(optional)")
    tips = models.TextField(verbose_name="Tips", null=True, blank=True, help_text="(optional)")

    class Meta:
        abstract = True


class PrefilledExercise(BaseExercise):
    class Meta:
        verbose_name = "Pre-filled Exercise"
        verbose_name_plural = "Pre-filled Exercises"


class CustomUserExercise(BaseExercise):
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)
    reference = models.ForeignKey(to=PrefilledExercise, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Custom User Exercise"
        verbose_name_plural = "Custom User Exercises"

    def __str__(self):
        return self.name


@receiver(pre_save, sender=CustomUserExercise)
def prefill_user_exercise(sender, instance: CustomUserExercise, *args, **kwargs):
    """ Fills out a CustomUserExercise instance based on the PrefilledExercise selected
    """
    if not kwargs.get('created'):  # Only does this upon creation
        return
    if not instance.reference:  # If its a blank exercise, thus no reference, than theres nothing to be done
        return
    # Iterates through model fields. Because both CustomUserExercise and PrefilledExercise inherit from BaseExercise,
    # their fields are identical, except for the fields defined on CustomUserExercise
    for field in CustomUserExercise._meta.fields:
        fieldname = field.name
        if fieldname in ['id', 'reference', 'user']:  # These fields cannot be overwritten cuz theyre specific 4 CUsEx
            continue
        setattr(instance, fieldname, getattr(instance.reference, fieldname))


class WorkoutSession(models.Model):
    date = models.DateField(verbose_name='Date')
    time = models.TimeField(verbose_name='Time')
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)

    def total_exercises(self):
        pass

    def total_reps(self):
        pass

    def total_weight(self):
        pass


class WorkoutExercise(models.Model):
    workout_session = models.ForeignKey(verbose_name='Workout Session', to=WorkoutSession, on_delete=models.CASCADE)
    exercise = models.ForeignKey(verbose_name='Exercise', to=CustomUserExercise, on_delete=models.DO_NOTHING)


class Set(models.Model):
    exercise = models.ForeignKey(verbose_name='Exercise', to=WorkoutExercise, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name='Weight Used', decimal_places=2, max_digits=7, default=0.00)
    reps = models.PositiveSmallIntegerField(verbose_name='Reps Done', default=1)
    rest_time = models.PositiveSmallIntegerField(verbose_name='Rest Time (sec)', default=60)


class WorkoutTemplate(models.Model):
    name = models.CharField(verbose_name='Template Name', max_length=100)
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)


class WorkoutExerciseTemplate(models.Model):
    workout_template = models.ForeignKey(verbose_name='Workout Template', to=WorkoutTemplate, on_delete=models.CASCADE)
    exercise = models.ForeignKey(verbose_name='Exercise', to=CustomUserExercise, on_delete=models.DO_NOTHING)


class SetTemplate(models.Model):
    exercise = models.ForeignKey(verbose_name='Exercise Template', to=WorkoutExerciseTemplate, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name='Weight', decimal_places=2, max_digits=7, default=0.00)
    reps = models.PositiveSmallIntegerField(verbose_name='Reps', default=1)
