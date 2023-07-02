from rest_framework import serializers
from Workout_Logbook.models import WorkoutUser, UserPhisyqueStatus, UserPhisyqueStatusPhoto, PrefilledExercise, \
    CustomUserExercise, WorkoutTemplate, WorkoutExerciseTemplate, SetTemplate, WorkoutSession, WorkoutExercise, Set


class WorkoutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutUser
        fields = [
            'id',
            'first_name',
            'email',
            'height',
            'birthday',
            'gender',
            'get_gender_display',
        ]


class UserPhisyqueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhisyqueStatus
        fields = [
            'id',
            'user',
            'date',
            'weight',
            'body_fat',
            'neck',
            'chest',
            'shoulder',
            'back',
            'waist',
            'abdomen',
            'hips',
            'thigh_r',
            'thigh_l',
            'calf_r',
            'calf_l',
            'biceps_r',
            'biceps_l',
            'forearm_r',
            'forearm_l',
            'wrist_r',
            'wrist_l',
        ]


class UserPhisyqueStatusPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhisyqueStatusPhoto
        fields = [
            'id',
            'status',
            'photo',
            'label',
        ]


class PrefilledExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefilledExercise
        fields = [
            'id',
            'name',
            'aliases',
            'primary_muscles',
            'secondary_muscles',
            'force',
            'level',
            'mechanic',
            'equipment',
            'category',
            'instructions',
            'description',
            'tips',
            'get_primary_muscles_display',
            'get_secondary_muscles_display',
            'get_force_display',
            'get_level_display',
            'get_mechanic_display',
            'get_equipment_display',
            'get_category_display',
        ]


class CustomUserExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserExercise
        fields = [
            'id',
            'name',
            'aliases',
            'primary_muscles',
            'secondary_muscles',
            'force',
            'level',
            'mechanic',
            'equipment',
            'category',
            'instructions',
            'description',
            'tips',
            'get_primary_muscles_display',
            'get_secondary_muscles_display',
            'get_force_display',
            'get_level_display',
            'get_mechanic_display',
            'get_equipment_display',
            'get_category_display',
            'user',
            'reference',
            'history',
        ]


class WorkoutTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTemplate
        fields = [
            'id',
            'name',
            'user',
            'eta',
            'total_exercises',
            'history',
        ]


class WorkoutExerciseTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExerciseTemplate
        fields = [
            'id',
            'workout_template',
            'exercise',
            'eta',
        ]


class SetTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetTemplate
        fields = [
            'id',
            'exercise',
            'weight',
            'reps',
            'rest_time',
        ]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = [
            'id',
            'date',
            'time',
            'user',
            'template',
            'total_exercises',
            'total_reps',
            'total_weight',
            'total_load',
        ]


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'workout_session',
            'exercise',
            'total_reps',
            'total_weight',
            'total_load',
        ]


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = [
            'id',
            'exercise',
            'weight',
            'reps',
            'rest_time',
        ]
