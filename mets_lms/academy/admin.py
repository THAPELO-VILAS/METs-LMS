# from django.contrib import admin

# # Register your models here.

from django.contrib import admin
from .models import Course, Enrollment, Quiz, Assignment, Project, Certificate, Question, Choice
from .models import Assignment, AssignmentSubmission,ProjectSubmission



admin.site.register(Course)
admin.site.register(Enrollment)
import nested_admin




class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 4
    min_num = 2
    max_num = 10

class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]
    fields = ['text', 'question_type']  # ✅ make admin show the type

class QuizAdmin(nested_admin.NestedModelAdmin):
    model = Quiz
    inlines = [QuestionInline]
    list_display = ('title', 'course', 'time_limit', 'max_attempts')

class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission
    extra = 0
    readonly_fields = ['student', 'file', 'submitted_at']

class ProjectSubmissionInline(admin.TabularInline):
    model = ProjectSubmission
    extra = 0
    readonly_fields = ['student', 'file', 'submitted_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date']
    inlines = [ProjectSubmissionInline]

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ['project', 'student', 'file', 'submitted_at']

# @admin.register(Assignment)
# class AssignmentAdmin(admin.ModelAdmin):
#     list_display = ['title', 'course', 'due_date']
#     inlines = [AssignmentSubmissionInline]

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at']
    list_filter = ['assignment']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)#, QuestionAdmin)
# admin.site.register(Quiz)
from .models import QuizAttempt

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'student', 'score', 'completed_at']
    list_filter = ['quiz', 'completed_at']
    search_fields = ['student__username', 'quiz__title']
admin.site.register(Assignment)
# admin.site.register(Project)
admin.site.register(Certificate)
# admin.site.register(Question)
admin.site.register(Choice)







