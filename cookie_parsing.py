import http.cookies
import base64
import json
import jwt
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhvqCC+37A+UXgcvDl+7\nnbVjDI3QErdZBkI1VypVBMkKKWHMNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO\n/3+gRs/MWG27gdRNtf57uLk1+lQI6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pT\nBvirlsdX+jXrbOEaQphn0OdQo0WDoOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeM\nzlD1aDDS478PDZdckPjT96ICzqe4O1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZ\nbkhB70aTBuWDGLDR0iLenzyQecmD4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJw\nFwIDAQAB\n-----END PUBLIC KEY-----\n"
private_key = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n"

# Manusls in scope are 		TM155719 ,OMPFP23164,TM114519,OMT356886X19,CTM10120X019,PDIM10092X19
json_data = {
    "manuals": ["TM155719", "OMPFP23164", "TM114519", "OMT356886X19", "CTM10120X019", "PDIM10092X19"]
}
encoded = jwt.encode(json_data, private_key, algorithm="RS256")
print(f"encoded:{encoded}")
def parse_cookie_header(cookie_header):
    # Parse the cookie header
    cookie = http.cookies.SimpleCookie()
    cookie.load(cookie_header)

    # Extract relevant cookies
    cloudfront_key_pair_id = cookie.get('CloudFront-Key-Pair-Id').value
    cloudfront_policy = cookie.get('CloudFront-Policy').value
    cloudfront_signature = cookie.get('CloudFront-Signature').value

    # Decode the CloudFront-Policy
    decoded_policy = base64.b64decode(cloudfront_policy + "==").decode('utf-8')
    policy_dict = json.loads(decoded_policy)
    print(f"policy_dict:{json.dumps(policy_dict, indent=4)}")
    # Create a dictionary of decoded information
    decoded_info = {
        'CloudFront-Key-Pair-Id': cloudfront_key_pair_id,
        'CloudFront-Policy': policy_dict,
        'CloudFront-Signature': cloudfront_signature
    }
    print(f"decoded_info:{json.dumps(decoded_info,indent=4)}")
    decoded_cookie = jwt.decode(cloudfront_signature, public_key, algorithms=['RS256'], verify=True) 
    print(f"decoded_cookie:{json.dumps(decoded_cookie,indent=4)}")
    return decoded_cookie

# Example usage
cookie_header = f'CloudFront-Key-Pair-Id=K15P8UNU1GRYNN; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vbWFudWFsLWNvbnRlbnQuZGVlcmUuY29tLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NDExMTk2MTJ9fX1dfQ__; CloudFront-Signature={encoded}'
##el-oEn9lbe19H0VeA~YypSUhXcRcVujdJ7zrW7iASRIK9WX6IQoCcfKfyAw4OEp1mNRzusUxoFYe1eMAg9vOXMLSiS8jVA4vpHJIUk6Na7dTLrRcVPGf~tGK~V5gT12EHYA54vGdrjG0DBC0AT5ffBMn9BXVGM30CpkiFWzYBeoiUjGBn7CVHMjd-FEnRgJ0PEPXi-o52~DOGLDKkXpP2nXyzlQAW0mZv-fqBN8AqhtEqHlxrMeOgwLn81Czk0CIpHLGvuMyiMb-EkvstTQmZBP~aCWP2xFs9fI5g96H-pkcypy3KcA5IVoswxMFq63jznYd6KDL9e8NlL4cqY8LlQ__
decoded_info = parse_cookie_header(cookie_header)
print(f"decoded_manuals:{decoded_info}")
print(f"original_manuals:{json.dumps(json_data, indent=4)}")



