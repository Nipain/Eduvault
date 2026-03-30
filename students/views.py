from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentAdmissionForm
from django.contrib import messages 
from .models import Student, Class
import re
from accounts.decorators import role_required

@role_required(["admin"])
def add_student(request):
    if request.method == "POST":
        form = StudentAdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully")  # ✅ message added
            return redirect("add_student")  # stay on same page
        else:
            print(form.errors)
    else:
        form = StudentAdmissionForm()

    return render(request, "students/add_student.html", {"form": form})

@role_required(["admin"])
def edit_student(request, pk):
    # Fetch the student or return 404 if not found
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == "POST":
        # Passing 'instance=student' tells Django to update the existing record
        form = StudentAdmissionForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Details for {student.name} updated successfully!")
            return redirect("student_list") # Redirect back to the list
    else:
        # Populate the form with current student data
        form = StudentAdmissionForm(instance=student)

    return render(request, "students/add_student.html", {
        "form": form,
        "is_edit": True, # Useful for changing the page title
        "student": student
    })

@role_required(["admin"])
def promote_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    current_class_name = student.student_class.name # e.g., "1st"
    
    # 1. Extract the number
    match = re.search(r'\d+', current_class_name)
    
    if match:
        current_num = int(match.group())
        next_num = current_num + 1
        
        # 2. Smart Suffix Logic (Handle 1st, 2nd, 3rd, 4th...)
        if 11 <= (next_num % 100) <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(next_num % 12, 'th')
            
        target_name = f"{next_num}{suffix}" # Result: "2nd"
        
        try:
            # 3. Look for the actual Class object
            next_class_obj = Class.objects.get(name__iexact=target_name)
            student.student_class = next_class_obj
            student.save()
            messages.success(request, f"Success! {student.name} is now in {next_class_obj.name}")
        
        except Class.DoesNotExist:
            messages.error(request, f"Error: Class '{target_name}' does not exist in the database. Please create it first.")
    else:
        messages.error(request, "Could not identify a numeric grade level in the current class name.")
        
    return redirect("student_list")

from django.db.models import Q

@role_required(["admin"])
def student_list(request):
    query = request.GET.get('search', '')
    
    if query:
        # Search by name OR unique_id
        students = Student.objects.filter(
            Q(name__icontains=query) | 
            Q(unique_id__icontains=query)
        ).order_by('-id')
    else:
        # Default: 10 most recent students
        students = Student.objects.all().order_by('-id')[:10]
        
    return render(request, "students/student_list.html", {
        "students": students,
        "search_query": query
    })