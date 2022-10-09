FROM snakepacker/python:all
WORKDIR /code
COPY . .
RUN ["make","prepare"]
CMD ["make","run-local-gatherer"]
