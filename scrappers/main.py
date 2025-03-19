import time
from datetime import datetime, timedelta
from typing import Any
from GupyScraper import GupyScraper
from Database import Database
from settings import jobs_names, remote
from TelegramBot import TelegramBot
from LinkedinScraper import LinkedinScraper


class ScrapHandler:
    def __init__(self) -> None:
        self.__gupy: GupyScraper = GupyScraper()
        self.__jobs_names: list[str] = jobs_names
        self.__remote: bool = remote
        self.__telegram_bot = TelegramBot()
        self.__linkedin: LinkedinScraper = LinkedinScraper()

    def find_gupy_new_jobs(self) -> None:
        available_jobs: list[dict[str, Any]] = []
        for job_name in self.__jobs_names:
            print(f"Searching for {job_name} in gupy...")
            available_jobs.extend(self.__gupy.search_available_jobs_offers(start_date=datetime.today().date(),
                                                                           remote=self.__remote, job_name=job_name))
        db: Database = Database()
        print(f"Found {len(available_jobs)} jobs in gupy!")
        self.send_new_jobs_message(db.insert_new_jobs(available_jobs))
        db.close()

    def send_new_jobs_message(self, new_jobs: list[dict[str, str]]) -> None:
        for i, new_job in enumerate(new_jobs):
            message: str = (
                f"Nome: {new_job['name']}\nRemoto: {'Sim' if new_job['is_remote'] else 'Não'}\nAbertura: {new_job['published_date'].strftime('%d/%m/%Y %H:%M')}\n"
                f"Empresa: {new_job['company']}\nLink: {new_job['url']}")
            if new_job['website'] == 'linkedin':
                message += f"\nLink2: https://www.linkedin.com/jobs/view/{new_job['job_id']}/"
            self.__telegram_bot.send_message(message)
            if i % 5 == 0:
                time.sleep(2)

    def find_linkedin_new_jobs(self, listed_at: int) -> None:
        for job_name in self.__jobs_names:
            print(f"Searching for {job_name} in Linkedin...")
            available_jobs: list[dict[str, Any]] = self.__linkedin.search_jobs(job_name=job_name, listed_at=listed_at)
            db: Database = Database()
            for job in available_jobs:
                print(job["name"])
            print(f"Found {len(available_jobs)} {job_name} jobs in Linkedin!")
            self.send_new_jobs_message(db.insert_new_jobs(available_jobs))
            db.close()


if __name__ == '__main__':
    job_finder: ScrapHandler = ScrapHandler()
    job_finder.find_gupy_new_jobs()
    job_finder.find_linkedin_new_jobs(listed_at=86400)
    iterations: int = 0
    print(f"Last update: {datetime.now()}")
    while True:
        hour_now: datetime = datetime.now()
        next_hour: datetime = (hour_now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        time_till_next_hour = (next_hour - hour_now).total_seconds()
        time.sleep(time_till_next_hour)
        job_finder.find_gupy_new_jobs()
        job_finder.find_linkedin_new_jobs(listed_at=11800)
        print(f"Last update: {datetime.now()}")
