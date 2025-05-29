FROM python:3.12.3

COPY . .

RUN pip install uv

RUN uv pip install -r \recuirements.txt --system

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]