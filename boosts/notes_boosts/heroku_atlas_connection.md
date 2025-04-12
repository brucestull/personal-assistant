# Heroku Atlas Connection

* Get the local ip address of the production server:
  * `heroku run curl http://ipinfo.io/ip`
  -OR-
  * Using bash:
    1. `heroku run bash`
    1. `ip addr | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'`