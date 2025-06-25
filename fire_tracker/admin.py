from django.contrib import admin
from .models import UserProfile, MonthlyTracking, FireProgress, Goal, InflationData


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'current_age', 'target_retirement_age', 'annual_income', 'annual_expenses', 'current_net_worth', 'fire_progress_percentage', 'years_to_fire']
    list_filter = ['country', 'target_retirement_age', 'inflation_rate', 'expected_return_rate', 'withdrawal_rate']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['fire_number', 'fire_progress_percentage', 'years_to_fire', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'country', 'current_age', 'target_retirement_age')
        }),
        ('Financial Information', {
            'fields': ('annual_income', 'annual_expenses', 'current_net_worth')
        }),
        ('FIRE Parameters', {
            'fields': ('inflation_rate', 'expected_return_rate', 'withdrawal_rate')
        }),
        ('Calculated Values', {
            'fields': ('fire_number', 'fire_progress_percentage', 'years_to_fire'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MonthlyTracking)
class MonthlyTrackingAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'income', 'expenses', 'savings_rate', 'net_worth']
    list_filter = ['month', 'savings_rate']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'month'
    readonly_fields = ['savings_rate', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'month')
        }),
        ('Financial Data', {
            'fields': ('income', 'expenses', 'net_worth')
        }),
        ('Additional Information', {
            'fields': ('notes', 'savings_rate')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FireProgress)
class FireProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'fire_number', 'current_net_worth', 'progress_percentage', 'years_to_fire']
    list_filter = ['date', 'progress_percentage']
    search_fields = ['user__username']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'date')
        }),
        ('Progress Data', {
            'fields': ('fire_number', 'current_net_worth', 'progress_percentage', 'years_to_fire')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'goal_type', 'target_amount', 'current_amount', 'progress_percentage', 'is_completed']
    list_filter = ['goal_type', 'is_completed', 'target_date']
    search_fields = ['user__username', 'name']
    readonly_fields = ['progress_percentage', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'name', 'goal_type')
        }),
        ('Financial Targets', {
            'fields': ('target_amount', 'current_amount', 'target_date')
        }),
        ('Status', {
            'fields': ('is_completed', 'progress_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InflationData)
class InflationDataAdmin(admin.ModelAdmin):
    list_display = ['country', 'year', 'inflation_rate']
    list_filter = ['country', 'year']
    search_fields = ['country', 'year']
    ordering = ['-year', 'country']
    
    fieldsets = (
        ('Data Information', {
            'fields': ('country', 'year', 'inflation_rate')
        }),
    )


# Customize admin site
admin.site.site_header = "FIRE Calculator Administration"
admin.site.site_title = "FIRE Calculator Admin"
admin.site.index_title = "Welcome to FIRE Calculator Administration"
