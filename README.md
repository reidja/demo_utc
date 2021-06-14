# Interview Chatbot and Resume

This is a very simple webhook and resume that is designed to work with the IBM Watson Assistant.


## Requirements

* Docker
* Docker-Compose
* Python 3

## Webhook

The webhook will accept a JSON request with a parameter called: `timezone`. Based on this, it will return your local time, and the current time in UTC back to the chatbot.

Example flow:

```
User: What time is it?
Chat bot: Your timezone is America/Toronto, it's +4 hours from UTC. Your local time is <X> and UTC time is <Y>.
```

You can view the docs at: https://jrdemo-c4a24be17d2b0bfc980895fd31267ec3-0000.mon01.containers.appdomain.cloud/api/docs

## Development Tools and Libraries (webhook)

You can prepare the environment by running the following commands:

```
cd webhook/
pip install -r requirements-debug.txt
```

## Building the Application

You can build the application and push it to a registry by running the following:

```
docker-compose build
docker-compose push
```

If you update `.env` you can ovveride the default registry.

## Deploying the Application

This application is deployed to a Kubernetes cluster. It makes use
of basic Ingress, Services, and Deployments. It does not store any
data.

You will need to configure `helm` and have it connected to your Kubernetes cluster

```
helm upgrade webhook charts/webhook --install
helm upgrade resume charts/resume --install
```

## Using Postman

A postman collection is provided in the `postman` directory. This collection
provides a few sample requests that can be used when running `docker-compose up`. 

**Note**: Docker will port-forward `127.0.0.1:8000` -> `<container>:8000`


## Running Lint Checker

You can run the lint checker by calling `flake8` from within the
`webhook/src` directory.

This is automatically performmed when running `docker-compose build`

```
flake8
```

## Running Unit Tests

You can run the unit tests by calling `pytest` from within the `webhook/src` directory.

This is automatically performmed when running `docker-compose build`

```
pytest
```
