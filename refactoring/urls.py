"""Urls of refactoring app"""

from django.urls import path

from refactoring.views import (
    CodeInputView, IndexView, RulesView, refactor_code_view,
    RefactoringRecommendationListView, download_recommendations_view,
    save_recommendation_view,
)


app_name = 'refactoring'

urlpatterns = [
    # Index page
    path(
        '',
        IndexView.as_view(),
        name='index',
    ),

    # Code input

    path(
        'code_input/',
        CodeInputView.as_view(),
        name='code_input',
    ),

    # Saved recommendations

    path(
        'saved_recommendations/',
        RefactoringRecommendationListView.as_view(),
        name='saved_recommendations',
    ),

    # Rules

    path(
        'rules/',
        RulesView.as_view(),
        name='rules',
    ),

    # Code refactoring

    path(
        'code_refactoring/',
        refactor_code_view,
        name='code_refactoring',
    ),

    # Recommendations downloading

    path(
        'download/<str:extention>/',
        download_recommendations_view,
        name='download',
    ),

    # Recommendations saving

    path(
        'save_recommendation/',
        save_recommendation_view,
        name='save_recommendation',
    ),
]
