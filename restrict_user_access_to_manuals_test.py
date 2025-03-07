import unittest
from restrict_user_access_to_manuals import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler(self):
        event = {
            "Records": [
                {
                    "cf": {
                        "config": {
                            "distributionId": "EXAMPLE"
                        },
                        "request": {
                            "clientIp": "203.0.113.178",
                            "method": "GET",
                            "uri": "/WebSA/Data/manuals/manualbooks/tm1874/tm1874_09001faa8004ae2a.html",
                            "querystring": "",
                            "headers": {
                                "host": [
                                    {
                                        "key": "Host",
                                        "value": "manual-content.deere.com"
                                    }
                                ],
                                "cookie": [
                                    {
                                        "key": "Cookie",
                                        "value": "signed-by-pro=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }

        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['status'], 401)
        self.assertEqual(response['body'], 'Unauthorized')

if __name__ == '__main__':
    unittest.main()