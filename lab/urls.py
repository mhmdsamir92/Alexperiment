from lab import views
from django.conf.urls import url

urlpatterns = [
    url(r'^start_alexperiment\/?', views.start_alexperiment),
    url(r'^run_results\/?', views.get_run_results)
]
