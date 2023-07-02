import decimal
import math
from _decimal import Decimal
from typing import List
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField

from Workout_Logbook.base_model import BaseModel

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


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


class WorkoutUser(AbstractUser, BaseModel):
    class GenderChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMA = 'F', 'Female'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField('Email address', unique=True)
    height = models.PositiveSmallIntegerField(verbose_name='Height (cm)')
    birthday = models.DateField(verbose_name='Birth Day')
    gender = models.CharField(verbose_name='Gender', max_length=2, choices=GenderChoices.choices,
                              default=GenderChoices.MALE)

    objects = WorkoutUserManager()

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.all()

    def owner_id(self):
        return self.id


class UserPhisyqueStatus(BaseModel):
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date')
    weight = models.DecimalField('Current Weight', decimal_places=2, max_digits=5, null=True, blank=True)
    body_fat = models.DecimalField('Body Fat (%)', decimal_places=2, max_digits=5, null=True, blank=True,
                                   default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
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

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(user_id__exact=user_id)

    def owner_id(self):
        return self.user.owner_id()


class UserPhisyqueStatusPhoto(BaseModel):
    status = models.ForeignKey(to=UserPhisyqueStatus, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Photo', upload_to=get_photo_path)
    label = models.CharField(verbose_name='Label', max_length=50, null=True, blank=True)

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(status__user_id__exact=user_id)

    def owner_id(self):
        return self.status.owner_id()


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
    primary_muscles = MultiSelectField(verbose_name="Primary Muscles", choices=MuscleGroupChoices.choices,
                                       max_length=100, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    secondary_muscles = MultiSelectField(verbose_name="Secondary Muscles", choices=MuscleGroupChoices.choices,
                                         max_length=100, default=MuscleGroupChoices.shoulders, null=True, blank=True)
    force = models.CharField(verbose_name="Force", max_length=4, choices=ForceChoices.choices,
                             default=ForceChoices.pull, null=True)
    level = models.CharField(verbose_name="Level", max_length=3, choices=LevelChoices.choices,
                             default=LevelChoices.intermediate)
    mechanic = models.CharField(verbose_name="Mechanic", max_length=4, choices=MechanicChoices.choices,
                                default=MechanicChoices.compound, null=True)
    equipment = models.CharField(verbose_name="Equipment", max_length=3, choices=EquipmentChoices.choices,
                                 default=EquipmentChoices.machine, null=True)
    category = models.CharField(verbose_name="Category", max_length=5, choices=CategoryChoices.choices,
                                default=CategoryChoices.strength)
    instructions = models.TextField(verbose_name="Instructions", null=True, blank=True, help_text="(optional)")
    description = models.TextField(verbose_name="Description", null=True, blank=True, help_text="(optional)")
    tips = models.TextField(verbose_name="Tips", null=True, blank=True, help_text="(optional)")

    class Meta:
        abstract = True


class PrefilledExercise(BaseExercise, BaseModel):
    class Meta:
        verbose_name = "Pre-filled Exercise"
        verbose_name_plural = "Pre-filled Exercises"

    def __str__(self):
        return self.name

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.all()

    def owner_id(self):
        return None


class CustomUserExercise(BaseExercise):
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)
    reference = models.ForeignKey(to=PrefilledExercise, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Custom User Exercise"
        verbose_name_plural = "Custom User Exercises"

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Preenche os campos do exercicio com base na referencia. Ao final, define a referencia como nula pra permitir
        futuras edicoes no exercicio customizado
        """
        reference = self.reference
        name = self.name
        if not reference:
            if not name:
                raise ValidationError(_('Name field is mandatory'))
            return
        for field in self._meta.get_fields():
            field_name = field.name
            if field_name in ['id', 'user', 'reference', 'tips', 'description', 'aliases']:
                continue
            if field_name == 'name':
                self.name = name or reference.name
                continue
            setattr(self, field_name, getattr(reference, field_name) or getattr(self, field_name))
        self.reference = None
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(user_id__exact=user_id)

    def owner_id(self):
        return self.user.owner_id()

    def history(self) -> List:
        """
        Retorna uma lista contendo o histórico desse exercicio para o usuário dele
        Returns:
            Lista contendo os dados de peso, reps e carga para determinados dias
        """
        return [{'date': w_ex.workout_session.date, 'reps': w_ex.total_reps(), 'weight': w_ex.total_weight(),
                 'load': w_ex.total_load()} for w_ex in self.workoutexercise_set.all()]


class WorkoutTemplate(models.Model):
    name = models.CharField(verbose_name='Template Name', max_length=100)
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(user_id__exact=user_id)

    def owner_id(self):
        return self.user.owner_id()

    # todo: colocar quantidade de exercicios separada por grupo muscular

    def eta(self) -> int:
        """
        Retorna um tempo estimado necessário para a execução dessa ficha
        Returns:
            Tempo, em minutos
        """
        return math.ceil(sum([
            w_ex.eta() + (5 * 60)  # Tempo estimado pra cada exercicio + 5min de descanso entre os exercicios
            for w_ex in self.workoutexercisetemplate_set.all()
        ]) / 60)

    def total_exercises(self) -> int:
        """
        Retorna a quantidade de exercicios planejados para essa ficha
        """
        return self.workoutexercisetemplate_set.count()

    def history(self) -> List:
        """
        Retorna uma lista contendo o histórico dessa ficha para o usuário dela
        Returns:
            Lista contendo os dados de peso, reps e carga para determinados dias
        """
        return [{'date': w_session.date, 'reps': w_session.total_reps(), 'weight': w_session.total_weight(),
                 'load': w_session.total_load()} for w_session in self.workoutsession_set.all()]


class WorkoutExerciseTemplate(models.Model):
    workout_template = models.ForeignKey(verbose_name='Workout', to=WorkoutTemplate, on_delete=models.CASCADE)
    exercise = models.ForeignKey(verbose_name='Exercise', to=CustomUserExercise, on_delete=models.PROTECT)

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(workout_template__user_id__exact=user_id)

    def owner_id(self):
        return self.workout_template.owner_id()

    def eta(self) -> int:
        """
        Retorna um tempo estimado necessário para a execução desse exercicio
        Returns:
            Tempo, em segundos
        """
        return sum([
            7 * set.reps +  # Estima-se que uma repetição bem feita dure 7 segundos
            set.rest_time  # Soma-se o tempo de descanso entre as séries
            for set in self.settemplate_set.all()
        ])


class SetTemplate(models.Model):
    exercise = models.ForeignKey(verbose_name='Exercise', to=WorkoutExerciseTemplate, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name='Weight', decimal_places=2, max_digits=7, default=0.00)
    reps = models.PositiveSmallIntegerField(verbose_name='Reps', default=1)
    rest_time = models.PositiveSmallIntegerField(verbose_name='Rest Time (sec)', default=60)

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(exercise__workout_template__user_id__exact=user_id)

    def owner_id(self):
        return self.exercise.owner_id()


class WorkoutSession(models.Model):
    date = models.DateField(verbose_name='Date')
    time = models.TimeField(verbose_name='Time')
    user = models.ForeignKey(to=WorkoutUser, on_delete=models.CASCADE)
    template = models.ForeignKey(verbose_name='Template', to=WorkoutTemplate, on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return f'{self.user} @ {self.date.strftime("%d/%m/%Y")} ({self.template.name if self.template else "-"})'

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(user_id__exact=user_id)

    def owner_id(self):
        return self.user.owner_id()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Cria os exercicios e sets com base no template, se houver algum
        """
        super().save(force_insert, force_update, using, update_fields)
        if not self.template:
            return
        for exercise_template in self.template.workoutexercisetemplate_set.all():
            exercise = WorkoutExercise.objects.create(workout_session=self, exercise=exercise_template.exercise)
            for set_template in exercise_template.settemplate_set.all():
                Set.objects.create(exercise=exercise, weight=set_template.weight, reps=set_template.reps,
                                   rest_time=set_template.rest_time)

    def total_exercises(self) -> int:
        """
        Retorna a quantidade de exercicios realizados nessa sessao
        """
        return self.workoutexercise_set.count()

    def all_sets(self) -> List['Set']:
        """
        Retorna uma lista com todos os sets realizados nessa sessao
        """
        sets = []
        for exercise in self.workoutexercise_set.all():
            sets.append(exercise.set_set.all())
        from itertools import chain
        return list(chain(*sets))

    def total_reps(self) -> int:
        """
        Retorna o total de repeticoes feita nessa sessao
        """
        return sum([set.reps for set in self.all_sets()])

    def total_weight(self) -> decimal.Decimal:
        """
        Retorna o peso total levantado nessa sessao
        """
        return sum([set.weight for set in self.all_sets()])

    def total_load(self) -> decimal.Decimal:
        """
        Retorna a carga total dessa sessao
        """
        return self.total_reps() * self.total_weight()


class WorkoutExercise(models.Model):
    workout_session = models.ForeignKey(verbose_name='Workout Session', to=WorkoutSession, on_delete=models.CASCADE)
    exercise = models.ForeignKey(verbose_name='Exercise', to=CustomUserExercise, on_delete=models.PROTECT)

    def __str__(self):
        return self.exercise.name

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(workout_session__user_id__exact=user_id)

    def owner_id(self):
        return self.workout_session.owner_id()

    def total_reps(self) -> int:
        """
        Retorna o total de repeticoes feitas nesse exercicio feito
        """
        return sum(self.set_set.all().values_list('reps', flat=True))

    def total_weight(self) -> decimal.Decimal:
        """
        Retorna o peso total levantado nesse exercicio feito
        """
        return sum(self.set_set.all().values_list('weight', flat=True))

    def total_load(self) -> decimal.Decimal:
        """
        Retorna a carga total desse exercicio feito
        """
        return self.total_reps() * self.total_weight()


class Set(models.Model):
    exercise = models.ForeignKey(verbose_name='Exercise', to=WorkoutExercise, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name='Weight Used', decimal_places=2, max_digits=7, default=0.00)
    reps = models.PositiveSmallIntegerField(verbose_name='Reps Done', default=1)
    rest_time = models.PositiveSmallIntegerField(verbose_name='Rest Time (sec)', default=60)

    def __str__(self):
        return f'{self.exercise.exercise.name} - {self.weight}:{self.reps}:{self.rest_time}'

    @classmethod
    def get_queryset(cls, user_id):
        return cls.objects.filter(exercise__workout_session__user_id__exact=user_id)

    def owner_id(self):
        return self.exercise.owner_id()
