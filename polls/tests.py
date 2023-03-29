import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        # was_punlished_recently returns False for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='Which is the best screenplay?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        # was_published_recently() must return Flase for questions whose pub_date is more than 1 day in the past
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text='Which is the best screenplay?',pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        # was_published_recently() must return True for questions whose pub_date is actual
        time = timezone.now()
        present_question = Question(question_text='Which is the best screenplay?',pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # if no question exists, an appropiate message is displayed
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])