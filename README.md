# About this app

## Stack

*  Python 3.6
*  Django 2.1
*  PostgreSQL 9.6
*  Celery 4.2
*  RabbitMQ 3
*  DRF 3.9

## Implementation

This is a dockerised application which provides RESTful API endpoints to upload, download and list
already uploaded images. Currently only .png and .jpeg images are supported. The whole application
consists of 4 containers: web container, celery container, db container and message broker container.

Web container runs django/drf app and provides the endpoints listed below.
DB container stores the Postgres database
Message broker container run rabbit-mq service to allow async implementation of
some functionality
Celery container is built off the same image as the Web container and run async tasks

To run the application you will need to have docker and docker-compose installed

The following endpoints are available:


    api/images/get/<image_id>?img_format=[jpeg|png]
    api/images/list
    api/images/create
    api_token

See 'How to use API' section for more info

## How this application works

Read this section please before proceeding to 'how to run' section

This application required token based authorisation. See 'How to login' part for
valid credentials once you read this section (Admin user with these credentials gets
created when you start the application)

To obtain a token use api_token API

Images can be uploaded in bulk using create api, if you use apps like Postman or insomnia
please make sure that you have multipart/form-data set as Content-Type.
Once images are uploaded the async tasks will run to create same images in different format
E.g. if you have uploaded image img.png then duplciate image will be created in .jpeg format
and vice versa. Duplicates always get created with name <converted_img.[ext]>. File names never
clash as they stored in app root folder in files dicrectory as:


/files/user_<user_id>/hash/image


Duplicate images are created by celery workers asynchronously by copying an existing image and
converting it using imagemagick software.

Each image is created under parent image container object in the database. So, image container
has reverse relationship to all child images

## How to use API

1) First you need to get an access token, use below endpoint

    api_token

2) Now upload one or multiple images

    api/images/create

    make sure that you set multipart/form-data as Content-Type and use the access toke
    from step 1.

    For example, if you upload two images "dog.png" and "cat.jpg", you will get:

        {
            "40": {
                "name": "dog.png"
            },
            "41": {
                "name": "cat.jpg"
            }
        }

    where "40" and "41" are image container IDs which you can use in the next step to download
    an image:

3) Download an image, using below API

        api/images/get/<image_container_id>?img_format=[jpeg|png]

    image_container_id - is an ID of a image container, see step 2. img_format - query
    parameter is optional and defaults to jpeg. If invalid format requested or image
    with requested format has not been generated yet then corresponding message is returned

4) List images using below API:
    
    api/images/list

    example response:

    [
        {
            "id": 1,
            "images": [
                {
                    "name": "dog.png"
                },
                {
                    "name": "converted_img.jpeg"
                }
            ]
        },
        {
            "id": 2,
            "images": [
                {
                    "name": "cat.jpg"
                },
                {
                    "name": "converted_img.png"
                }
            ]
        }
    ]


## How to run

The below command will build and run docker containers, run all the migrations
and craete a user for you

- `docker-compose up`

You can access admin page on:

http://0.0.0.0:7771/


## How to login

You can login to admin portal with the following credentials:

username: admin
password: Admin555

## Todo

### Unit tests
I have spent a lot of time on this application so did not have time to add unit tests
Unit tests required to test all of the controllers and helper functions including async
tasks

### Image upload
Current implementation is naive and not practical. For production implementation one
could use pre-signed URLs to submit the images directly to cloud storage e.g. AWS boto3
Python library provides such functionality so files could be directly uploaded onto S3

### Image bulk download
Currently there's no bulk download functionality

### Image download query param
Image on GET reuqest should be downloding image only if a certain query param is
provided e.g. download=true, otherwise json to be returned with the queried image data

### Docstrings
Class and methods miss docstrings

### Limited number of image types
Currently only jpeg and png supported

### No permissions logic
Any user can see any images right now

### Same docker image used for web and celery
Web container does not really need image converting software

### API library
Did not have time to create API wrapper library (shim)
