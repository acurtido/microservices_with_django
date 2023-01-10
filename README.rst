Microservices with Django Rest Framework
#########################################

Microservices is an architectural approach where a large application is broken down into smaller, independent services that communicate with one another through APIs. 

Each service has a specific responsibility and can be deployed, scaled, and maintained separately.

The main goal of microservices is to improve scalability, flexibility, and maintainability of large applications. By breaking down a monolithic application into smaller services, teams can work on individual services in parallel, which can lead to faster development times. 

Each service can be deployed, scaled, and maintained independently, allowing teams to make changes without affecting other parts of the application. 

This can lead to reduced downtime and faster deployment cycles.

Advantages
===========

* One of the main advantages of microservices is that it allows for a more modular design, which makes it easier to identify and fix issues. 
* Microservices can also make it easier to implement new features and technologies, as each service can be updated independently. 
* Furthermore, microservices are typically easier to test than monolithic applications, which can lead to higher-quality code and fewer bugs.

Disadvantages
==============

However, there are also some disadvantages to microservices.

* One of the biggest challenges is the complexity of communication between services, which can make it more difficult to ensure that all services are working together correctly.
* In addition, it can be more difficult to track data flow and troubleshoot issues in a microservices environment.
* Also, there is a learning curve to using microservices and the infrastructure and support is more complex
* Microservices are very expensive to deploy and maintain


**Microservices are not suitable for small projects.** They are best used for large projects with many teams, where each team will work on a separate service.

Project Description
********************

Our project is an e-commerce marketplace for online courses and physical products. We will be building it using microservices architecture, with each service being responsible for a specific functionality. 

We will be utilizing the power of Django Rest Framework for creating web APIs for our services.

PostgreSQL will perfectly suit all our data storage needs, and Redis for caching. To connect our services and handle asynchronous communication between them, we will be using Apache Kafka (Confluent Cloud) as our event bus. 

This allows for a decoupled architecture, where services can communicate and work together in a loosely coupled fashion.

Our goal is to create a highly scalable and fault-tolerant e-commerce platform that can handle a large number of requests and users. By using microservices and event-driven architecture, we aim to create a system that can easily adapt to changing business requirements and can evolve over time without introducing too much technical debt. 

Additionally, we want to provide a platform that is easy to understand, test and deploy.

Getting Started
****************

#. **Download the project files** and install all dependencies by running:

    .. code-block:: bash

        $ docker-compose up

#. **Start each microservice separately** by navigating to the directory of the service and running the appropriate command for your build system, for example:

    .. code-block:: bash

        $ docker-compose up

#. Pay attention to the consumer.py and producer.py files, these are example files with dummy data provided. You must connect to confluent kafka cloud services through google cloud platform.
#. Create topics in apache kafka and subscribe your consumer.py to each topic according to its functionality.
#. One big challenge will be how to make an authorized request to a service that requires the user authentication. Let's see a `code example on how to tackle this challenge`

    .. code-block:: python

        Python code goes here

**Development**
****************
How to develop the app and add more functionality according to your needs

**Production**
**************

#. You may want to use kubernetes, convert the docker-compose.yaml file into its corresponding kubernetes yaml file.
#. Deploy kubernetes on your favorite cloud service provider.
#. Decide wether you want a database inside kubernetes or you want a separate database hosted on the same cloud provider.
#. Each service works separately so you are good to go, make sure the authentication app is always running in order to register new users. It's not necessary, but common sense tells apart the chimps from humans.

**CI/CD**
**********
Now we will talk about continuous integration and deployment of our application.

**Security**
*************
How we handle vulnerabilities.

**Scalability**
****************
How to scale our systems to millions of users.