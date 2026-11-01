from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test

from .models import Register, Card, Transaction, FraudAlert


# ---------------- CUSTOMER REGISTRATION ----------------

def register(request):

    if request.method == "POST":

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not name or not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('register')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')

        Register.objects.create(
            name=name,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


# ---------------- COMMON LOGIN ----------------

def login(request):

    if request.method == "POST":

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # ADMIN LOGIN

        admin_user = authenticate(
            request,
            username=email,
            password=password
        )

        if admin_user is not None and admin_user.is_staff:

            auth_login(request, admin_user)

            return redirect('admin_dashboard')

        # CUSTOMER LOGIN

        customer = Register.objects.filter(
            email=email,
            password=password
        ).first()

        if customer:

            if customer.is_blocked:

                messages.error(
                    request,
                    "Your account has been blocked. Please contact the administrator."
                )

                return redirect('login')

            request.session['user_id'] = customer.id
            request.session['user_name'] = customer.name

            return redirect('dashboard')

        messages.error(request, "Invalid email or password.")

        return redirect('login')

    return render(request, 'login.html')


# ---------------- CUSTOMER DASHBOARD ----------------

def dashboard(request):

    user_id = request.session.get('user_id')

    if not user_id:

        messages.error(request, "Please log in first.")
        return redirect('login')

    customer = Register.objects.filter(id=user_id).first()

    if not customer or customer.is_blocked:

        request.session.flush()

        messages.error(
            request,
            "Your account is blocked or unavailable."
        )

        return redirect('login')

    return render(request, 'dashboard.html')


# ---------------- CUSTOMER LOGOUT ----------------

def customer_logout(request):

    request.session.flush()

    messages.success(request, "You have logged out successfully.")

    return redirect('login')


# ---------------- HOME PAGE ----------------

def home(request):

    return render(request, 'home.html')


# ---------------- ADMIN DASHBOARD ----------------

@user_passes_test(
    lambda user: user.is_staff,
    login_url='login'
)
def admin_dashboard(request):

    total_customers = Register.objects.count()
    total_cards = Card.objects.count()
    total_transactions = Transaction.objects.count()
    total_fraud = FraudAlert.objects.count()

    recent_transactions = Transaction.objects.select_related(
        'card'
    ).order_by('-txn_time')[:10]

    # Get registered customers
    customers = Register.objects.all().order_by('-id')

    context = {
        'total_customers': total_customers,
        'total_cards': total_cards,
        'total_transactions': total_transactions,
        'total_fraud': total_fraud,
        'recent_transactions': recent_transactions,
        'customers': customers,
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


# ---------------- ADMIN VIEW CUSTOMERS ----------------

@user_passes_test(
    lambda user: user.is_staff,
    login_url='login'
)
def admin_customers(request):

    customers = Register.objects.all().order_by('-id')

    context = {
        'customers': customers,
    }

    return render(
        request,
        'admin_customers.html',
        context
    )


# ---------------- ADMIN BLOCK / UNBLOCK CUSTOMER ----------------

@user_passes_test(
    lambda user: user.is_staff,
    login_url='login'
)
def toggle_customer_status(request, customer_id):

    if request.method == 'POST':

        customer = get_object_or_404(
            Register,
            id=customer_id
        )

        customer.is_blocked = not customer.is_blocked

        customer.save()

        if customer.is_blocked:

            messages.success(
                request,
                f'{customer.name} has been blocked.'
            )

        else:

            messages.success(
                request,
                f'{customer.name} has been unblocked.'
            )

    return redirect('admin_customers')


# ---------------- ADMIN LOGOUT ----------------

@user_passes_test(
    lambda user: user.is_staff,
    login_url='login'
)
def admin_logout(request):

    auth_logout(request)

    messages.success(
        request,
        "Admin logged out successfully."
    )

    return redirect('login')