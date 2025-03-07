import json
import jwt
# from jwt import InvalidSignatureError
import requests
private_key = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n"
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhvqCC+37A+UXgcvDl+7\nnbVjDI3QErdZBkI1VypVBMkKKWHMNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO\n/3+gRs/MWG27gdRNtf57uLk1+lQI6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pT\nBvirlsdX+jXrbOEaQphn0OdQo0WDoOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeM\nzlD1aDDS478PDZdckPjT96ICzqe4O1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZ\nbkhB70aTBuWDGLDR0iLenzyQecmD4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJw\nFwIDAQAB\n-----END PUBLIC KEY-----\n"

'''
This will abe a lambda edge that will   

1. Scan the incoming cookie names signed-by-pro form the content accessed by the user
2. DEcode the cookie based on the certificate 9public) and verify the signature
3. If the signature is verified, the lambda will proceed to next step otheriws ereturns 401
4. The lambda will then decode the content of the cookie to fetch pins or manuals list
5. For each pin or manual, the lambda will fetch manual by calling a gateway service that will return the manual
6. If the  manual thus refurned matched the path pattern of the content requested by the user, the lambda will allow the user to access the content
7. If the manual does not match the path pattern of the content requested by the user, the lambda will return 401
'''
def lambda_handler(event, context):
    # Extract the request from the CloudFront event
    request = event['Records'][0]['cf']['request']
    headers = request['headers']

    # Extract the signed-by-pro cookie
    if 'cookie' not in headers:
        print("No cookie found")
        return generate_response(401, 'Unauthorized')

    cookies = headers['cookie'][0]['value']
    signed_cookie = extract_validate_cookie(cookies)

    if not signed_cookie:
        print("Not a signed cookie that is required.")
        return generate_response(401, 'Unauthorized')

    # Decode and verify the 

    decoded_cookie = extract_cookie_information(signed_cookie)


    # Fetch pins or manuals list from the decoded cookie
    pins_or_manuals = decoded_cookie.get('pins_or_manuals', [])

    # Check if the requested content matches any manual
    requested_path = request['uri']
    
    for manual in pins_or_manuals:
        # Fetch the manual from the gateway service pin to manual
        graphql_query = """
        {
        publications($pin:String!)
        {
            manuals(accessories:false, translation:false)
            {
                    manuals
            }
        }
        """
        variables = {
            "pin": manual
        }
        response = requests.post(
            'https://common-content-api-devl.apps-devl-vpn.us.e06.c01.johndeerecloud.com/publications/manuals/pin',
            json={'query': graphql_query, 'variables': variables},
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            continue
        sample_json = '{"data":{"publications":{"manuals":[{"manualNo":"TM131019"},{"manualNo":"TM164619"},{"manualNo":"LVU17923"},{"manualNo":"CTM120019"},{"manualNo":"CTM120419"}]}},"message":"ok","code":200}'
        # get all manual numbers and return as a list
        manuals = json.loads(sample_json).get('data', {}).get('publications', {}).get('manuals', [])
        # manuals = response.json().get('data', {}).get('getManuals', {}).get('manuals', [])
        if not manuals:
            continue

        for manual_path in manuals:
            if manual_path in requested_path:
                 print('User is authorized to access the content, passing on the request')
                 print('Before')
                 request.headers['X-Route'] = 'PRO' 
                 print('After')
                 request
    print('User is NOT authorized to access the content')
    return generate_response(401, 'Unauthorized')

def extract_cookie_information(signed_cookie):
    ## this is a dependency on SC to provide the public key to decode cookie
    # public_key = '-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----'
    # try:
    decoded_cookie = jwt.decode(signed_cookie, public_key, algorithms=['RS256'])
    # except InvalidSignatureError:
    #     return generate_response(401, 'Unauthorized')
    return decoded_cookie

def extract_validate_cookie(cookies):
    signed_cookie = None
    for cookie in cookies.split(';'):
        if 'signed-by-pro' in cookie:
            signed_cookie = cookie.split('=')[1]
            break
    return signed_cookie

def generate_response(status_code, message):
    return {
        'status': str(status_code),
        'statusDescription': message,
        'headers': {
            'content-type': [{
                'key': 'Content-Type',
                'value': 'text/plain'
            }]
        },
        'body': message
    }