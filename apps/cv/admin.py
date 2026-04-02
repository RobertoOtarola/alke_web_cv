from django.contrib import admin

from .models import (
    Achievement, Certification, Education, Experience,
    Language, Presentation, Profile, Publication, Skill,
)


class AchievementInline(admin.TabularInline):
    model  = Achievement
    extra  = 1
    fields = ("description",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines       = [AchievementInline]
    list_display  = ("role", "company", "location", "start_date", "end_date", "featured")
    list_filter   = ("featured",)
    search_fields = ("role", "company", "location")
    list_editable = ("featured",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "location", "email")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ("name", "category")
    list_filter   = ("category",)
    search_fields = ("name",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_year", "year")
    ordering     = ("-year",)




@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "level")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display  = ("name", "institution", "year")
    ordering      = ("-year",)
    search_fields = ("name", "institution")


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display  = ("title", "publication_type", "event", "year")
    list_filter   = ("publication_type",)
    search_fields = ("title",)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display  = ("event", "location", "year", "topic")
    search_fields = ("event", "topic")
