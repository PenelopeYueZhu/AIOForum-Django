from django.urls import path
from . import views

urlpatterns = [
   # path('', views.PublicQuestionListView.as_view(), name='index'),

    path('ask', views.submit_question, name='submit-question'),
    path('success', views.submit_question_success, name='submit-success'),

    # Public access.
    path('ajax/categories', views.getCategories, name='get_categories'),

    path('', views.public_question_list, name='index'),
    path('all/', views.PublicQuestionList.as_view(), name='public-all'),
    path('<slug:slug>', views.QuestionDetailView.as_view(),
        name='question-detail'),

    # Peer access only.
    # Question list.
    path('peaccess/all', views.all_question_list, name='peaccess'),
    path('peaccess/all/get', views.AllQuestionList.as_view(), name='pe-all'),
    # Edit questions.
    path('peaccess/<slug:slug>/edit',
        views.QuestionEditView.as_view(), name='edit-question'),
    # Edit categories.
    path('categories/', views.CategoryListAddView.as_view(),
        name='add-view-category'),
]
