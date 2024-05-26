from flask import request, jsonify

class RequestVerificationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with self.app.app_context():
            try:
                if request.endpoint and request.endpoint.startswith('api_v1.') and request.method in ['POST', 'PUT']:
                    verification_header = request.headers.get('X-Request-Verification')
                    if verification_header != 'your_verification_value':
                        response = jsonify({'message': 'Unauthorized access'})
                        response.status_code = 401
                        return response(environ, start_response)
            except RuntimeError:
                pass  # Ignore the error when working outside of request context

            # If request object is not available or middleware conditions are not met,
            # simply pass the request through to the next middleware or the Flask application itself.
            return self.app(environ, start_response)
