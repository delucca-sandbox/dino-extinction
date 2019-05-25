# Dino Extinction
![cover](https://media1.tenor.com/images/dba231f6d236ec0f0464512ebcb3b527/tenor.gif?itemid=11807028)

The year is 2242. The mankind kingdom expanded from Earth to our entire solar system. Our society is flourishing and nothing can stop our species from conquering new solar systems. During our expansion, we met with an ancient enemy in our home land: Dinosaurs. We thought that this hostile predator was extinct 144 million years ago, but it appears that somehow they survived.

You're the captain of a strike force in our planet and your goal is simple: **use your robots to destroy as most dinosaurs as you can.**

## 🧐 What's inside

The service is organized in the following structure:
```
Dino-Extinction-v1.0.0
│
├── dino_extinction
│ ├── blueprints
│ ├── └── <blueprint>
| ├── infrastructure
| ├── temlpates
| ├── static
│ └── __init__.py
│ └── config.yaml
├── features
├── tests
├── CHANGELOG.md
├── COMMANDS.md
├── Dockerfile
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## 🤖 Installation Instructions

To run this app you must have Docker and Docker Compose installed on your machine. You can follow [this guideline](https://docs.docker.com/install/) to install **Docker** and [this one](https://docs.docker.com/compose/install/) to install **Docker Compose**.

With both installed, simply go to the root of this project and them run:
```
$ docker-compose build
$ docker-compose up
```

When you see a dinossaur art and a running message you can start using this application. The serve will be listening on: `http://localhost/`

## ☕ Usage

To understand how to use this app and see all endpoint that this server has, checkout our [commands reference](COMMANDS.md)

## 🐞 Testing

I'm using **Pytest** and **Behave** to run all tests. To runn all behaviour/acceptance tests simply run:

```
$ behave
```

And, for the units tests, run:

```
pytest
```

## 💅 Versioning

We use [SemVer 2.0.0](https://semver.org/) for versioning your releases.
