from django.contrib import admin

from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('project', 'slug', 'subtitle')
    prepopulated_fields = {'slug': ('project',)}
    fieldsets = (
        (None, {
            'fields': ('project', 'slug', 'subtitle', 'image', 'skills_applied'),
        }),
        ('Secciones del Caso de Estudio', {
            'classes': ('collapse',),
            'fields': (
                'section_1_description',
                'section_2_challenge',
                'section_3_solution',
                'section_4_tools',
                'section_5_learnings',
                'section_6_metrics',
                'section_7_skills',
                'section_8_justification',
            ),
        }),
    )
