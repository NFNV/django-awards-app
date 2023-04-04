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

def create_question(question_text, days):
    # Create a question with the given 'question text', and published the given number of days offset to now (negative for questions published in the past, positive for question that have yet to be published).
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # if no question exists, an appropiate message is displayed.
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_questions(self):
        # Question with a pub date in the future arent't displayed on the index page.
        create_question('Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        # Questions with a pub date in the past, are displayed on the index page.
        question = create_question('Past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])
        
    def test_future_question_and_past_questions(self):
        # Even if both past and future questions exist, only past questions are displayed.
        past_question = create_question(question_text='Past question', days=-30)
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )

    def test_two_past_questions(self):
        # The questions index page may display multiple questions.
        past_question1 = create_question(question_text='Past question 1', days=-30)
        past_question2 = create_question(question_text='Past question 2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        # The questions aren't displayed in the index view.
        future_question1 = create_question("Future question 1", 25)
        future_question2 = create_question("Future question 2", 15)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # The detail view of a question with a pub date in the future returns a 404 error not found.
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        # The detail view of a question with a pub date in the past desplays the question's text.
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
