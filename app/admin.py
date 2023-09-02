from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin

from .models import Choice, Question, LatexDoc, Molecule


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(ImportExportModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)


class LatexDocAdmin(ImportExportModelAdmin):
    list_display = ('name','content', 'creat_date', 'latex_type')

admin.site.register(LatexDoc, LatexDocAdmin)

class MoleculeAdmin(ImportExportModelAdmin):
    list_display = ('name','content', 'creat_date')

admin.site.register(Molecule, MoleculeAdmin)