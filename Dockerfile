FROM python3.12.3

COPY . .

RUN pip install -r recuirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]