# from django.utils.deprecation import MiddlewareMixin
#
#
# class SameSiteMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         if 'sessionid' in response.cookies:
#                 response.cookies['sessionid']['samesite'] = 'Secure'
#         if 'csrftoken' in response.cookies:
#                 response.cookies['csrftoken']['samesite'] = 'Secure'
#         return response