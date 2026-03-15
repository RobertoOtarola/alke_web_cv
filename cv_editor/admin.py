from django.contrib import admin

# Register your models here.
from .models import Profile, Skill, Experience, Achievement, Education, Project, Language


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [AchievementInline]
    list_display = ('role', 'company', 'start_date', 'end_date')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'location')


admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Language)
