from django.shortcuts import render
from rest_framework_api.views import BaseAPIView, StandardAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class HelloWorldView(BaseAPIView):
    def get(self, request, format=None):
        your_condition_here = True
        if your_condition_here:
            dict = {'message':'Hello World!'}
            return self.send_response(dict,status=status.HTTP_201_CREATED)
        else:
            error_message = 'This is a custom error message. I am a String.'
            return self.send_error(error_message)


class HelloWorldViewFakeData(BaseAPIView):
    fake_data = [
        {'id': 1, 'name': 'John'},
        {'id': 2, 'name': 'Jane'},
        {'id': 3, 'name': 'Bob'},
        {'id': 4, 'name': 'Alice'},
        {'id': 5, 'name': 'Eve'},
    ]

    def get(self, request, format=None):
        return self.send_response(self.fake_data)


# class HelloWorldPaginatedView(StandardAPIView):
#     # Set the serializer class to be used in the view
#     serializer_class = APIResponseSerializer

#     def get(self, request):
#         # Create a list of data to be paginated
#         data = ['Hello', 'World', 'This', 'Is', 'A', 'Test']

#         # Call the `paginate_data` method to paginate the data
#         paginated_data = self.paginate_data(
#             data, request, context={'request': request}
#         )

#         # Return the paginated data in the APIResponseSerializer format
#         return paginated_data

class HelloWorldPaginatedView(StandardAPIView):
    def get(self, request):
        # Set the page size to 3
        self.pagination_class.page_size = 3

        # Generate some data
        data = ['Hello', 'World', 'This', 'Is', 'A', 'Paginated', 'Response']

        # Return a paginated response
        return self.paginate_data(data, request)


# class HelloWorldObjectPaginatedView(StandardAPIView):
#     def get(self, request, format=None):
#         courses = Courses.objects.all()
#         if courses:
#             return self.paginate_data(courses, request, page_size=3, max_page_size=5)
#         else:
#             return self.send_error('No data found')


class RequestInstructorView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, format=None):
        user = self.request.user 
        user.become_seller = True
        user.save()
        return self.send_response('Success', status=status.HTTP_200_OK)