from django.urls import path
from . import views

urlpatterns = [
    path('', views.PublicQuestionListView.as_view(), name='index'),
    path('<slug:slug>-<int:pk>', views.QuestionDetailView.as_view(),
        name = 'question-detail'),
    path('ask', views.submit_question, name='submit-question'),
    path('success', views.submit_question_success, name='submit-success'),
    #path('youarenotsupposedtobehere',
        #views.AllQuestionListView.as_view(), name='peaccess'),


    # Peer access only.
    # Question list.
    path('peaccess', views.all_question_list, name='peaccess'),
    path('peaccess/all', views.AllQuestionList.as_view(), name='pe-all'),
    path('ajax/categories', views.getCategories, name='get_categories'),
    # Edit questions.
    path('peaccess/<slug:slug>/edit',
        views.QuestionEditView.as_view(), name='edit-question'),
    # Edit categories.
    path('categories', views.CategoryListAddView.as_view(),
        name='add-view-category'),
]
