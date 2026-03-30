from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FeeCategory, FeeStructure, Invoice, Transaction
from students.models import Student, Class
from django.db import transaction # To ensure data integrity
from django.db.models import Q
from django.db.models import Sum
from accounts.decorators import role_required

# def fee_dashboard(request):
#     classes = Class.objects.all()
#     invoices = Invoice.objects.select_related('student', 'student__student_class').order_by('-created_at')
    
#     class_id = request.GET.get('student_class')
#     search_query = request.GET.get('search')

#     # 1. Filter by Dropdown Class
#     if class_id:
#         invoices = invoices.filter(student__student_class_id=class_id)
        
#     # 2. Filter by Search Box (Complex query)
#     if search_query:
#         invoices = invoices.filter(
#             Q(student__name__icontains=search_query) | 
#             Q(student__roll_number__icontains=search_query) |
#             Q(student__unique_id__icontains=search_query) |
#             Q(student__student_class__name__icontains=search_query)
#         )

#     context = {
#         "invoices": invoices,
#         "classes": classes,
#         "selected_class": class_id,
#     }
#     return render(request, "fees/fee_list.html", context)

@role_required(["admin"])
def generate_monthly_invoices(request):
    """View to trigger fee generation for a specific month/class."""
    if request.method == "POST":
        target_class_id = request.POST.get('student_class')
        month = int(request.POST.get('month'))
        year = 2026
        
        target_class = get_object_or_404(Class, id=target_class_id)
        students = Student.objects.filter(student_class=target_class)
        
        # Get all recurring fee structures for this class (Tuition, Transport, etc.)
        fee_structures = FeeStructure.objects.filter(student_class=target_class, is_recurring=True)
        
        if not fee_structures:
            messages.error(request, f"No fee structure defined for {target_class.name}.")
            return redirect('fee_dashboard')

        total_created = 0
        
        with transaction.atomic(): # If one fails, none are created
            for student in students:
                # Check if invoice already exists to prevent double billing
                if not Invoice.objects.filter(student=student, month=month, year=year).exists():
                    total_fee = sum([fs.amount for fs in fee_structures])
                    
                    Invoice.objects.create(
                        student=student,
                        month=month,
                        year=year,
                        total_amount=total_fee,
                        status='unpaid'
                    )
                    total_created += 1
        
        messages.success(request, f"Generated {total_created} invoices for {target_class.name}.")
        return redirect('fee_dashboard')

    classes = Class.objects.all()
    return render(request, "fees/generate_fees.html", {"classes": classes})

# def collect_payment(request, invoice_id):
#     invoice = get_object_or_404(Invoice, id=invoice_id)
    
#     if request.method == "POST":
#         amount = float(request.POST.get('amount'))
#         mode = request.POST.get('payment_mode')
#         ref = request.POST.get('reference_number')
        
#         if amount > float(invoice.balance):
#             messages.error(request, "Cannot pay more than the outstanding balance!")
#         else:
#             Transaction.objects.create(
#                 invoice=invoice,
#                 amount_paid=amount,
#                 payment_mode=mode,
#                 reference_number=ref
#             )
#             messages.success(request, f"Payment recorded! Status updated to {invoice.get_status_display()}.")
            
#         # Redirect back to the main dashboard
#         return redirect('fee_dashboard')
    
#     return render(request, "fees/collect_payment.html", {"invoice": invoice})

@role_required(["admin"])
def fee_dashboard(request):
    """Now listing 10 most recent STUDENTS by default."""
    classes = Class.objects.all()
    
    # Base query
    students = Student.objects.select_related('student_class').order_by('-id')
    
    class_id = request.GET.get('student_class')
    search_query = request.GET.get('search')

    # Apply filters
    if class_id:
        students = students.filter(student_class_id=class_id)
        
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | 
            Q(roll_number__icontains=search_query) |
            Q(unique_id__icontains=search_query)
        )

    # Apply "10 Recent" limit only if no search/filter is active
    is_filtered = bool(class_id or search_query)
    if not is_filtered:
        students = students[:10]

    return render(request, "fees/fee_list.html", {
        "students": students, 
        "classes": classes,
        "selected_class": class_id,
        "is_filtered": is_filtered
    })

@role_required(["admin"])
def collect_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        month = int(request.POST.get('month'))
        session_start_year = int(request.POST.get('year')) # This is 2026
        
        # LOGIC: If month is Jan, Feb, or March, it belongs to the NEXT calendar year
        if month in [1, 2, 3]:
            actual_year = session_start_year + 1
        else:
            actual_year = session_start_year

        amount = float(request.POST.get('amount'))
        mode = request.POST.get('payment_mode')

        fee_structures = FeeStructure.objects.filter(student_class=student.student_class)
        total_due = sum([fs.amount for fs in fee_structures])

        # Use actual_year instead of the raw POST year
        invoice, created = Invoice.objects.get_or_create(
            student=student,
            month=month,
            year=actual_year,
            defaults={'total_amount': total_due}
        )

        Transaction.objects.create(
            invoice=invoice,
            amount_paid=amount,
            payment_mode=mode,
            reference_number=request.POST.get('reference_number')
        )
        
        messages.success(request, f"Payment for {invoice.get_month_display()} {actual_year} recorded!")
        return redirect('fee_dashboard')

    return render(request, "fees/collect_payment.html", {"student": student})

@role_required(["admin"])
def student_fee_history(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    # Fetch invoices and their related transactions
    history = Invoice.objects.filter(student=student).prefetch_related('transactions').order_by('-year', '-month')
    
    # Calculate Totals
    total_fees = history.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_paid = history.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    total_balance = total_fees - total_paid

    context = {
        "student": student,
        "history": history,
        "total_fees_all_time": total_fees,
        "total_paid_all_time": total_paid,
        "total_balance": total_balance,
    }
    return render(request, "fees/student_fees_history.html", context)


