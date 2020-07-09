from django.urls import path
from . import views

urlpatterns = [
    path('', views.PublicQuestionListView.as_view(), name='index'),
    path('<slug:slug>-<int:pk>', views.QuestionDetailView.as_view(),
        name = 'question-detail'),
    path('ask', views.submit_question, name='submit-question'),
    path('success', views.submit_question_success, name='submit-success'),
    path('youarenotsupposedtobehere',
        views.AllQuestionListView.as_view(), name = 'peaccess'),
    path('youarenotsupposedtobehere/<status>',
        views.QuestionByStatusListView.as_view(), name = 'peaccess-filter'),
    path('youarenotsupposedtobehere/<int:pk>/edit',
             views.QuestionEditView.as_view(), name = 'edit-question'),
    path('categories', views.CategoryListAddView.as_view(),
        name='add-view-category'),
]
