from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, DeletionMixin, CreateView
from django.views.generic.edit import FormView

from questions.models import Category, Question
from questions.forms import SubmitQuestionForm, CategoryFormSet

import datetime

# Create your views here.

class PublicQuestionListView(generic.ListView):
    paginate_by = 10
    model = Question
    # Only show questions that has been published.
    queryset = Question.objects.filter(status__iexact=Question.PUBLIC)

class QuestionDetailView(generic.DetailView):
    model = Question

# Show all the questions. Only Peers should have access to this.
class AllQuestionListView(generic.ListView):
    # Get all the questions from the database.
    paginate_by = 10
    model = Question

    # Use a different template since we want a different filter option on top.
    template_name = 'questions/peeraccess_question_list.html'

# Show the questions based on filtered results.
class QuestionByStatusListView(generic.ListView):
    paginate_by = 10

    # Use a different template since we want a different filter option on top.
    template_name = 'questions/peeraccess_question_list.html'

    # Filter the questions by their status.
    def get_queryset(self):
        status = self.kwargs['status']
        return Question.objects.filter(status__iexact=status)

# Peer access to update a question.
# Reference: https://stackoverflow.com/questions/51772361/
# how-to-include-delete-function-in-updateview-instead-a-deleteview
class QuestionEditView(DeletionMixin, UpdateView):
    model = Question
    fields = ['category', 'reply', 'status']
    template_name = 'questions/edit_question.html'
    success_url = reverse_lazy('peaccess')

    def post(self, request, *args, **kwargs):
        """ Handling update and delete quests in the form differently. """
        # When updating, manually update the quesiton object.
        if 'update_question' in self.request.POST:
            # Get the reference to the form and the question being edited.
            form = self.get_form()
            question = self.get_object()

            if form.is_valid():
                # Udpate the question with form data.
                question.reply = form.cleaned_data['reply']
                question.status = form.cleaned_data['status']
                # Clean the many-to-many field of category.
                question.category.clear()
                # Iterate through all the categories and add each one.
                for category in form.cleaned_data['category']:
                    question.category.add(category)
                question.save()

            return HttpResponseRedirect(reverse('submit-success'))

        else: # if 'delete_question' in self.request.POST, use deletionmixin.
            return self.delete(request, *args, **kwargs)


class CategoryListAddView(FormView):
    """ Display formset of categories for editing existed categories and adding
        new ones."""

    form_class = CategoryFormSet
    success_url = reverse_lazy('peaccess')
    template_name = 'questions/view_add_category.html'

    def form_valid(self, form):
        """ Save all the new names as new categories in the database. """
        form.save()

        # Return to success_url
        return HttpResponseRedirect(self.get_success_url())

def submit_question(request):
    # If this is a POST request then process form data
    if request.method == 'POST':
        # Grab the question from the request
        form = SubmitQuestionForm(request.POST)

        # Check if the question is actually valid
        if form.is_valid():
            # If it is, then create a new PrivateQuestion data
            new_question = Question(
                subject = form.cleaned_data['subject'],
                content = form.cleaned_data['content'],
                post_date = datetime.date.today())

            # If op choses to give us his email, record it
            if form.data['email']:
                new_question.op_email = form.cleaned_data['email']

            # Query the new question to the database
            new_question.save()

            return HttpResponseRedirect(reverse('submit-success'))

    # If this is a GET request then give out the new form
    else:
        form = SubmitQuestionForm()

    context = {'form': form, }

    return render(request, 'questions/submit_question.html', context)

def submit_question_success(request):
    # Render the success page.
    return render(request, 'questions/submit_question_success.html')
