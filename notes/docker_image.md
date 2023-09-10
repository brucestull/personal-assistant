# Docker Image

```yml
jobs:
  build:
    docker:
      - image: cimg/python:3.11.5
    steps:
      - checkout
      - run: python --version
```

![image](https://github.com/brucestull/personal-assistant/assets/47562501/3af55503-4dd3-4d83-8e7e-ca3169968baa)
