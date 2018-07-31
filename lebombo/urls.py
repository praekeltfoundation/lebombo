from django.urls import path

from .views import InvestigationView

"""
urlpatterns = [
    path(r"^investigation/(?P<investigation_slug>\w+)/$", InvestigationView.as_view()),
]
"""

urlpatterns = [
    path(
        "investigation/<int:investigation_slug>/",
        InvestigationView.as_view(),
        name="investigation",
    )
]
