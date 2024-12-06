FROM python:3

WORKDIR /usr/src/scrapy_project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./scripts/start_race_spider.py"]