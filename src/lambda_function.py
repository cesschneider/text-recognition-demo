import json
from typing import Dict, Any
import logging
from urllib.parse import urlparse

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def validate_image_url(url: str) -> bool:
    """
    Validate if the URL has a valid image extension
    """
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    parsed_url = urlparse(url)
    return parsed_url.path.lower().endswith(valid_extensions)

def validate_content_type(headers: Dict[str, str]) -> bool:
    """
    Validate if the Content-Type header indicates an image
    """
    content_type = headers.get('content-type', headers.get('Content-Type', '')).lower()
    return content_type.startswith('image/')

def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a formatted API Gateway response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Enable CORS
        },
        'body': json.dumps(body)
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function
    """
    logger.info('Received event: %s', json.dumps(event))

    try:
        # Get headers and body
        headers = event.get('headers', {})
        if not headers:
            return create_response(400, {'error': 'Missing headers'})

        # Parse body
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return create_response(400, {'error': 'Invalid JSON in request body'})

        # Validate Content-Type header
        if not validate_content_type(headers):
            return create_response(400, {
                'error': 'Invalid Content-Type. Must be an image type.'
            })

        # Validate presence of imageUrl
        image_url = body.get('imageUrl')
        if not image_url:
            return create_response(400, {
                'error': 'Missing imageUrl in request body'
            })

        # Validate image URL format
        if not validate_image_url(image_url):
            return create_response(400, {
                'error': 'Invalid image URL. URL must end with a valid image extension.'
            })

        # All validations passed
        return create_response(200, {
            'message': 'Valid image request',
            'imageUrl': image_url
        })

    except Exception as e:
        logger.error('Error processing request: %s', str(e))
        return create_response(500, {
            'error': 'Internal server error',
            'details': str(e)
        })