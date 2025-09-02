from student.models import Student
from teacher.models import Teacher
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.forms import formset_factory
from .models import Part, Class, CT, Exam, Student, Attendance, CTResult, ExamResult
from .forms import ClassForm, CTForm, ExamForm, AttendanceForm, CTResultForm, ExamResultForm

# ---------------------------- Teacher Part View ----------------------------

@method_decorator(login_required, name='dispatch')
class TeacherPartListView(View):
    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        parts = Part.objects.filter(teacher=teacher).select_related('course', 'course__semester')
        return render(request, 'teacher_part_list.html', {
            'teacher': teacher,
            'parts': parts,
        })

 # Assuming your models are in .models

# Add these imports if they are not already present
from .models import Part, Class, CT, Exam, Student, Attendance, CTResult, ExamResult 


def part_detail(request, part_id):
    part = get_object_or_404(Part, id=part_id)

    # Get all classes, CTs, and exams for this part, ordered for consistent display
    # Use the same descending order for both class headers and data fetching
    classes_ordered = Class.objects.filter(part=part).order_by('-class_number')

    # CORRECTED: Changed 'name' to 'topic' for Exam ordering
    # Assuming CT also has 'topic' or 'ct_number' for ordering
    cts = CT.objects.filter(part=part).order_by('ct_number') # Use 'ct_number' if it exists, otherwise 'topic'
    exams = Exam.objects.filter(part=part).order_by('topic') # CORRECTED: Changed 'name' to 'topic'

    # Get students for this part (from the semester associated with the part's course)
    students = Student.objects.filter(semester=part.course.semester) 

    # Prepare detailed data for each student including attendance, CTs, and Exams
    student_data_overview = {}

    for student in students:
        # --- Class Attendance Data ---
        student_classes_statuses = []
        present_count = 0
        
        for class_obj in classes_ordered: 
            try:
                attendance = Attendance.objects.get(class_session=class_obj, student=student)
                student_classes_statuses.append(attendance.status)
                if attendance.status == 'P':
                    present_count += 1
            except Attendance.DoesNotExist:
                student_classes_statuses.append('N/A')
        
        total_recorded_classes = len(student_classes_statuses)
        percentage = 0
        if total_recorded_classes > 0:
            percentage = (present_count / total_recorded_classes) * 100

        # --- CT Marks Data ---
        student_ct_marks = []
        for ct_obj in cts:
            try:
                ct_mark = CTResult.objects.get(ct=ct_obj, student=student)
                student_ct_marks.append(str(ct_mark.marks)) 
            except CTResult.DoesNotExist:
                student_ct_marks.append('N/A')

        # --- Exam Marks Data ---
        student_exam_marks = []
        for exam_obj in exams:
            try:
                exam_mark = ExamResult.objects.get(exam=exam_obj, student=student)
                student_exam_marks.append(str(exam_mark.marks)) 
            except ExamResult.DoesNotExist:
                student_exam_marks.append('N/A')

        # Store all collected data for the current student
        student_data_overview[student] = {
            'attendance': {
                'list': student_classes_statuses,
                'present_count': present_count,
                'total_recorded': total_recorded_classes,
                'percentage': percentage
            },
            'cts': student_ct_marks,
            'exams': student_exam_marks,
        }

    # Sort the student_data_overview by attendance percentage (descending)
    # Secondary sort by student name for tie-breaking
    sorted_student_data = sorted(
        student_data_overview.items(),
        key=lambda item: (item[1]['attendance']['percentage'], item[0].name),
        reverse=True
    )

    context = {
        'part': part,
        'classes': classes_ordered, 
        'cts': cts, 
        'exams': exams, 
        'sorted_student_data': sorted_student_data, 
    }
    return render(request, 'courses/part_detail.html', context)
# class, ct ,exam cre


def create_class(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    students = Student.objects.filter(semester=part.course.semester)
    
    # Get next class number
    last_class = Class.objects.filter(part=part).order_by('-class_number').first()
    next_class_number = (last_class.class_number + 1) if last_class else 1
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create class
                class_obj = form.save(commit=False)
                class_obj.part = part
                class_obj.class_number = next_class_number
                class_obj.save()
                
                # Create attendance records
                for student in students:
                    status = request.POST.get(f'attendance_{student.id}', 'P')
                    Attendance.objects.create(
                        class_session=class_obj,
                        student=student,
                        status=status
                    )
                
                messages.success(request, 'Class created successfully!')
                return redirect('part_detail', part_id=part.id)
    else:
        form = ClassForm()
    
    context = {
        'form': form,
        'part': part,
        'students': students,
        'next_class_number': next_class_number,
    }
    return render(request, 'courses/create_class.html', context)

def create_ct(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    students = Student.objects.filter(semester=part.course.semester)


    
    # Get next CT number
    last_ct = CT.objects.filter(part=part).order_by('-ct_number').first()
    next_ct_number = (last_ct.ct_number + 1) if last_ct else 1
    
    if request.method == 'POST':
        form = CTForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create CT
                ct_obj = form.save(commit=False)
                ct_obj.part = part
                ct_obj.ct_number = next_ct_number
                ct_obj.save()
                
                # Create CT results
                for student in students:
                    marks = request.POST.get(f'marks_{student.id}', 0)
                    CTResult.objects.create(
                        ct=ct_obj,
                        student=student,
                        marks=float(marks) if marks else 0
                    )
                
                messages.success(request, 'CT created successfully!')
                return redirect('part_detail', part_id=part.id)
    else:
        form = CTForm()
    
    context = {
        'form': form,
        'part': part,
        'students': students,
        'next_ct_number': next_ct_number,
    }
    return render(request, 'courses/create_ct.html', context)

def create_exam(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    students = Student.objects.filter(semester=part.course.semester)
    
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create Exam
                exam_obj = form.save(commit=False)
                exam_obj.part = part
                exam_obj.save()
                
                # Create exam results
                for student in students:
                    marks = request.POST.get(f'marks_{student.id}', 0)
                    ExamResult.objects.create(
                        exam=exam_obj,
                        student=student,
                        marks=float(marks) if marks else 0
                    )
                
                messages.success(request, 'Exam created successfully!')
                return redirect('part_detail', part_id=part.id)
    else:
        form = ExamForm()
    
    context = {
        'form': form,
        'part': part,
        'students': students,
    }
    return render(request, 'courses/create_exam.html', context)

def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(semester=class_obj.part.course.semester)
    
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                
                # Update attendance records
                for student in students:
                    status = request.POST.get(f'attendance_{student.id}', 'P')
                    attendance, created = Attendance.objects.get_or_create(
                        class_session=class_obj,
                        student=student,
                        defaults={'status': status}
                    )
                    if not created:
                        attendance.status = status
                        attendance.save()
                
                messages.success(request, 'Class updated successfully!')
                return redirect('part_detail', part_id=class_obj.part.id)
    else:
        form = ClassForm(instance=class_obj)
    
    # Get current attendance data
    attendance_data = {}
    for student in students:
        try:
            attendance = Attendance.objects.get(class_session=class_obj, student=student)
            attendance_data[student.id] = attendance.status
        except Attendance.DoesNotExist:
            attendance_data[student.id] = 'P'
    
    context = {
        'form': form,
        'class_obj': class_obj,
        'students': students,
        'attendance_data': attendance_data,
    }
    return render(request, 'courses/edit_class.html', context)

def edit_ct(request, ct_id):
    ct_obj = get_object_or_404(CT, id=ct_id)
    students = Student.objects.filter(semester=ct_obj.part.course.semester)
    
    if request.method == 'POST':
        form = CTForm(request.POST, instance=ct_obj)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                
                # Update CT results
                for student in students:
                    marks = request.POST.get(f'marks_{student.id}', 0)
                    result, created = CTResult.objects.get_or_create(
                        ct=ct_obj,
                        student=student,
                        defaults={'marks': float(marks) if marks else 0}
                    )
                    if not created:
                        result.marks = float(marks) if marks else 0
                        result.save()
                
                messages.success(request, 'CT updated successfully!')
                return redirect('part_detail', part_id=ct_obj.part.id)
    else:
        form = CTForm(instance=ct_obj)
    
    # Get current marks data
    marks_data = {}
    for student in students:
        try:
            result = CTResult.objects.get(ct=ct_obj, student=student)
            marks_data[student.id] = result.marks
        except CTResult.DoesNotExist:
            marks_data[student.id] = 0
    
    context = {
        'form': form,
        'ct_obj': ct_obj,
        'students': students,
        'marks_data': marks_data,
    }
    return render(request, 'courses/edit_ct.html', context)

def edit_exam(request, exam_id):
    exam_obj = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(semester=exam_obj.part.course.semester)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam_obj)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                
                # Update exam results
                for student in students:
                    marks = request.POST.get(f'marks_{student.id}', 0)
                    result, created = ExamResult.objects.get_or_create(
                        exam=exam_obj,
                        student=student,
                        defaults={'marks': float(marks) if marks else 0}
                    )
                    if not created:
                        result.marks = float(marks) if marks else 0
                        result.save()
                
                messages.success(request, 'Exam updated successfully!')
                return redirect('part_detail', part_id=exam_obj.part.id)
    else:
        form = ExamForm(instance=exam_obj)
    
    # Get current marks data
    marks_data = {}
    for student in students:
        try:
            result = ExamResult.objects.get(exam=exam_obj, student=student)
            marks_data[student.id] = result.marks
        except ExamResult.DoesNotExist:
            marks_data[student.id] = 0
    
    context = {
        'form': form,
        'exam_obj': exam_obj,
        'students': students,
        'marks_data': marks_data,
    }
    return render(request, 'courses/edit_exam.html', context)

def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    part_id = class_obj.part.id
    class_obj.delete()
    messages.success(request, 'Class deleted successfully!')
    return redirect('part_detail', part_id=part_id)

def delete_ct(request, ct_id):
    ct_obj = get_object_or_404(CT, id=ct_id)
    part_id = ct_obj.part.id
    ct_obj.delete()
    messages.success(request, 'CT deleted successfully!')
    return redirect('part_detail', part_id=part_id)

def delete_exam(request, exam_id):
    exam_obj = get_object_or_404(Exam, id=exam_id)
    part_id = exam_obj.part.id
    exam_obj.delete()
    messages.success(request, 'Exam deleted successfully!')
    return redirect('part_detail', part_id=part_id)