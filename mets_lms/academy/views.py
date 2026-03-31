from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Certificate, Assignment, Project
from django.utils import timezone
from django.db import models

from .forms import AssignmentUploadForm, ProjectUploadForm
from .models import Quiz, Question, Choice, StudentAnswer, QuizAttempt
from .models import Assignment, AssignmentSubmission

from .models import Course, Assignment, Project, AssignmentSubmission, ProjectSubmission

User = get_user_model()

# ------------------------------
# INDEX (Public)
# ------------------------------
def index(request):
    return render(request, 'academy/index.html')


# ------------------------------
# HOME (Dashboard - Protected)
# ------------------------------
@login_required



def home(request):
    all_courses = Course.objects.all()  # Show all courses on home
    user_courses = request.user.enrolled_courses.all() if request.user.is_authenticated else []
    return render(request, 'academy/home.html', {
        'all_courses': all_courses,
        'user_courses': user_courses
    })


@login_required
def dashboard(request):
    enrolled_courses = request.user.enrolled_courses.all()

    for course in enrolled_courses:
        course.progress = 30

    return render(request, 'academy/dashboard.html', {
        'enrolled_courses': enrolled_courses
    })



# ------------------------------
# COURSES (Public)
# ------------------------------
def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'academy/courses.html', {'all_courses': all_courses})


# ------------------------------
# REGISTER (AUTO LOGIN)
# ------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        id_number = request.POST.get('id_number')
        country = request.POST.get('country')
        city = request.POST.get('city')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user = User.objects.create_user(
                username=email,  # ✅ use email as username
                email=email,
                id_number=id_number,
                country=country,
                city=city,
                password=password1
            )

            # ✅ AUTO LOGIN AFTER REGISTER
            login(request, user)

            messages.success(request, "Account created successfully!")
            return redirect('home')

    return render(request, 'academy/register.html')


# ------------------------------
# LOGIN (EMAIL BASED)
# ------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email).first()

        if user:
            user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'academy/login.html')


# ------------------------------
# LOGOUT
# ------------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')




from .models import Enrollment


#     return redirect('home')


from django.shortcuts import get_object_or_404



@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user in course.students.all():
        messages.info(request, f"You are already enrolled in {course.name}.")
    else:
        course.students.add(request.user)
        messages.success(request, f"You have enrolled in {course.name}.")

    return redirect('dashboard')



@login_required

def unenroll_course(request, course_id):
    try:
        course = Course.objects.get(request,id=course_id)
        if request.user in course.students.all():
            course.students.remove(request.user)
            messages.success(request, f"You have unenrolled from {course.name}.")
        else:
            messages.error(request, "You are not enrolled in this course.")
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
    return redirect('dashboard')

@login_required
def unenroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.students.remove(request.user)
    return redirect('dashboard')



    

# ------------------------------
# ASSIGNMENTS
# ------------------------------


@login_required
def assignments(request, course_id):
    course = Course.objects.get(id=course_id)

    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('courses')

    return render(request, 'academy/assignments.html', {'course': course})


# ------------------------------
# PROJECTS
# ------------------------------
@login_required
def projects(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.user not in course.students.all():
        return redirect('courses')

    return render(request, 'academy/projects.html', {'course': course})


@login_required
def quizzes(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('dashboard')

    if request.user not in course.students.all():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')

    return render(request, 'academy/quizzes.html', {'course': course})

# ------------------------------
# CERTIFICATES
# ------------------------------

@login_required
def certificates(request):
    user_certificates = Certificate.objects.filter(student=request.user)

    return render(request, 'academy/certificates.html', {
        'certificates': user_certificates
    })

from django.db.models import Count

@login_required
def course_detail(request, course_id):
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages

    course = get_object_or_404(Course, id=course_id)

    # Ensure student is enrolled
    if request.user not in course.students.all():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')

    # Course-level assignments and projects
    assignments = Assignment.objects.filter(course=course)
    projects = Project.objects.filter(course=course)

    # Student submissions
    student_assignment_submissions = AssignmentSubmission.objects.filter(
        student=request.user,
        assignment__course=course
    ).values_list('assignment_id', flat=True)

    student_project_submissions = ProjectSubmission.objects.filter(
        student=request.user,
        project__course=course
    ).values_list('project_id', flat=True)

    # Handle upload
    if request.method == 'POST':
        # Assignment upload
        if 'assignment_file' in request.FILES:
            assignment_id = request.POST.get('assignment_id')
            assignment = Assignment.objects.get(id=assignment_id)

            if assignment.id in student_assignment_submissions:
                messages.warning(request, "You have already submitted this assignment.")
            else:
                AssignmentSubmission.objects.create(
                    assignment=assignment,
                    student=request.user,
                    file=request.FILES['assignment_file']
                )
                messages.success(request, "Assignment submitted successfully.")
            return redirect('course_detail', course_id=course.id)

        # Project upload
        elif 'project_file' in request.FILES:
            project_id = request.POST.get('project_id')
            project = Project.objects.get(id=project_id)

            if project.id in student_project_submissions:
                messages.warning(request, "You have already submitted this project.")
            else:
                ProjectSubmission.objects.create(
                    project=project,
                    student=request.user,
                    file=request.FILES['project_file']
                )
                messages.success(request, "Project submitted successfully.")
            return redirect('course_detail', course_id=course.id)
    # Track attempts for each quiz
    quiz_attempts = {}
    for quiz in course.quiz_set.all():
        attempts = quiz.quizattempt_set.filter(student=request.user).count()
        quiz_attempts[quiz.id] = attempts

    

    return render(request, 'academy/course_detail.html', {
        'course': course,
        'assignments': assignments,
        'projects': projects,
        'student_assignment_submissions': student_assignment_submissions,
        'student_project_submissions': student_project_submissions,
        'quiz_attempts': quiz_attempts,  # pass attempts to template
    })
    
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check enrollment
    if request.user not in assignment.course.students.all():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')

    if not assignment.is_open:
        messages.error(request, "This assignment is closed.")
        return redirect('course_detail', course_id=assignment.course.id)

    if request.method == "POST":
        form = AssignmentUploadForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('course_detail', course_id=assignment.course.id)
    else:
        form = AssignmentUploadForm()

    return render(request, 'academy/submit_assignment.html', {'assignment': assignment, 'form': form})


# -------------------
# Project Upload
# -------------------
@login_required
def submit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check enrollment
    if request.user not in project.course.students.all():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')

    if not project.is_open:
        messages.error(request, "This project is closed.")
        return redirect('course_detail', course_id=project.course.id)

    if request.method == "POST":
        form = ProjectUploadForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user
            project.save()
            messages.success(request, "Project submitted successfully!")
            return redirect('course_detail', course_id=project.course.id)
    else:
        form = ProjectUploadForm()

    return render(request, 'academy/submit_project.html', {'project': project, 'form': form})

from .models import Quiz, Question, Choice, StudentAnswer

@login_required

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()

    if request.method == "POST":
        attempt = QuizAttempt.objects.create(student=request.user, quiz=quiz)
        score = 0

        for question in questions:
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected_choice
                )
                if selected_choice.is_correct:
                    score += 1

        attempt.score = (score / questions.count()) * 100
        attempt.save()

        # Prepare student answers dictionary for template
        student_answers = {}
        for sa in StudentAnswer.objects.filter(attempt=attempt):
            student_answers[sa.question.id] = sa.selected_choice.id

        return render(request, 'academy/quiz_result.html', {
            'quiz': quiz,
            'questions': questions,
            'attempt': attempt,
            'student_answers': student_answers,
        })

    return render(request, 'academy/quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })






# def take_quiz(request, quiz_id):
#     from django.shortcuts import get_object_or_404, redirect
#     from django.contrib import messages

#     quiz = get_object_or_404(Quiz, id=quiz_id)

#     # Count previous attempts
#     user_attempts = QuizAttempt.objects.filter(
#         quiz=quiz,
#         student=request.user
#     ).count()

#     # Check maximum attempts
#     if user_attempts >= quiz.max_attempts:
#         messages.warning(request, "You have reached the maximum number of attempts for this quiz.")
#         return redirect('course_detail', course_id=quiz.course.id)

#     # Handle quiz submission normally...
#     if request.method == 'POST':
#         # your existing submission logic here
#         pass

#     # Render quiz page
#     return render(request, 'academy/take_quiz.html', {'quiz': quiz})

def quiz_result(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    attempt = QuizAttempt.objects.get(user=request.user, quiz=quiz)
    
    # Prepare dictionary of question_id -> selected_choice.id
    student_answers = {
        ans.question.id: ans.selected_choice.id
        for ans in attempt.studentanswer_set.all()
    }
    
    return render(request, 'academy/quiz_result.html', {
        'attempt': attempt,
        'questions': quiz.question_set.all(),
        'student_answers': student_answers
    })

# ------------------------------
# Assignment dashboard
# ------------------------------

def assignment_dashboard(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)

    return render(request, 'assignment/dashboard.html', {
        'assignment': assignment,
        'submissions': submissions
    })


from django.views.decorators.http import require_POST


# ------------------------------
# GRADE SUBMISSION
# ------------------------------
@require_POST
def grade_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    submission.grade = request.POST.get('grade')
    submission.feedback = request.POST.get('feedback')
    submission.save()

    return redirect('assignment_dashboard', assignment_id=submission.assignment.id)





def student_assignments(request):
    assignments = Assignment.objects.all()
    submissions = AssignmentSubmission.objects.filter(student=request.user)

    submission_dict = {
        sub.assignment.id: sub for sub in submissions
    }

    return render(request, 'assignment/student_assignments.html', {
        'assignments': assignments,
        'submission_dict': submission_dict
    })