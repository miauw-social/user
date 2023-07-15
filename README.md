# user service
This is the base microservice structure for any other service (in python) 


## Events
These are the events this microservice is listening to.

`user.create`: event which triggers user creation.
`user.find`: event which triggers search for user by username/email.
`user.find.id`: event which triggers search for user based on its id.

## Deployment (without miauw stack)

1. Image Build
```sh
$ docker build -t miauw/user .
```
2. Run Image
```
$ docker run -d miauw/user
```