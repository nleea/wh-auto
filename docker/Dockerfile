FROM python:3.12

WORKDIR /app

COPY ../requirements.txt /app/

RUN pip install -r requirements.txt

COPY ../src/ /app/

WORKDIR /log

COPY ../log/ /log/

WORKDIR /app

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]