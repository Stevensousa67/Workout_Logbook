from .viewsets import WorkoutUserViewSet, UserPhisyqueStatusViewSet, UserPhisyqueStatusPhotoViewSet, \
    PrefilledExerciseViewSet, CustomUserExerciseViewSet, WorkoutTemplateViewSet, WorkoutExerciseTemplateViewSet, \
    SetTemplateViewSet, WorkoutSessionViewSet, WorkoutExerciseViewSet, SetViewSet

from rest_framework.routers import DefaultRouter

app_name = 'Workout_Logbook'

router = DefaultRouter()
router.register(r'workout-users', WorkoutUserViewSet, basename='workout_user')
router.register(r'user-phisyque-statuses', UserPhisyqueStatusViewSet, basename='user_phisyque_status')
router.register(r'user-phisyque-status-photos', UserPhisyqueStatusPhotoViewSet, basename='user_phisyque_status_photo')
router.register(r'prefilled-exercises', PrefilledExerciseViewSet, basename='prefilled_exercise')
router.register(r'custom-exercises', CustomUserExerciseViewSet, basename='custom_exercise')
router.register(r'workout-templates', WorkoutTemplateViewSet, basename='workout_template')
router.register(r'workout-exercise-templates', WorkoutExerciseTemplateViewSet, basename='workout_exercise_template')
router.register(r'set-templates', SetTemplateViewSet, basename='set_template')
router.register(r'workout-sessions', WorkoutSessionViewSet, basename='workout_session')
router.register(r'workout-exercises', WorkoutExerciseViewSet, basename='workout_exercise')
router.register(r'sets', SetViewSet, basename='set')
routes = router.urls
