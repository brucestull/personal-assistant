# `pipenv` Notes

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
django = "==4.1.7"
docutils = "==0.19"
gunicorn = "==20.1.0"
whitenoise = "==6.3.0"
psycopg2 = "==2.9.5"
tzdata = "==2022.7"
coverage = "==7.2.6"
python-dotenv = "==1.0.0"
pytest-cov = "==4.1.0"
flake8 = "*"

[dev-packages]

[requires]
python_version = "3.11"

```