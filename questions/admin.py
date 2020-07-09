from django.contrib import admin
from .models import Category, Question, Reply

# Define admin classes for category
class CategoryAdmin(admin.ModelAdmin):
    pass

# Define admin classes for PublicQuestion
#class PublicQuestionAdmin(admin.ModelAdmin):
#    pass

# Define admin classes for PrivateQuestion
#class PrivateQuestionAdmin(admin.ModelAdmin):
#    pass

# Define admin class for questions in general
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ( 'category', 'post_date' )

    exclude = [ 'post_date', 'slug' ] # You don't have to manually fill out this

    # Section the display off into student action and admin action
    fieldsets = (
        ('Student Action', {
            'fields': ('subject', 'content', 'op_email')
        }),
        ('Admin Action', {
            'fields': ('reply', 'category', 'status')
        }),
    )

    list_display = ('subject', 'post_date')

# Define admin classes
class ReplyAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, ReplyAdmin)
