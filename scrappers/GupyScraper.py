from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import requests

from settings import forbidden_words


class GupyScraper:
    def __int__(self) -> None:
        pass

    def search_available_jobs_offers(self, start_date: datetime.date, remote: bool, job_name: str) -> list[dict[str, Any]]:
        offset: int = 0
        filtered_job_list: list[dict[str, Any]] = []
        reach_limit_date: bool = False
        while (True):
            data: list[dict[str, Any]] = requests.get(
                f"https://portal.api.gupy.io/api/v1/jobs?jobName={job_name.lower()}&isRemoteWork={str(remote).lower()}&offset={offset}").json()
            if len(data["data"]) == 0:
                break
            for job in data["data"]:
                if datetime.strptime(str(job['publishedDate']), "%Y-%m-%dT%H:%M:%S.%fZ").date() < start_date:
                    reach_limit_date = True
                    break
                job["website"] = "gupy"
                job["jobUrl"] = job["jobUrl"].replace("?jobBoardSource=gupy_portal", "")
                if job["applicationDeadline"] is None:
                    job["applicationDeadline"] = datetime.strptime(str(job['publishedDate']), "%Y-%m-%dT%H:%M:%S.%fZ").date() + timedelta(30)
                job["publishedDate"] = datetime.strptime(str(job['publishedDate']), "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/Sao_Paulo"))
                job["applicationDeadline"] = datetime.strptime(str(job['applicationDeadline']), "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/Sao_Paulo"))
                have_forbidden_words: bool = False
                for word in forbidden_words:
                    if word.lower() in job["name"].lower():
                        have_forbidden_words = True
                        break
                if have_forbidden_words:
                    continue
                filtered_job_list.append(job)
            if reach_limit_date:
                break
            offset += 10
        return filtered_job_list


