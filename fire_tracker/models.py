from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
import random


class Visitor(models.Model):
    """Track unique visitors to the application"""
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['ip_address', 'user_agent']
        ordering = ['-last_visit']
    
    def __str__(self):
        return f"Visitor {self.ip_address} - {self.visit_count} visits"
    
    @classmethod
    def get_total_visitors(cls):
        """Get total number of unique visitors"""
        return cls.objects.count()
    
    @classmethod
    def track_visit(cls, request):
        """Track a visit and return visitor count"""
        ip_address = cls.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        visitor, created = cls.objects.get_or_create(
            ip_address=ip_address,
            user_agent=user_agent,
            defaults={'visit_count': 1}
        )
        
        if not created:
            visitor.visit_count += 1
            visitor.save()
        
        return cls.get_total_visitors()
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfile(models.Model):
    """User profile with FIRE calculation preferences"""
    COUNTRY_CHOICES = [
        ('USA', 'United States'),
        ('INDIA', 'India'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    RISK_CHOICES = [
        ('NO', 'No Risk'),
        ('MOD', 'Moderate Risk'),
        ('HIGH', 'High Risk'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='USA')
    target_retirement_age = models.PositiveIntegerField(default=45)
    current_age = models.PositiveIntegerField()
    annual_income = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    annual_expenses = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    current_net_worth = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inflation_rate = models.DecimalField(max_digits=4, decimal_places=2, default=2.5)
    expected_return_rate = models.DecimalField(max_digits=4, decimal_places=2, default=7.0)
    withdrawal_rate = models.DecimalField(max_digits=4, decimal_places=2, default=4.0)  # 4% rule
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    financial_risk = models.CharField(max_length=4, choices=RISK_CHOICES, default='MOD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_emoji = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.country}"
    
    @property
    def fire_number(self):
        """Calculate FIRE number based on annual expenses and withdrawal rate"""
        return self.annual_expenses * (100 / self.withdrawal_rate)
    
    @property
    def years_to_fire(self):
        """Calculate years needed to reach FIRE"""
        if self.current_net_worth >= self.fire_number:
            return 0
        
        # Using the formula: FV = PV * (1 + r)^n + PMT * ((1 + r)^n - 1) / r
        # Where FV = fire_number, PV = current_net_worth, PMT = annual_savings, r = return_rate
        annual_savings = self.annual_income - self.annual_expenses
        
        if annual_savings <= 0:
            return None
        
        # Simplified calculation - can be made more complex with inflation adjustments
        remaining_amount = self.fire_number - self.current_net_worth
        years = 0
        current_amount = self.current_net_worth
        
        while current_amount < self.fire_number and years < 100:
            current_amount = current_amount * (1 + self.expected_return_rate / 100) + annual_savings
            years += 1
        
        return years
    
    @property
    def fire_progress_percentage(self):
        """Calculate progress percentage towards FIRE number"""
        if self.fire_number <= 0:
            return 0
        progress = (self.current_net_worth / self.fire_number) * 100
        return min(progress, 100)
    
    @property
    def random_profile_emoji(self):
        if self.gender == 'M':
            return random.choice(['👦', '🧑', '👨'])
        elif self.gender == 'F':
            return random.choice(['👧', '🧑‍🦰', '👩'])
        else:
            return random.choice(['🧑', '🧑‍🦱', '🧑‍🦰'])


class MonthlyTracking(models.Model):
    """Monthly tracking of income, expenses, and net worth"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()  # First day of the month
    income = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    expenses = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    net_worth = models.DecimalField(max_digits=15, decimal_places=2)
    savings_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"
    
    def save(self, *args, **kwargs):
        # Calculate savings rate
        if self.income > 0:
            self.savings_rate = ((self.income - self.expenses) / self.income) * 100
        super().save(*args, **kwargs)


class InflationData(models.Model):
    """Historical inflation data for different countries"""
    country = models.CharField(max_length=10, choices=UserProfile.COUNTRY_CHOICES)
    year = models.PositiveIntegerField()
    inflation_rate = models.DecimalField(max_digits=4, decimal_places=2)
    
    class Meta:
        unique_together = ['country', 'year']
        ordering = ['-year']
    
    def __str__(self):
        return f"{self.country} - {self.year}: {self.inflation_rate}%"


class FireProgress(models.Model):
    """Track FIRE progress over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    fire_number = models.DecimalField(max_digits=15, decimal_places=2)
    current_net_worth = models.DecimalField(max_digits=15, decimal_places=2)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    years_to_fire = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.progress_percentage}%"


class Goal(models.Model):
    """Financial goals and milestones"""
    GOAL_TYPES = [
        ('EMERGENCY_FUND', 'Emergency Fund'),
        ('DEBT_FREE', 'Debt Free'),
        ('FIRE_NUMBER', 'FIRE Number'),
        ('COAST_FIRE', 'Coast FIRE'),
        ('BARISTA_FIRE', 'Barista FIRE'),
        ('CUSTOM', 'Custom Goal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    @property
    def progress_percentage(self):
        if self.target_amount <= 0:
            return 0
        progress = (self.current_amount / self.target_amount) * 100
        return min(progress, 100)
