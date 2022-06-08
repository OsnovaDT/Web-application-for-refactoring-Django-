"""Urls of refactoring app"""

from django.urls import path

from refactoring.views import (
    ManualCodeInputView, IndexView, refactor_code_handler,
    RefactoringResultsView, InstructionView, RulesView,
    download_results_in_json, download_results_in_pdf,
)


app_name = 'refactoring'

urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='index',
    ),

    path(
        'manual_input/',
        ManualCodeInputView.as_view(),
        name='manual_input',
    ),

    path(
        'refactor/',
        refactor_code_handler,
        name='refactor',
    ),

    path(
        'results/',
        RefactoringResultsView.as_view(),
        name='results',
    ),

    path(
        'instruction/',
        InstructionView.as_view(),
        name='instruction',
    ),

    path(
        'rules/',
        RulesView.as_view(),
        name='rules',
    ),

    path(
        'json_download/',
        download_results_in_json,
        name='json_download',
    ),

    path(
        'pdf_download/',
        download_results_in_pdf,
        name='pdf_download',
    ),
]
