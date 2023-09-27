# property-server

## running docker & pipenv

 - open docker desktop
 - run: docker run -it --rm --name lap4 --mount type=bind,src="$(pwd)",dst=/code -p 5000:5000 python:3.11 bash -c "cd /code && bash
 - pip install pipenv
 - pipenv install
 - pipenv run dev