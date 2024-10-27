from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import json
import requests
from .api import api_pedagogy, api_planner, api_assessment

MESSAGE = []

ASSISTANT = []

# Create your views here.
def index(request):
    return render(request, 'ascend/index.html')

def about(request):
    return render(request, 'ascend/about.html')

def courses(request):
    courses = Courses.objects.all()
    return render(request, "ascend/courses.html", {
        "courses": courses })

def tools(request):
    return render(request, "ascend/tools.html")

def pedagogy(request):
    return render(request, "ascend/pedagogyguide.html")

def feedback(request):
    return render(request, "ascend/feedback.html")

def resources(request):
    search_term = request.GET.get('search', '')
    category = request.GET.get('category', '')
    

    if search_term:
        videos = YoutubeContent.objects.filter(title__icontains=search_term)
        resources = Resources.objects.filter(name__icontains=search_term)
    
    elif category:
        videos = YoutubeContent.objects.filter(category=category)
        resources = ''

    else: 
        videos =  YoutubeContent.objects.all()
        resources = Resources.objects.all()

    return render(request, "ascend/resources.html", {
        "search": search_term,
        "videos": videos,
        "resources": resources
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

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    if len(MESSAGE) > 20 and len(ASSISTANT) > 20:
        MESSAGE = []
        ASSISTANT = []

    MESSAGE.append({
                    "role": "user",
                    "content": f"Respond to this message and do not put any preface text in your response. If the message is not related to teachers or teaching, simply respond with, 'Invalid question. I am designed to assist teachers only': {message}"
                })
    data = {
        "temperature": 1.7,
        "messages": [
            {
                "role": "system",
                "content": "You are Ascend Chat, a chatbot designed to assist Nigerian teachers. You are from a web application called Ascend that has courses, teacher upskilling resources and tools all designed to help teachers improve and improve learning outcomes."
            }
            ] + MESSAGE + ASSISTANT + [
                {
                    "role": "user",
                    "content": f"Respond to this message and do not put any preface text in your response and simplify for easy comprehension: {message}"
                }
            ],
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "stream": stream
        }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
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

    content = request.GET.get('content', '')
    number = request.GET.get('number', '')

    result = api_assessment(content, number)
    return JsonResponse({ "result": result })

@login_required
def planner_api(request):

    subject = request.GET.get('subject', '')
    topic = request.GET.get('topic', '')
    sub = request.GET.get('sub', '')
    duration = request.GET.get('duration', '')

    result = api_planner(subject, topic, sub,duration)
    return JsonResponse({ "result": result })


@login_required
def pedagogy_api(request):

    subject = request.GET.get('subject', '')
    topic = request.GET.get('topic', '')
    subject_class = request.GET.get('class', '')
    pedagogy = request.GET.get('pedagogy', '')

    result = api_pedagogy(pedagogy, subject, topic, subject_class)
    return JsonResponse({ "result": result })