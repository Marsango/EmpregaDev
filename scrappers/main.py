from datetime import datetime
from typing import Any

from GupyScraper import GupyScraper
from Database import Database
from QUERY_PARAMETERS import jobs_names, remote


class ScrapHandler:
    def __init__(self):
        self.__gupy: GupyScraper = GupyScraper()
        self.__jobs_names: list[str] = jobs_names
        self.__remote: bool = remote

    def find_gupy_new_jobs(self):
        available_jobs: list[dict[str, Any]] = []
        for job_name in self.__jobs_names:
            available_jobs.extend(self.__gupy.search_available_jobs_offers(start_date=datetime.today(),
                                                                           remote=self.__remote, job_name=job_name))
        db: Database = Database()
        new_jobs = db.insert_new_jobs(available_jobs)
        