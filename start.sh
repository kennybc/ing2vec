#!/bin/bash
#scrapy crawl allrecipes -s JOBDIR=crawler/jobdir &
#cd frontend && npm run frontend && cd .. &
uvicorn backend.server:app --reload