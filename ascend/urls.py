from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('sign-up', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('about', views.about, name="about"),
    path('courses', views.courses, name="courses"),
    path('course/using-ai-in-teaching', views.ai_course, name="ai_course"),
    path('resources', views.resources, name="resources"),
    path('tools', views.tools, name="tools"),
    path('tool/assessment-generator', views.assessment, name="assessment"),
    path('tool/lesson-planner', views.planner, name="planner"),
    path('tool/ascendchat', views.ascendchat, name="ascendchat"),
    path('tool/pedagogy-guide', views.pedagogy, name="pedagogy"),


    # API Routes
    path('api/ascendchat/<str:message>', views.ascend_chat),
    path('api/assessment', views.assessment_api),
    path('api/planner', views.planner_api),
    path('api/pedagogy-guide', views.pedagogy_api),
]
