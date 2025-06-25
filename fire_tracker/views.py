from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, date
from decimal import Decimal
import json
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.views.generic import TemplateView

from .models import UserProfile, MonthlyTracking, FireProgress, Goal, InflationData
from django.conf import settings


@login_required
def dashboard(request):
    """Main dashboard showing FIRE progress and key metrics"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('fire_tracker:setup_profile')
    
    # Get recent monthly tracking data
    recent_tracking = MonthlyTracking.objects.filter(user=request.user).order_by('-month')[:12]
    
    # Get FIRE progress history
    progress_history = FireProgress.objects.filter(user=request.user).order_by('-date')[:12]
    
    # Get user goals
    goals = Goal.objects.filter(user=request.user, is_completed=False)
    
    # Calculate additional metrics
    total_savings = MonthlyTracking.objects.filter(user=request.user).aggregate(
        total_savings=Sum('income') - Sum('expenses')
    )['total_savings'] or 0
    
    avg_savings_rate = MonthlyTracking.objects.filter(user=request.user).aggregate(
        avg_rate=Avg('savings_rate')
    )['avg_rate'] or 0
    
    # Get currency symbol
    currency_symbol = settings.FIRE_SETTINGS[profile.country]['currency_symbol']

    # Calculate FIRE numbers
    withdrawal_rate = float(profile.withdrawal_rate)
    annual_expenses = float(profile.annual_expenses)
    lean_expenses = annual_expenses * 0.7
    fat_expenses = annual_expenses * 1.5
    barista_expenses = annual_expenses * 0.85

    fire_numbers = {
        'Regular FIRE': annual_expenses * (100 / withdrawal_rate),
        'Lean FIRE': lean_expenses * (100 / withdrawal_rate),
        'Fat FIRE': fat_expenses * (100 / withdrawal_rate),
        'Barista FIRE': barista_expenses * (100 / withdrawal_rate),
    }

    # Coast FIRE calculation (approximate):
    # FV = FIRE number, PV = ? (what you need now), n = years to retirement, r = expected return
    # PV = FV / (1 + r)^n
    years_to_retirement = profile.target_retirement_age - profile.current_age
    expected_return = float(profile.expected_return_rate) / 100
    regular_fire = fire_numbers['Regular FIRE']
    if years_to_retirement > 0 and expected_return > 0:
        coast_fire = regular_fire / ((1 + expected_return) ** years_to_retirement)
    else:
        coast_fire = 0
    fire_numbers['Coast FIRE'] = coast_fire

    context = {
        'profile': profile,
        'recent_tracking': recent_tracking,
        'progress_history': progress_history,
        'goals': goals,
        'total_savings': total_savings,
        'avg_savings_rate': avg_savings_rate,
        'currency_symbol': currency_symbol,
        'fire_numbers': fire_numbers,
    }
    
    return render(request, 'fire_tracker/dashboard.html', context)


@login_required
def setup_profile(request):
    """Setup or update user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        is_update = True
    except UserProfile.DoesNotExist:
        profile = None
        is_update = False
    
    if request.method == 'POST':
        if profile:
            # Update existing profile
            profile.country = request.POST.get('country')
            profile.target_retirement_age = int(request.POST.get('target_retirement_age'))
            profile.current_age = int(request.POST.get('current_age'))
            profile.annual_income = Decimal(request.POST.get('annual_income'))
            profile.annual_expenses = Decimal(request.POST.get('annual_expenses'))
            profile.current_net_worth = Decimal(request.POST.get('current_net_worth'))
            profile.inflation_rate = Decimal(request.POST.get('inflation_rate'))
            profile.expected_return_rate = Decimal(request.POST.get('expected_return_rate'))
            profile.withdrawal_rate = Decimal(request.POST.get('withdrawal_rate'))
            profile.save()
        else:
            # Create new profile
            profile = UserProfile.objects.create(
                user=request.user,
                country=request.POST.get('country'),
                target_retirement_age=int(request.POST.get('target_retirement_age')),
                current_age=int(request.POST.get('current_age')),
                annual_income=Decimal(request.POST.get('annual_income')),
                annual_expenses=Decimal(request.POST.get('annual_expenses')),
                current_net_worth=Decimal(request.POST.get('current_net_worth')),
                inflation_rate=Decimal(request.POST.get('inflation_rate')),
                expected_return_rate=Decimal(request.POST.get('expected_return_rate')),
                withdrawal_rate=Decimal(request.POST.get('withdrawal_rate')),
            )
        
        # Create initial FIRE progress entry
        FireProgress.objects.create(
            user=request.user,
            date=date.today(),
            fire_number=profile.fire_number,
            current_net_worth=profile.current_net_worth,
            progress_percentage=profile.fire_progress_percentage,
            years_to_fire=profile.years_to_fire,
        )
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('fire_tracker:dashboard')
    
    # Get default values based on country
    default_country = 'USA'
    if profile:
        default_country = profile.country
    
    default_settings = settings.FIRE_SETTINGS[default_country]
    
    context = {
        'profile': profile,
        'is_update': is_update,
        'default_settings': default_settings,
        'countries': UserProfile.COUNTRY_CHOICES,
        'currency_symbol': default_settings['currency_symbol'],
    }
    
    return render(request, 'fire_tracker/setup_profile.html', context)


@login_required
def monthly_tracking(request):
    """Add or update monthly tracking data"""
    if request.method == 'POST':
        month_str = request.POST.get('month')
        month_date = datetime.strptime(month_str, '%Y-%m').date().replace(day=1)
        
        income = Decimal(request.POST.get('income'))
        expenses = Decimal(request.POST.get('expenses'))
        net_worth = Decimal(request.POST.get('net_worth'))
        notes = request.POST.get('notes', '')
        
        # Update or create monthly tracking
        tracking, created = MonthlyTracking.objects.update_or_create(
            user=request.user,
            month=month_date,
            defaults={
                'income': income,
                'expenses': expenses,
                'net_worth': net_worth,
                'notes': notes,
            }
        )
        
        # Update user profile with latest net worth
        profile = UserProfile.objects.get(user=request.user)
        profile.current_net_worth = net_worth
        profile.save()
        
        # Create FIRE progress entry
        FireProgress.objects.create(
            user=request.user,
            date=date.today(),
            fire_number=profile.fire_number,
            current_net_worth=net_worth,
            progress_percentage=profile.fire_progress_percentage,
            years_to_fire=profile.years_to_fire,
        )
        
        messages.success(request, f'Monthly data for {month_date.strftime("%B %Y")} saved successfully!')
        return redirect('monthly_tracking')
    
    # Get existing tracking data
    tracking_data = MonthlyTracking.objects.filter(user=request.user).order_by('-month')
    
    # Get user profile for currency symbol
    try:
        profile = UserProfile.objects.get(user=request.user)
        currency_symbol = settings.FIRE_SETTINGS[profile.country]['currency_symbol']
    except UserProfile.DoesNotExist:
        currency_symbol = '$'  # Default fallback
    
    # Pagination
    paginator = Paginator(tracking_data, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tracking_data': tracking_data,
        'currency_symbol': currency_symbol,
    }
    
    return render(request, 'fire_tracker/monthly_tracking.html', context)


@login_required
def edit_monthly_tracking(request, tracking_id):
    """Edit existing monthly tracking entry"""
    tracking = get_object_or_404(MonthlyTracking, id=tracking_id, user=request.user)
    
    if request.method == 'POST':
        tracking.income = Decimal(request.POST.get('income'))
        tracking.expenses = Decimal(request.POST.get('expenses'))
        tracking.net_worth = Decimal(request.POST.get('net_worth'))
        tracking.notes = request.POST.get('notes', '')
        tracking.save()
        
        # Update user profile if this is the most recent entry
        latest_tracking = MonthlyTracking.objects.filter(user=request.user).order_by('-month').first()
        if latest_tracking == tracking:
            profile = UserProfile.objects.get(user=request.user)
            profile.current_net_worth = tracking.net_worth
            profile.save()
        
        messages.success(request, 'Monthly tracking updated successfully!')
        return redirect('monthly_tracking')
    
    context = {
        'tracking': tracking,
        'currency_symbol': settings.FIRE_SETTINGS[UserProfile.objects.get(user=request.user).country]['currency_symbol'],
    }
    
    return render(request, 'fire_tracker/edit_monthly_tracking.html', context)


@login_required
def goals(request):
    """Manage financial goals"""
    if request.method == 'POST':
        name = request.POST.get('name')
        goal_type = request.POST.get('goal_type')
        target_amount = Decimal(request.POST.get('target_amount'))
        target_date_str = request.POST.get('target_date')
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date() if target_date_str else None
        
        Goal.objects.create(
            user=request.user,
            name=name,
            goal_type=goal_type,
            target_amount=target_amount,
            target_date=target_date,
        )
        
        messages.success(request, 'Goal created successfully!')
        return redirect('goals')
    
    goals_list = Goal.objects.filter(user=request.user).order_by('-created_at')
    
    # Get user profile for currency symbol
    try:
        profile = UserProfile.objects.get(user=request.user)
        currency_symbol = settings.FIRE_SETTINGS[profile.country]['currency_symbol']
    except UserProfile.DoesNotExist:
        currency_symbol = '$'  # Default fallback
    
    context = {
        'goals': goals_list,
        'goal_types': Goal.GOAL_TYPES,
        'currency_symbol': currency_symbol,
    }
    
    return render(request, 'fire_tracker/goals.html', context)


@login_required
def update_goal_progress(request, goal_id):
    """Update goal progress"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        current_amount = Decimal(request.POST.get('current_amount'))
        goal.current_amount = current_amount
        
        # Check if goal is completed
        if current_amount >= goal.target_amount:
            goal.is_completed = True
        
        goal.save()
        
        messages.success(request, 'Goal progress updated successfully!')
        return redirect('goals')
    
    context = {
        'goal': goal,
        'currency_symbol': settings.FIRE_SETTINGS[UserProfile.objects.get(user=request.user).country]['currency_symbol'],
    }
    
    return render(request, 'fire_tracker/update_goal_progress.html', context)


@login_required
def analytics(request):
    """Detailed analytics and charts"""
    profile = UserProfile.objects.get(user=request.user)
    
    # Get tracking data for charts
    tracking_data = MonthlyTracking.objects.filter(user=request.user).order_by('month')
    
    # Prepare data for charts
    months = [entry.month.strftime('%b %Y') for entry in tracking_data]
    net_worth_data = [float(entry.net_worth) for entry in tracking_data]
    savings_rate_data = [float(entry.savings_rate) for entry in tracking_data]
    income_data = [float(entry.income) for entry in tracking_data]
    expenses_data = [float(entry.expenses) for entry in tracking_data]
    
    # Calculate additional metrics
    total_months = tracking_data.count()
    avg_monthly_income = tracking_data.aggregate(avg=Avg('income'))['avg'] or 0
    avg_monthly_expenses = tracking_data.aggregate(avg=Avg('expenses'))['avg'] or 0
    avg_savings_rate = tracking_data.aggregate(avg=Avg('savings_rate'))['avg'] or 0
    
    # Net worth growth
    if tracking_data.count() >= 2:
        first_net_worth = tracking_data.first().net_worth
        last_net_worth = tracking_data.last().net_worth
        net_worth_growth = ((last_net_worth - first_net_worth) / first_net_worth * 100) if first_net_worth > 0 else 0
    else:
        net_worth_growth = 0
    
    context = {
        'profile': profile,
        'months': json.dumps(months),
        'net_worth_data': json.dumps(net_worth_data),
        'savings_rate_data': json.dumps(savings_rate_data),
        'income_data': json.dumps(income_data),
        'expenses_data': json.dumps(expenses_data),
        'total_months': total_months,
        'avg_monthly_income': avg_monthly_income,
        'avg_monthly_expenses': avg_monthly_expenses,
        'avg_savings_rate': avg_savings_rate,
        'net_worth_growth': net_worth_growth,
        'currency_symbol': settings.FIRE_SETTINGS[profile.country]['currency_symbol'],
    }
    
    return render(request, 'fire_tracker/analytics.html', context)


@login_required
def fire_calculator(request):
    """Advanced FIRE calculator with different scenarios"""
    if request.method == 'POST':
        # Handle calculator form submission
        annual_expenses = Decimal(request.POST.get('annual_expenses'))
        withdrawal_rate = Decimal(request.POST.get('withdrawal_rate'))
        current_age = int(request.POST.get('current_age'))
        target_age = int(request.POST.get('target_age'))
        current_savings = Decimal(request.POST.get('current_savings'))
        monthly_contribution = Decimal(request.POST.get('monthly_contribution'))
        expected_return = Decimal(request.POST.get('expected_return'))
        
        # Calculate FIRE number
        fire_number = annual_expenses * (100 / withdrawal_rate)
        
        # Calculate years to FIRE
        years_to_fire = target_age - current_age
        
        # Calculate required monthly contribution
        required_monthly = calculate_required_contribution(
            current_savings, fire_number, years_to_fire, expected_return
        )
        
        lean_fire_amount = (annual_expenses or 40000) * 25
        regular_fire_amount = (annual_expenses or 60000) * 25
        fat_fire_amount = (annual_expenses or 100000) * 25
        barista_fire_amount = (annual_expenses or 60000) * 0.85 * 25
        # Coast FIRE calculation (approximate)
        years_to_retirement = target_age - current_age
        expected_return = float(expected_return) / 100 if expected_return else 0
        if years_to_retirement > 0 and expected_return > 0:
            coast_fire_amount = regular_fire_amount / ((1 + expected_return) ** years_to_retirement)
        else:
            coast_fire_amount = 0
        
        context = {
            'fire_number': fire_number,
            'years_to_fire': years_to_fire,
            'required_monthly': required_monthly,
            'current_monthly': monthly_contribution,
            'annual_expenses': annual_expenses,
            'withdrawal_rate': withdrawal_rate,
            'current_age': current_age,
            'target_age': target_age,
            'current_savings': current_savings,
            'monthly_contribution': monthly_contribution,
            'expected_return': expected_return,
            'currency_symbol': settings.FIRE_SETTINGS[UserProfile.objects.get(user=request.user).country]['currency_symbol'],
            'lean_fire_amount': lean_fire_amount,
            'regular_fire_amount': regular_fire_amount,
            'fat_fire_amount': fat_fire_amount,
            'barista_fire_amount': barista_fire_amount,
            'coast_fire_amount': coast_fire_amount,
        }
        
        return render(request, 'fire_tracker/fire_calculator.html', context)
    
    # Get currency symbol for empty form
    try:
        profile = UserProfile.objects.get(user=request.user)
        currency_symbol = settings.FIRE_SETTINGS[profile.country]['currency_symbol']
    except UserProfile.DoesNotExist:
        currency_symbol = '$'  # Default fallback
    
    # Provide default values for the strategy cards
    context = {
        'currency_symbol': currency_symbol,
        'lean_fire_amount': 40000 * 25,
        'regular_fire_amount': 60000 * 25,
        'fat_fire_amount': 100000 * 25,
        'barista_fire_amount': 60000 * 0.85 * 25,
        'coast_fire_amount': 0,
    }
    return render(request, 'fire_tracker/fire_calculator.html', context)


def calculate_required_contribution(current_savings, target_amount, years, return_rate):
    """Calculate required monthly contribution to reach target amount"""
    if years <= 0:
        return 0
    
    # Using the formula: FV = PV * (1 + r)^n + PMT * ((1 + r)^n - 1) / r
    # Solving for PMT: PMT = (FV - PV * (1 + r)^n) / ((1 + r)^n - 1) / r
    
    monthly_rate = return_rate / 100 / 12
    total_periods = years * 12
    
    if monthly_rate == 0:
        return (target_amount - current_savings) / total_periods
    
    future_value_factor = (1 + monthly_rate) ** total_periods
    required_monthly = (target_amount - current_savings * future_value_factor) / (
        (future_value_factor - 1) / monthly_rate
    )
    
    return max(required_monthly, 0)


@csrf_exempt
def api_fire_progress(request):
    """API endpoint for FIRE progress data"""
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        # Get user's FIRE progress
        progress_data = FireProgress.objects.filter(user_id=user_id).order_by('date')
        
        dates = [entry.date.strftime('%Y-%m-%d') for entry in progress_data]
        progress_percentages = [float(entry.progress_percentage) for entry in progress_data]
        
        return JsonResponse({
            'dates': dates,
            'progress': progress_percentages,
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'nav_profile': profile}
        except UserProfile.DoesNotExist:
            return {}
    return {}


@csrf_exempt
@login_required
def help_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        help_type = data.get('type')
        message = data.get('message')
        user = request.user
        subject = f"[FIRE up] {'Bug Report' if help_type == 'bug' else 'Feature Request'} from {user.username}"
        body = f"User: {user.username} ({user.email})\nType: {help_type}\n\nMessage:\n{message}"
        send_mail(
            subject,
            body,
            'noreply@fireup.com',
            ['fupsup25@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class CustomLoginView(LoginView):
    template_name = 'fire_tracker/login.html'
    extra_context = {'hide_nav': True}


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    extra_context = {'hide_nav': True}


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    extra_context = {'hide_nav': True}


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    extra_context = {'hide_nav': True}


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    extra_context = {'hide_nav': True}


# Placeholder for registration view
class CustomRegisterView(TemplateView):
    template_name = 'registration/register.html'
    extra_context = {'hide_nav': True}
