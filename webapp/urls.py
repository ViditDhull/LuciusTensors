from django.urls import path


from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("upcoming", views.upcoming, name="upcoming"),
    path("sql_query_generator", views.sql_query_generator, name="sql_query_generator"),
    path("code_optimizer", views.code_optimizer, name="code_optimizer"),
    path("query_pdf", views.query_pdf, name="query_pdf")
]