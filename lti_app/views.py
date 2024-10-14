# lti_app/views.py

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.contrib.django import DjangoMessageLaunch, DjangoOIDCLogin
from django.views.decorators.csrf import csrf_exempt
import logging
import os

logger = logging.getLogger(__name__)

# Define the absolute path to tool_config.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL_CONFIG_PATH = os.path.join(BASE_DIR, 'tool_config.json')


@csrf_exempt
def lti_login(request):
    try:
        redirect_uri = request.build_absolute_uri('/lti/launch/')
        logger.info(f"Redirect URI: {redirect_uri}")
        tool_config = ToolConfJsonFile(TOOL_CONFIG_PATH)
        oidc_login = DjangoOIDCLogin(request, tool_config)
        return oidc_login \
            .enable_check_cookies() \
            .redirect(redirect_uri)
    except Exception as e:
        logger.error(f"Error during OIDC login: {e}")
        return HttpResponse("An error occurred during OIDC login.", status=500)


@csrf_exempt
def lti_launch(request):
    try:
        logger.debug(f"Launch POST data: {request.POST}")
        tool_config = ToolConfJsonFile(TOOL_CONFIG_PATH)
        message_launch = DjangoMessageLaunch(request, tool_config)
        launch_data = message_launch.get_launch_data()
        
        # Extract user information
        user_info = {
            'name': launch_data.get('name', 'Unknown User'),
            'given_name': launch_data.get('given_name', ''),
            'family_name': launch_data.get('family_name', ''),
            'email': launch_data.get('email', ''),
            'user_id': launch_data.get('sub', ''),
            'roles': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/roles', []),
            'course_title': launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', {}).get('title', 'Unknown Course'),
        }
        
        # Log the successful launch
        logger.info(f"LTI Launch successful for user: {user_info['user_id']}")
        
        # Render the template with user information
        return render(request, 'lti_app/launch_success.html', {'user_info': user_info})
    
    except Exception as e:
        logger.error(f"Error during LTI Launch: {e}")
        return HttpResponse(f"An error occurred during LTI Launch. {e}", status=500)


@csrf_exempt
def jwks(request):
    try:
        tool_config = ToolConfJsonFile(TOOL_CONFIG_PATH)  # Use absolute path
        jwks_data = tool_config.get_jwks()
        return JsonResponse(jwks_data)
    except Exception as e:
        logger.error(f"Error fetching JWKS: {e}")
        return HttpResponse("An error occurred while fetching JWKS.", status=500)
