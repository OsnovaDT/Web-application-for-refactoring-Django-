"""Business logic used in views"""

from ast import parse

from django.contrib.auth import get_user_model
from django.http import JsonResponse, FileResponse

from refactoring.services.code_parser import CodeParser
from refactoring.services.rules_checker import CleanCodeRulesChecker
from refactoring.models import RefactoringRecommendation
from refactoring.services.utils import (
    get_code_error, get_code_to_display_in_html,
)
from refactoring.services.files_download import (
    get_response_with_file, get_xml_file_content,
)


User = get_user_model()


def get_recommendations_or_error_response(code: str) -> JsonResponse:
    """Return response with recommendations or with error"""

    code_error = get_code_error(code)

    if code_error != '':
        results = {'error': code_error}
    else:
        results = {'recommendations': _get_code_recommendations(code)}

    return JsonResponse(results)


def create_refactoring_recommendation(recommendation_data: dict) -> None:
    """Create refactoring recommendation"""

    if isinstance(recommendation_data, dict):
        code = recommendation_data.get('code')
        username = recommendation_data.get('username')
        recommendations = recommendation_data.get('recommendations')

        if username and code and recommendations:
            RefactoringRecommendation.objects.create(
                user=User.objects.get(username=username),
                code=get_code_to_display_in_html(code),
                recommendation=recommendations,
            )


def get_file_response_with_refactoring_recommendations(
        recommendations: str, extension: str) -> FileResponse | JsonResponse:
    """Return file response with refactoring recommendations"""

    if extension == 'xml':
        recommendations = get_xml_file_content(recommendations)

    return get_response_with_file(
        recommendations, f'refactoring_recommendations.{extension}',
    )


def _get_code_recommendations(code: str) -> dict:
    """Return refactoring recommendations for user's code"""

    code_recommendations = {}

    if isinstance(code, str):
        parser = CodeParser()
        parser.visit(parse(code))

        recommendations = CleanCodeRulesChecker(
            parser.code_items
        ).recommendations

        code_recommendations = {
            rule: ", ".join(wrong_code_items)
            for rule, wrong_code_items in recommendations.items()
        }

    return code_recommendations
