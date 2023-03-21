from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse(f'You are on the main page')

def detail(request, question_id):
    return HttpResponse(f'You are reading question {question_id}')

def results(request, question_id):
    return HttpResponse(f'You are reading the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting to the question {question_id}')