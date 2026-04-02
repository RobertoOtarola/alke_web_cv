from django.contrib import admin
from .models import Proyecto, CaseStudy

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'destacado', 'orden', 'fecha_creacion')
    list_filter = ('destacado',)
    search_fields = ('nombre', 'descripcion', 'tecnologias')

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'slug', 'subtitle')
    prepopulated_fields = {'slug': ('proyecto',)}
    fieldsets = (
        (None, {
            'fields': ('proyecto', 'slug', 'subtitle', 'image', 'skills_applied'),
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
