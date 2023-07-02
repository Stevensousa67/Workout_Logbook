import nested_admin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from Workout_Logbook.forms import CustomUserCreationForm, CustomUserChangeForm
from Workout_Logbook.models import CustomUserExercise, WorkoutUser, UserPhisyqueStatus, UserPhisyqueStatusPhoto, \
    WorkoutSession, WorkoutExercise, Set, WorkoutTemplate, WorkoutExerciseTemplate, SetTemplate, PrefilledExercise

admin.site.register(PrefilledExercise)


@admin.register(CustomUserExercise)
class CustomUserExerciseAdmin(admin.ModelAdmin):
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
class WorkoutUserAdmin(UserAdmin, nested_admin.NestedModelAdmin):
    inlines = [UserPhisyqueStatusInline]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_superuser']

    def get_fieldsets(self, request, obj=None):
        """Override do método para não permitir que usuários staff alterem configurações de permissões e de superusuário
            já que apenas superusuários podem fazer isto.
        """
        if request.user.is_superuser:
            perm_fields = ('is_staff', 'is_superuser', 'is_active', 'groups')
            perm_add_fields = (
                'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                'is_active')
        else:
            perm_fields = ('is_active',) if obj and not obj.is_superuser else ()
            perm_add_fields = (
                'email', 'password1', 'password2', 'first_name', 'last_name', 'is_active')

        fieldsets = (
            (_('Principal'), {'fields': ('email', 'password', 'first_name', 'last_name')}),
            (_('Permissões'), {'fields': perm_fields}),
            (_('Configurações'), {'fields': (
                'height', 'birthday', 'gender')})
        )
        add_fieldsets = (
            (_('Principal'), {
                'classes': ('wide',),
                'fields': perm_add_fields
            }),
            (
                _('Configurações'),
                {'fields': ('height', 'birthday', 'gender')})
        )
        if not obj:
            return add_fieldsets
        return fieldsets

    search_fields = ('email', 'first_name',)
    ordering = ('email',)


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
    readonly_fields = [
        'total_exercises',
        'total_reps',
        'total_weight',
        'total_load',
    ]
    fields = [
        'user',
        'date',
        'time',
        'total_exercises',
        'total_reps',
        'total_weight',
        'total_load',
        'template',
    ]


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
    readonly_fields = [
        'eta',
        'total_exercises',
        'history',
    ]
    fields =[
        'user',
        'name',
        'eta',
        'total_exercises',
        'history',
    ]
