import unittest
from unittest.mock import patch
from manuals_validator_lambda_edge import lambda_handler, decode_decompress_manuals, validate_signature, fetch_manual, generate_response   

class TestManualsValidatorLambdaEdge(unittest.TestCase):

    @patch('manuals_validator_lambda_edge.jwt.decode')
    def test_decode_decompress_manuals(self, mock_jwt_decode):
        mock_jwt_decode.return_value = {'manuals': ['tm1874', 'tm1875']}
        cookie = 'dummy_cookie'
        manuals = decode_decompress_manuals(cookie)
        self.assertEqual(manuals, ['tm1874', 'tm1875'])

    @patch('manuals_validator_lambda_edge.jwt.decode')
    def test_validate_signature(self, mock_jwt_decode):
        mock_jwt_decode.return_value = {'manuals': ['tm1874', 'tm1875']}
        cookie = 'dummy_cookie'
        decoded_cookie = validate_signature(cookie)
        self.assertEqual(decoded_cookie, {'manuals': ['tm1874', 'tm1875']})

    def test_fetch_manual(self):
        requested_path = '/WebSA/Data/manuals/manualbooks/tm1874/tm1874_09001faa8004ae2a.html'
        manual = fetch_manual(requested_path)
        self.assertEqual(manual, 'tm1874')

    def test_generate_response(self):
        response = generate_response(403, 'Forbidden')
        self.assertEqual(response, {'status': 403, 'body': 'Forbidden'})

    @patch('manuals_validator_lambda_edge.validate_signature')
    @patch('manuals_validator_lambda_edge.decode_decompress_manuals')
    def test_lambda_handler_valid_cookie(self, mock_decode_decompress_manuals, mock_validate_signature):
        event = {
            'Records': [{
                'cf': {
                    'request': {
                        'headers': {
                            'cookie': {
                                'CloudFront-PSML': 'dummy_cookie'
                            }
                        },
                        'uri': '/WebSA/Data/manuals/manualbooks/tm1874/tm1874_09001faa8004ae2a.html'
                    }
                }
            }]
        }
        context = {}
        mock_validate_signature.return_value = 'dummy_signed_cookie'
        mock_decode_decompress_manuals.return_value = ['tm1874', 'tm1875']

        response = lambda_handler(event, context)
        self.assertEqual(response, event['Records'][0]['cf']['request'])

    @patch('manuals_validator_lambda_edge.validate_signature')
    def test_lambda_handler_invalid_cookie(self, mock_validate_signature):
        event = {
            'Records': [{
                'cf': {
                    'request': {
                        'headers': {
                            'cookie': {
                                'CloudFront-PSML': 'dummy_cookie'
                            }
                        },
                        'uri': '/WebSA/Data/manuals/manualbooks/tm1874/tm1874_09001faa8004ae2a.html'
                    }
                }
            }]
        }
        context = {}
        mock_validate_signature.return_value = None

        response = lambda_handler(event, context)
        self.assertEqual(response, generate_response(403, 'Forbidden'))

    def test_lambda_handler_no_cookie(self):
        event = {
            'Records': [{
                'cf': {
                    'request': {
                        'headers': {}
                    }
                }
            }]
        }
        context = {}

        response = lambda_handler(event, context)
        self.assertEqual(response, generate_response(403, 'Forbidden'))

    ### TBD : replace dummy cookie with actual compressed and endocded manuals 
    # def test_decode_decompress_manuals(self):   
    #     cookie = 'CloudFront-Key-Pair-Id=K15P8UNU1GRYNN; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vbWFudWFsLWNvbnRlbnQuZGVlcmUuY29tLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NDExMTk2MTJ9fX1dfQ__; CloudFront-Signature=el-oEn9lbe19H0VeA~YypSUhXcRcVujdJ7zrW7iASRIK9WX6IQoCcfKfyAw4OEp1mNRzusUxoFYe1eMAg9vOXMLSiS8jVA4vpHJIUk6Na7dTLrRcVPGf~tGK~V5gT12EHYA54vGdrjG0DBC0AT5ffBMn9BXVGM30CpkiFWzYBeoiUjGBn7CVHMjd-FEnRgJ0PEPXi-o52~DOGLDKkXpP2nXyzlQAW0mZv-fqBN8AqhtEqHlxrMeOgwLn81Czk0CIpHLGvuMyiMb-EkvstTQmZBP~aCWP2xFs9fI5g96H-pkcypy3KcA5IVoswxMFq63jznYd6KDL9e8NlL4cqY8LlQ__; _ga=GA1.1.68462441.1739266344; s_ecid=MCMID%7C16724589531343719873287160179831727966; _hp2_props.3269992521=%7B%22Affiliate%22%3A%22OD7900%22%2C%22Affiliate%20Name%22%3A%22John%20Deere%20Innovation%22%2C%22Idea%20Box%22%3Afalse%2C%22Free%20Trial%22%3Afalse%2C%22product_type%22%3A%22Incubate%22%2C%22Campaign%20Name%22%3A%22Advanced%20IT%20PSC%20Incubator%22%7D; _hp2_id.3269992521=%7B%22userId%22%3A%223536261884865808%22%2C%22pageviewId%22%3A%224246691570476466%22%2C%22sessionId%22%3A%226463320064539084%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _gcl_au=1.1.542792000.1739962225; _fbp=fb.1.1740133811162.496715553451180370; AMCVS_8CC867C25245ADC30A490D4C%40AdobeOrg=1; s_cc=true; SL_C_23361dd035530_SID={"9190c5627164895eb3c32217d9aea2f15cceda0e":{"sessionId":"YOmZ04_hAJyfZXNWs2NWN","visitorId":"rNvElTNVNP8oGpCX5lR7P"}}; SMSESSION=""; incap_ses_704_3104473=qYo1IS0RqUJ5CZG7cxzFCaIxwGcAAAAA0f+XDs+JgUjl2/gdCEZH5Q==; AMCV_8CC867C25245ADC30A490D4C%40AdobeOrg=179643557%7CMCIDTS%7C20147%7CMCMID%7C16724589531343719873287160179831727966%7CMCAAMLH-1741253666%7C12%7CMCAAMB-1741253666%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1740656066s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; s_ppvl=en_us%2520%253A%2520jdt%2520%253A%2520home%2C100%2C81%2C1190%2C1920%2C963%2C1536%2C864%2C1.25%2CP; visid_incap_3104473=k1xBLGx7SQe3FHIs9sWKgiAZq2cAAAAAQkIPAAAAAABBT7ILxRVG248f2xXNC9UR; _ga_2N0KHYJXNT=GS1.1.1740648866.4.1.1740648882.0.0.0; at_check=true; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Feb+28+2025+11%3A16%3A22+GMT%2B0530+(India+Standard+Time)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1d2870d4-ede2-48fe-add7-a577e5687e00&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false; s_ips=759; s_tp=3646; s_ppv=en_us%2520%253A%2520our-company%2520%253A%2520contact-us%2520%253A%2520locations%2C95%2C21%2C3467%2C2%2C4; s_sq=deerersddc%3D%2526c.%2526a.%2526activitymap.%2526page%253Den_us%252520%25253A%252520our-company%252520%25253A%252520contact-us%252520%25253A%252520locations%2526link%253DView%252520Locations%252520Map%2526region%253DMainContentSection%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Den_us%252520%25253A%252520our-company%252520%25253A%252520contact-us%252520%25253A%252520locations%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.deere.com%25252Fassets%25252Fpdfs%25252Fcommon%25252Four-company%25252Fabout%25252Fjd-world-locations.pdf%2526ot%253DA; MYSAPSSO2=AjQxMDMBABhRAEsARwA1AFIARABLACAAIAAgACAAIAACAAY0ADEAMAADABBQAEcAMQAgACAAIAAgACAABAAYMgAwADIANQAwADIAMgA4ADAAOAAxADkABQAEAAAACAkAAkUA%2fwFVMIIBUQYJKoZIhvcNAQcCoIIBQjCCAT4CAQExCzAJBgUrDgMCGgUAMAsGCSqGSIb3DQEHATGCAR0wggEZAgEBMG8wZDELMAkGA1UEBhMCVVMxHDAaBgNVBAoTE1NBUCBUcnVzdCBDb21tdW5pdHkxEzARBgNVBAsTClNBUCBXZWIgQVMxFDASBgNVBAsTC0kwMDIwNzYyMDM2MQwwCgYDVQQDEwNQRzECByAUAiYXRScwCQYFKw4DAhoFAKBdMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTI1MDIyODA4MTk0NVowIwYJKoZIhvcNAQkEMRYEFH4dBNltGvgnqP7wZvA%2foZJkmjaCMAkGByqGSM44BAMELjAsAhRklF3GeDznzM5GT2VTkQz7cgrDcAIUB%213flEeKyMPu9arsUGSLEs7AOxw%3d; fs_uid=#o-1E4TAT-na1#0aab7890-9e1f-490d-9edd-3e67ab07169a:4f9a4d8b-5993-4a7c-bc4a-cf1de0e076fa:1741004761300::2#6b9fe3cc#/1770387363; kndctr_8CC867C25245ADC30A490D4C_AdobeOrg_identity=CiYxNjcyNDU4OTUzMTM0MzcxOTg3MzI4NzE2MDE3OTgzMTcyNzk2NlIRCNz%5F0e7RMhgBKgRJTkQxMAPwAfL%2DnOTVMg%3D%3D; us-uc-cart-id-cert=3b988155-057f-40f2-8c19-8dc052c6bd28'
    #     manuals = decode_decompress_manuals(cookie)
    #     self.assertEqual(manuals, [])

    ### TBD : replace dummy cookie with actual cookie
    # def test_validate_signature(self):
    #     cookie = 'CloudFront-Key-Pair-Id=K15P8UNU1GRYNN; CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vbWFudWFsLWNvbnRlbnQuZGVlcmUuY29tLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NDExMTk2MTJ9fX1dfQ__; CloudFront-Signature=el-oEn9lbe19H0VeA~YypSUhXcRcVujdJ7zrW7iASRIK9WX6IQoCcfKfyAw4OEp1mNRzusUxoFYe1eMAg9vOXMLSiS8jVA4vpHJIUk6Na7dTLrRcVPGf~tGK~V5gT12EHYA54vGdrjG0DBC0AT5ffBMn9BXVGM30CpkiFWzYBeoiUjGBn7CVHMjd-FEnRgJ0PEPXi-o52~DOGLDKkXpP2nXyzlQAW0mZv-fqBN8AqhtEqHlxrMeOgwLn81Czk0CIpHLGvuMyiMb-EkvstTQmZBP~aCWP2xFs9fI5g96H-pkcypy3KcA5IVoswxMFq63jznYd6KDL9e8NlL4cqY8LlQ__; _ga=GA1.1.68462441.1739266344; s_ecid=MCMID%7C16724589531343719873287160179831727966; _hp2_props.3269992521=%7B%22Affiliate%22%3A%22OD7900%22%2C%22Affiliate%20Name%22%3A%22John%20Deere%20Innovation%22%2C%22Idea%20Box%22%3Afalse%2C%22Free%20Trial%22%3Afalse%2C%22product_type%22%3A%22Incubate%22%2C%22Campaign%20Name%22%3A%22Advanced%20IT%20PSC%20Incubator%22%7D; _hp2_id.3269992521=%7B%22userId%22%3A%223536261884865808%22%2C%22pageviewId%22%3A%224246691570476466%22%2C%22sessionId%22%3A%226463320064539084%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _gcl_au=1.1.542792000.1739962225; _fbp=fb.1.1740133811162.496715553451180370; AMCVS_8CC867C25245ADC30A490D4C%40AdobeOrg=1; s_cc=true; SL_C_23361dd035530_SID={"9190c5627164895eb3c32217d9aea2f15cceda0e":{"sessionId":"YOmZ04_hAJyfZXNWs2NWN","visitorId":"rNvElTNVNP8oGpCX5lR7P"}}; SMSESSION=""; incap_ses_704_3104473=qYo1IS0RqUJ5CZG7cxzFCaIxwGcAAAAA0f+XDs+JgUjl2/gdCEZH5Q==; AMCV_8CC867C25245ADC30A490D4C%40AdobeOrg=179643557%7CMCIDTS%7C20147%7CMCMID%7C16724589531343719873287160179831727966%7CMCAAMLH-1741253666%7C12%7CMCAAMB-1741253666%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1740656066s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; s_ppvl=en_us%2520%253A%2520jdt%2520%253A%2520home%2C100%2C81%2C1190%2C1920%2C963%2C1536%2C864%2C1.25%2CP; visid_incap_3104473=k1xBLGx7SQe3FHIs9sWKgiAZq2cAAAAAQkIPAAAAAABBT7ILxRVG248f2xXNC9UR; _ga_2N0KHYJXNT=GS1.1.1740648866.4.1.1740648882.0.0.0; at_check=true; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Feb+28+2025+11%3A16%3A22+GMT%2B0530+(India+Standard+Time)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1d2870d4-ede2-48fe-add7-a577e5687e00&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false; s_ips=759; s_tp=3646; s_ppv=en_us%2520%253A%2520our-company%2520%253A%2520contact-us%2520%253A%2520locations%2C95%2C21%2C3467%2C2%2C4; s_sq=deerersddc%3D%2526c.%2526a.%2526activitymap.%2526page%253Den_us%252520%25253A%252520our-company%252520%25253A%252520contact-us%252520%25253A%252520locations%2526link%253DView%252520Locations%252520Map%2526region%253DMainContentSection%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Den_us%252520%25253A%252520our-company%252520%25253A%252520contact-us%252520%25253A%252520locations%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.deere.com%25252Fassets%25252Fpdfs%25252Fcommon%25252Four-company%25252Fabout%25252Fjd-world-locations.pdf%2526ot%253DA; MYSAPSSO2=AjQxMDMBABhRAEsARwA1AFIARABLACAAIAAgACAAIAACAAY0ADEAMAADABBQAEcAMQAgACAAIAAgACAABAAYMgAwADIANQAwADIAMgA4ADAAOAAxADkABQAEAAAACAkAAkUA%2fwFVMIIBUQYJKoZIhvcNAQcCoIIBQjCCAT4CAQExCzAJBgUrDgMCGgUAMAsGCSqGSIb3DQEHATGCAR0wggEZAgEBMG8wZDELMAkGA1UEBhMCVVMxHDAaBgNVBAoTE1NBUCBUcnVzdCBDb21tdW5pdHkxEzARBgNVBAsTClNBUCBXZWIgQVMxFDASBgNVBAsTC0kwMDIwNzYyMDM2MQwwCgYDVQQDEwNQRzECByAUAiYXRScwCQYFKw4DAhoFAKBdMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTI1MDIyODA4MTk0NVowIwYJKoZIhvcNAQkEMRYEFH4dBNltGvgnqP7wZvA%2foZJkmjaCMAkGByqGSM44BAMELjAsAhRklF3GeDznzM5GT2VTkQz7cgrDcAIUB%213flEeKyMPu9arsUGSLEs7AOxw%3d; fs_uid=#o-1E4TAT-na1#0aab7890-9e1f-490d-9edd-3e67ab07169a:4f9a4d8b-5993-4a7c-bc4a-cf1de0e076fa:1741004761300::2#6b9fe3cc#/1770387363; kndctr_8CC867C25245ADC30A490D4C_AdobeOrg_identity=CiYxNjcyNDU4OTUzMTM0MzcxOTg3MzI4NzE2MDE3OTgzMTcyNzk2NlIRCNz%5F0e7RMhgBKgRJTkQxMAPwAfL%2DnOTVMg%3D%3D; us-uc-cart-id-cert=3b988155-057f-40f2-8c19-8dc052c6bd28'
    #     decoded_cookie = validate_signature(cookie)
    #     self.assertEqual(decoded_cookie, None)

if __name__ == '__main__':
    unittest.main()