

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.courses, name='courses'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Enrollment
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),

    # Course-related pages
    path('assignments/<int:course_id>/', views.assignments, name='assignments'),
    path('projects/<int:course_id>/', views.projects, name='projects'),
    path('quizzes/<int:course_id>/', views.quizzes, name='quizzes'),
    path('certificates/', views.certificates, name='certificates'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    path('assignment/<int:assignment_id>/dashboard/', views.assignment_dashboard, name='assignment_dashboard'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('my-assignments/', views.student_assignments, name='student_assignments'),

    #Submission
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('submit_project/<int:project_id>/', views.submit_project, name='submit_project'),

    #Quize
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),

    #Admin
    path('nested_admin/', include('nested_admin.urls')),  # add this
    path('admin/', admin.site.urls),

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)