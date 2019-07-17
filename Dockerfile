FROM kennethreitz/pipenv

COPY . /app

CMD ["python3", "-u", "waitlist.py", "--notify", "--schedule", "10"]
