from django.contrib import admin
from .models import *


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
