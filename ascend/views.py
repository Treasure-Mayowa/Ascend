from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
import json
import requests


MESSAGE = []

ASSISTANT = []

# Create your views here.
def index(request):
    return render(request, 'ascend/index.html')

def about(request):
    return render(request, 'ascend/about.html')

def courses(request):
    return render(request, "ascend/courses.html")

def tools(request):
    return render(request, "ascend/tools.html")

def resources(request):    
    return render(request, "ascend/resources.html", {
        "videos": YoutubeContent.objects.all()
    })

@login_required
def ai_course(request):
    return render(request, "ascend/aicourse.html")  

@login_required
def ascendchat(request):
    return render(request, "ascend/ascendchat.html")

@login_required
def planner(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "ascend/planner.html")

@login_required
def assessment(request):
    return render(request, 'ascend/assessment.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "ascend/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ascend/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if request.POST["school"]:
            school = request.POST["school"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "ascend/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if school:
                user.school = school
            user.save()
        except IntegrityError:
            return render(request, "ascend/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "ascend/register.html")

# API Routes
@login_required
def ascend_chat(request, message):
    global MESSAGE, ASSISTANT

    api_key = settings.API_KEY

    stream = False

    url = "https://chat.nbox.ai/api/chat/completions"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    if len(MESSAGE) > 20 and len(ASSISTANT) > 20:
        MESSAGE = []
        ASSISTANT = []

    MESSAGE.append({
                    "role": "user",
                    "content": f"Respond to this message and do not put any preface text in your response. If the message is not related to teachers or teaching, simply respond with, 'Invalid question. I am designed to assist teachers only': {message}"
                })
    data = {
        "temperature": 0.7,
        "messages": [
             {
                "role": "system",
                 "content": "You are Ascend Chat, a chatbot designed to assist Nigerian teachers. You are from a web application called Ascend that has courses, teacher upskilling resources and tools all designed to help teachers improve and improve learning outcomes."
            }
            ] + MESSAGE + ASSISTANT + [
                {
                    "role": "user",
                    "content": f"Respond to this message and do not put any preface text in your response: {message}"
                }
            ],
            "model": "llama-2-chat-70b-4k",
            "stream": stream,
            "max_tokens": 1000
        }
    response = requests.post(url, headers=headers, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return JsonResponse({ "result": result })
    else:
        result = response.json()['choices'][0]['message']['content']
        ASSISTANT.append({
                    "role": "assistant",
                    "content": result
                })
        return JsonResponse({ "result": result })


@login_required
def assessment_api(request):
    api_key = settings.API_KEY

    stream = False

    content = request.GET.get('content', '')
    number = request.GET.get('number', '')


    url = "https://chat.nbox.ai/api/chat/completions"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0.6,
       "messages": [
        {
           "role": "system",
                    "content": "You are an Ascend assessment AI designed to generate assessment questions from topics or notes"
        },
        {
            "role": "user",
            "content": f"Using these topics or notes, generate {number} good assessment questions. Format your response well and do not put an preface text in your response, just the assessment questions: {content}"
        }
        ],
        "model": "llama-2-chat-70b-4k",
        "stream": stream,
        "max_tokens": 1000
        }
    response = requests.post(url, headers=headers, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return JsonResponse({ "result": result })
    else:
        result = response.json()['choices'][0]['message']['content']
        return JsonResponse({ "result": result })

@login_required
def planner_api(request):
    api_key = settings.API_KEY

    stream = False

    subject = request.GET.get('subject', '')
    topic = request.GET.get('topic', '')
    sub = request.GET.get('sub', '')
    duration = request.GET.get('duration', '')

    url = "https://chat.nbox.ai/api/chat/completions"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0.7,
        "messages": [
        {
           "role": "system",
                    "content": "You are an Ascend lesson planner AI designed to generate lesson plans for Nigerian teachers"
        },
        {
            "role": "user",
            "content": f"Generate a lesson plan following the Nigerian curriculum with the the topic, {topic}, sub-topic, {sub}, lesson duration of {duration} minutes under the subject, {subject}. If there is an invalid topic, sub-topic, or subject, just respond 'Invalid input. Try again.' Format your response well and DO NOT put any preface text in your response, just the lesson plan. Also, put 'Key Point' outline in the lessons plan to highlight key points in the subtopic alongside other default outlines."
        }
        ],
        "model": "llama-2-chat-70b-4k",
        "stream": stream,
        "max_tokens": 1000
        }
    response = requests.post(url, headers=headers, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    result = json.loads(l)
                    return JsonResponse({ "result": result })
    else:
        result = response.json()['choices'][0]['message']['content']
        return JsonResponse({ "result": result })