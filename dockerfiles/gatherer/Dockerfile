FROM snakepacker/python:all
WORKDIR /code3
COPY . .
RUN ["make","prepare"]
CMD ["make","run-local-gatherer"]
