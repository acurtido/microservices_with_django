Django Rest Framework API Response
===================================

**Getting Started**
********************

To use the DjangoRestFramework API Response package, follow these steps:

#. **Step 1**. Install the package in your Django Rest Framework project by running the following command:

    
    pip install djangorestframework-api-response


#. **Step 2**. Add 'rest_framework_api' to your Django installed apps in your project's settings.py file:

    
    INSTALLED_APPS = [
        ...
        'rest_framework_api',
    ]


#. **Step 3**. In your Django views, import the StandardAPIView class from the package:

    
    from rest_framework_api.views import StandardAPIView


#. **Step 4**. Use the StandardAPIView class as the base class for your Django view. You can then use the following methods to send responses to the client:

Helper Functions
================

* `send_response(data=None, status=status.HTTP_200_OK)`: Sends a successful response to the client. The data parameter is optional and can be used to include additional data in the response. The status parameter can be used to specify the HTTP status code of the response.

* `send_error(error, status=status.HTTP_400_BAD_REQUEST)`: Sends an error response to the client. The error parameter is required and should be a string describing the error. The status parameter can be used to specify the HTTP status code of the response.

* `paginate_response(self, request, data)`: The paginate_response method takes two arguments: request and data. The request argument is the request object, which contains information about the incoming request (such as the HTTP method, the query parameters, and the payload, if applicable). The data argument is a list of data that you want to paginate.


**Example Views**
**************

*Here is an example view* that demonstrates how to use the StandardAPIView class:


    class HelloWorldView(StandardAPIView):
        def get(self, request, format=None):
            your_condition_here = True
            if your_condition_here:
                dict = {'message':'Hello World!'}
                list = ['This','is','a','List']
                string = 'Tis a string'
                number = 1
                float = 0.4
                object = {'I contain data'}
                return self.send_response(object,status=status.HTTP_201_CREATED)
            else:
                error_message = 'This is a custom error message. I am a String.'
                return self.send_error(error_message)


*Here is an example view* that demonstrates how to use the StandardAPIView class **with a custom success status code**:
    

    class HelloWorldView(StandardAPIView):
        def get(self, request, format=None):
            your_condition_here = True
            if your_condition_here:
                dict = {'message':'Hello World!'}
                return self.send_response(dict,status=status.HTTP_201_CREATED)
            else:
                error_message = 'This is a custom error message. I am a String.'
                return self.send_error(error_message)



When the client sends a request with the success parameter set to true, this view will send a successful response with the message "Hello World!". Otherwise, it will send an error response with the message "Hello Errors!".

The response sent to the client will have the following format:

    {
        "success": true,
        "status": "200"
        "data": {
            "message": "Hello World!"
        },
    }

or

    {
        "success": false,
        "status": "400",
        "error": "This is a custom error message. I am a String."
    }

You can then use the success and data fields in the client to determine the outcome of the request and process the response accordingly.


Paginated Views
===============

To use StandardAPIView, simply inherit it in your view class. You can then use the *`paginate_response`* method to easily paginate any data object and return the paginated response.

**Example Views**
*****************

*Here is an example view* that demonstrates how to use the StandardAPIView class that returns a paginated response:
    

    class HelloWorldPaginatedView(StandardAPIView):
        def get(self, request, format=None):
            data = [
                {'id': 1, 'content': 'Hello'},
                {'id': 2, 'content': 'World'},
                {'id': 3, 'content': 'This'},
                {'id': 4, 'content': 'Is'},
                {'id': 5, 'content': 'A'},
                {'id': 6, 'content': 'Paginated'},
                {'id': 7, 'content': 'Response'},
            ]
            if data:
                return self.paginate_response(data, request, page_size=3, max_page_size=5)
            else:
                return self.send_error('No data found')


The response will be a paginated list of data, with the pagination metadata included in the response. The pagination metadata will include the current page number, the number of results per page, the total number of results, and the total number of pages. 

For example, if there are 10 courses in total and the page size is 3, the response will include metadata indicating that there are a total of 4 pages, with the first page containing the first 3 courses and the second page containing the next 3 courses, and so on. The data for each course will be included in the 'results' field of the response.

Here is an example of what a response might look like:


    {
        "success": true,
        "status": 200,
        "count": 10,
        "next": "http://example.com/api/courses?page=2",
        "previous": null,
        "data": [
        {
            "id": 1,
            "name": "Introduction to Python",
            "description": "Learn the basics of Python programming"
        },
        {
            "id": 2,
            "name": "Advanced Python Techniques",
            "description": "Learn advanced techniques for Python programming"
        },
        {
            "id": 3,
            "name": "Data Science with Python",
            "description": "Learn how to use Python for data analysis and visualization"
        }
        ]
    }

**To make a request to the HelloWorldPaginatedView endpoint**, you can send a GET request to the URL for the view.

For example, if the view is mounted at /api/hello_world, you can send a request like this

    GET /api/hello_world

To specify the page size and maximum page size in the request, you can use the page_size_query_param and page_size query parameters, respectively.

For example, to set the page size to 10 and the maximum page size to 100, you can include the following query parameters in the URL:

    GET /api/hello_world?page_size=10&page_size=100

You can also specify the page number in the request using the **`page_query_param`** query parameter.

For example, to request the second page of results, you can include the following query parameter in the URL:

    GET /api/hello_world?p=2

This will return the second page of results, based on the page size specified in the request.


Django Models
===============

**Example Views**
*****************

    class HelloWorldObjectPaginatedView(StandardAPIView):
        def get(self, request, format=None):
            courses = Courses.objects.all()
            if courses:
                return self.paginate_response(request, courses)
            else:
                return self.send_error('No data found')

This **`HelloWorldObjectPaginatedView`** view should work as intended, as long as the necessary dependencies are imported and the **`Courses`** model is correctly defined.

The view subclass **`StandardAPIView`** and overrides the **`get`** method to return a paginated list of all **`courses`** in the database. If the queryset courses is empty, the view will return an error response using the **`send_error`** method.

You can also include query parameters in the request URL to control the pagination of the response. For example, you can use the page and page_size query parameters to specify the **`page`** number and **`page size`**, respectively.

    http://example.com/api/courses?page=2&page_size=10

This request will retrieve the second page of courses, with a page size of 10 courses per page. The response will include a paginated list of courses, along with metadata about the pagination (such as the total number of courses and URLs for the next and previous pages, if applicable).


Overall Conclusion
===================

The **`StandardAPIView`** class and the **`paginate_response`** method that you have implemented provide a solid foundation for creating views that return paginated responses in your API.

The **``StandardAPIView``** class includes several useful methods, including **`send_response`** and **`send_error`**, which allow you to easily send success and error responses from your views. The **`paginate_response`** method provides a convenient way to paginate data and return a paginated response to the client.

To create views using the **`StandardAPIView`** class, you can subclass **`StandardAPIView`** and override the appropriate HTTP method handler (e.g., **`get`**, **`post`**, **`put`**, etc.). Inside the handler method, you can call the **`paginate_response`** method to paginate and return the data to the client.


Here is an example of a view that uses the StandardAPIView class to return a paginated list of users:

    class UserListView(StandardAPIView):
        def get(self, request):
            users = User.objects.all()  # get all users from the database
            return self.paginate_response(request, users)

This view subclass **`StandardAPIView`** and overrides the **`get`** method to return a paginated list of all users in the database. It does this by calling the **`paginate_response`** method and passing in the request object and the list of users.

With this setup, you can easily create views that return paginated responses to the client using the **`StandardAPIView`** class and the **`paginate__response`** handler function.