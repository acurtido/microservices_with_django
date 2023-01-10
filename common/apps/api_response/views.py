from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import APIResponseSerializer
from .pagination import CustomPagination


class BaseAPIView(APIView):
    def send_response(self, data=None, status=status.HTTP_200_OK):
        serializer = APIResponseSerializer({
            'success': True,
            'status': status,
            'data': data
        })
        return Response(serializer.data, status=status)

    def send_error(self, error, status=status.HTTP_400_BAD_REQUEST):
        serializer = APIResponseSerializer({
            'success': False,
            'status': status,
            'error': error
        })
        return Response(serializer.data, status=status)


class StandardAPIView(BaseAPIView):
    def send_response(self, data=None, status=status.HTTP_200_OK):
        serializer = APIResponseSerializer({
            'success': True,
            'status': status,
            'data': data
        })
        return Response(serializer.data, status=status)

    def send_error(self, error, status=status.HTTP_400_BAD_REQUEST):
        serializer = APIResponseSerializer({
            'success': False,
            'status': status,
            'error': error
        })
        return Response(serializer.data, status=status)

    def paginate_response(self, request, data):
        try:
            paginator = CustomPagination()
            paginated_data = paginator.paginate_data(data, request)
            serializer = APIResponseSerializer({
                'success': True,
                'status': status.HTTP_200_OK,
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'data': paginated_data
            })
            return Response(serializer.data)
        except Exception as e:
            serializer = APIResponseSerializer({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            })
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# ============= Demo Views ============= #

class HelloWorldView(BaseAPIView):
    def get(self, request, format=None):
        your_condition_here = True
        if your_condition_here:
            dict = {'message':'Hello World!'}
            list = ['This','is','a','List']
            string = 'Tis a string'
            number = 1
            float = 0.4
            object = {'I contain data'}
            return self.send_response(dict,status=status.HTTP_201_CREATED)
        else:
            error_message = 'This is a custom error message. I am a String.'
            return self.send_error(error_message)


class HelloWorldPaginatedView(StandardAPIView):
    def get(self, request):
        data = [
                {'id': 1, 'content': 'Hello'},
                {'id': 2, 'content': 'World'},
                {'id': 3, 'content': 'This'},
                {'id': 4, 'content': 'Is'},
                {'id': 5, 'content': 'A'},
                {'id': 6, 'content': 'Paginated'},
                {'id': 7, 'content': 'Response'},
            ]
        return self.paginate_response(request, data)


# class HelloWorldObjectPaginatedView(StandardAPIView):
#     def get(self, request, format=None):
#         courses = Courses.objects.all()
#         if courses:
#             return self.paginate_response(request, courses)
#         else:
#             return self.send_error('No data found')