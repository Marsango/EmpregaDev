import time
from datetime import datetime
from typing import Any
from GupyScraper import GupyScraper
from Database import Database
from QUERY_PARAMETERS import jobs_names, remote
from telegram.TelegramBot import TelegramBot

class ScrapHandler:
    def __init__(self) -> None:
        self.__gupy: GupyScraper = GupyScraper()
        self.__jobs_names: list[str] = jobs_names
        self.__remote: bool = remote
        self.__telegram_bot = TelegramBot()

    def find_gupy_new_jobs(self) -> None:
        available_jobs: list[dict[str, Any]] = []
        for job_name in self.__jobs_names:
            available_jobs.extend(self.__gupy.search_available_jobs_offers(start_date=datetime.today().date(),
                                                                           remote=self.__remote, job_name=job_name))
        db: Database = Database()
        self.send_new_jobs_message(db.insert_new_jobs(available_jobs))

    def send_new_jobs_message(self, new_jobs: list[dict[str, str]]) -> None:
        for i, new_job in enumerate(new_jobs):
            message: str = (f"Nome: {new_job['name']}\nRemoto: {new_job['is_remote']}\nAbertura: {new_job['published_date']}\n"
                            f"Empresa: {new_job['company']}\nLink: {new_job['url']}")
            self.__telegram_bot.send_message(message)
            if i % 5 == 0:
                time.sleep(2)


if __name__ == '__main__':
    job_finder: ScrapHandler = ScrapHandler()
    job_finder.find_gupy_new_jobs()