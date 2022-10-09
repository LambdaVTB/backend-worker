FROM snakepacker/python:all
WORKDIR /code2
COPY . .
RUN ["make","prepare"]
CMD ["make","run-local-generator"]
