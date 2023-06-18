import nested_admin
from django.contrib import admin

from Workout_Logbook.forms import CustomUserExerciseForm
from Workout_Logbook.models import CustomUserExercise, WorkoutUser, UserPhisyqueStatus, UserPhisyqueStatusPhoto, \
    WorkoutSession, WorkoutExercise, Set, WorkoutTemplate, WorkoutExerciseTemplate, SetTemplate, PrefilledExercise

admin.site.register(PrefilledExercise)


@admin.register(CustomUserExercise)
class CustomUserExerciseAdmin(admin.ModelAdmin):
    form = CustomUserExerciseForm
    search_fields = [
        'name',
        'aliases',
    ]
    list_filter = [
        'user',
        # 'primary_muscles',
        # 'secondary_muscles',
        'force',
        'level',
        'mechanic',
        'equipment',
        'category',
    ]
    fields = [
        'user',
        'reference',
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
    ]


class UserPhisyqueStatusPhotoInline(nested_admin.NestedStackedInline):
    extra = 0
    model = UserPhisyqueStatusPhoto


class UserPhisyqueStatusInline(nested_admin.NestedStackedInline):
    extra = 0
    model = UserPhisyqueStatus
    inlines = [UserPhisyqueStatusPhotoInline]


@admin.register(WorkoutUser)
class WorkoutUserAdmin(nested_admin.NestedModelAdmin):
    inlines = [UserPhisyqueStatusInline]


class SetInline(nested_admin.NestedStackedInline):
    extra = 0
    model = Set


class WorkoutExerciseInline(nested_admin.NestedStackedInline):
    extra = 0
    model = WorkoutExercise
    inlines = [SetInline]


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(nested_admin.NestedModelAdmin):
    inlines = [WorkoutExerciseInline]


class SetTemplateInline(nested_admin.NestedStackedInline):
    extra = 0
    model = SetTemplate


class WorkoutExerciseTemplateInline(nested_admin.NestedStackedInline):
    extra = 0
    model = WorkoutExerciseTemplate
    inlines = [SetTemplateInline]


@admin.register(WorkoutTemplate)
class WorkoutTemplateAdmin(nested_admin.NestedModelAdmin):
    inlines = [WorkoutExerciseTemplateInline]
