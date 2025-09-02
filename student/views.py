# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Semester
from django.db.models import Q

def student_list(request):
    search_query = request.GET.get("search", "")
    semesters = Semester.objects.all()

    students_by_semester = {}
    for semester in semesters:
        students = semester.student_set.filter(
            Q(name__icontains=search_query) | Q(student_id__icontains=search_query)
        )
        students_by_semester[semester] = students

    blank_students = Student.objects.filter(semester=None).filter(
        Q(name__icontains=search_query) | Q(student_id__icontains=search_query)
    )

    return render(request, 'students/student_list.html', {
        'students_by_semester': students_by_semester,
        'blank_students': blank_students,
        'search_query': search_query
    })


def remove_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.previous_semester = student.semester
    student.semester = None
    student.save()
    return redirect('student_list')


def assign_students(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
    blank_students = Student.objects.filter(semester=None)

    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        Student.objects.filter(id__in=student_ids).update(semester=semester)
        return redirect('student_list')

    return render(request, 'students/assign_students.html', {
        'semester': semester,
        'blank_students': blank_students
    })
