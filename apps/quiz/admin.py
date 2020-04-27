from django.contrib import admin
from apps.quiz.models import Quiz, Question, Answer, UserAnswer


class QuizAdmin(admin.ModelAdmin):
    filter_horizontal = ('users_passed',)


class AnswerInline(admin.TabularInline):
    extra = 0
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']
    list_filter = ('quiz',)
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'right', 'question']
    list_filter = ('question',)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'answer_id', 'question_id']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
