FROM snakepacker/python:all
WORKDIR /code1
COPY . .
RUN ["make","prepare"]
CMD ["make","run-local-parser"]
