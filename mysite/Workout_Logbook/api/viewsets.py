from django_filters.rest_framework import DjangoFilterBackend

from .helpers import CustomModelViewSet
from .serializers import WorkoutUserSerializer, UserPhisyqueStatusSerializer, UserPhisyqueStatusPhotoSerializer, \
    PrefilledExerciseSerializer, CustomUserExerciseSerializer, WorkoutTemplateSerializer, \
    WorkoutExerciseTemplateSerializer, SetTemplateSerializer, WorkoutSessionSerializer, WorkoutExerciseSerializer, \
    SetSerializer
from Workout_Logbook.models import WorkoutUser, UserPhisyqueStatus, UserPhisyqueStatusPhoto, PrefilledExercise, \
    CustomUserExercise, WorkoutTemplate, WorkoutExerciseTemplate, SetTemplate, WorkoutSession, WorkoutExercise, Set


class WorkoutUserViewSet(CustomModelViewSet):
    queryset = WorkoutUser.objects.all()
    serializer_class = WorkoutUserSerializer


class UserPhisyqueStatusViewSet(CustomModelViewSet):
    queryset = UserPhisyqueStatus.objects.all()
    serializer_class = UserPhisyqueStatusSerializer


class UserPhisyqueStatusPhotoViewSet(CustomModelViewSet):
    queryset = UserPhisyqueStatusPhoto.objects.all()
    serializer_class = UserPhisyqueStatusPhotoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']


class PrefilledExerciseViewSet(CustomModelViewSet):
    queryset = PrefilledExercise.objects.all()
    serializer_class = PrefilledExerciseSerializer


class CustomUserExerciseViewSet(CustomModelViewSet):
    queryset = CustomUserExercise.objects.all()
    serializer_class = CustomUserExerciseSerializer


class WorkoutTemplateViewSet(CustomModelViewSet):
    queryset = WorkoutTemplate.objects.all()
    serializer_class = WorkoutTemplateSerializer


class WorkoutExerciseTemplateViewSet(CustomModelViewSet):
    queryset = WorkoutExerciseTemplate.objects.all()
    serializer_class = WorkoutExerciseTemplateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workout_template']


class SetTemplateViewSet(CustomModelViewSet):
    queryset = SetTemplate.objects.all()
    serializer_class = SetTemplateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exercise', 'exercise__workout_template']


class WorkoutSessionViewSet(CustomModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['template']


class WorkoutExerciseViewSet(CustomModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workout_session']


class SetViewSet(CustomModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exercise', 'exercise__workout_session']
