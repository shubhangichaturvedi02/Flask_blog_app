from functools import wraps
from flask import request, jsonify

def request_verification_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print("dsss", request.endpoint)
            # Check if request endpoint matches the criteria
            if request.endpoint and request.method in ['POST', 'PUT']:
                verification_header = request.headers.get('X-Request-Verification')
                print("verification_header", verification_header)
                if verification_header != 'request_from_app':
                    response = jsonify({'message': 'Unauthorized access'})
                    response.status_code = 401
                    return response
        except RuntimeError as e:
            print("Error", e)
            pass  # Ignore the error when working outside of request context

        # If conditions are not met, proceed with the original function
        return func(*args, **kwargs)


    return wrapper
