FROM python:3.12.3

COPY . .

RUN pip install uv # wget -qO- https://astral.sh/uv/install.sh | sh

RUN uv pip install -r \recuirements.txt --system

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]