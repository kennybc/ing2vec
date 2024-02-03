FROM python:3.11

WORKDIR /

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ./entrypoint.sh
#CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "&", "scrapy", "crawl", "allrecipes", "-s", "JOBDIR=crawler/jobdir"]