import jwt
private_key = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n"
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhvqCC+37A+UXgcvDl+7\nnbVjDI3QErdZBkI1VypVBMkKKWHMNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO\n/3+gRs/MWG27gdRNtf57uLk1+lQI6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pT\nBvirlsdX+jXrbOEaQphn0OdQo0WDoOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeM\nzlD1aDDS478PDZdckPjT96ICzqe4O1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZ\nbkhB70aTBuWDGLDR0iLenzyQecmD4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJw\nFwIDAQAB\n-----END PUBLIC KEY-----\n"

'''
This will abe a lambda edge that will   

1. Scan the incoming cookie named 'CloudFront-PSML' form the content accessed by the user.
2. Decode the cookie based on the certificate (public) or Encoded with basic algos and verify the signature. Cookie Decode
3. If the signature is verified, the lambda will proceed to next step otheriws ereturns 403 or 401
4. For each manual in the cookie compare with pub_code in url suffix, and if found allow access
5. if not found return 403
'''

def lambda_handler(event, context): 
    # Extract the request from the CloudFront event
    request = event['Records'][0]['cf']['request']
    headers = request['headers']

    # Extract the CloudFront-PSML cookie
    if 'cookie' not in headers:
        print("No cookie found")
        return generate_response(403, 'Forbidden')

    cookies = headers['cookie']['CloudFront-PSML']
    signed_cookie = validate_signature(cookies)

    if not signed_cookie:
        print("Invalid cookie. Not a signed cookie.") 
        return generate_response(403, 'Forbidden')

    # Decode and verify the cookie
    manuals = decode_decompress_manuals(signed_cookie)
    # Check if the requested content matches any manual
    requested_path = request['uri']
    requested_manual = fetch_manual(requested_path)

    if requested_manual in manuals:
        # Only place where manuals will be returned
        return request

    return generate_response(403, 'Forbidden')


'''
decompress and decode signed cookie paramter and return the value whihc are manuals
TBD: can be kept optional if this is not required
'''
def decode_decompress_manuals(cookie):
    # Decode the cookie
    decoded_cookie = jwt.decode(cookie, verify=False)
    # Fetch manuals list from the decoded cookie
    manuals = decoded_cookie.get('manuals', [])
    return manuals

'''
Validates if the cookie is signed by the provider e.g. PRO
If so returns the cookie value
'''
def validate_signature(cookie):
    # Decode the cookie
    decoded_cookie = jwt.decode(cookie, public_key, algorithms=['RS256'], verify=True)    
    return decoded_cookie


'''
Fetches a manual number based on the path 

e.g. if the path is /WebSA/Data/manuals/manualbooks/tm1874/tm1874_09001faa8004ae2a.html
the manual number is tm1874 which is before the last / and after the second last /
'''    
def fetch_manual(requested_path):
    parts = requested_path.split('/')
    return parts[-2]


def generate_response(status=403, body=None):
    return {
        'status': status,
        'body': body
    }