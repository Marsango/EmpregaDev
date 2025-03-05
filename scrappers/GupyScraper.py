from datetime import datetime
from typing import Any

import requests


class GupyScraper:
    def __int__(self):
        pass

    def search_available_jobs_offers(self, start_date: datetime.date, remote: bool, job_name: str) -> list[dict[str, Any]]:
        offset: int = 0
        filtered_job_list: list[dict[str, Any]] = []
        reach_limit_date: bool = False
        while (True):
            data: list[dict[str, Any]] = requests.get(
                f"https://portal.api.gupy.io/api/v1/jobs?jobName={job_name.lower()}&isRemoteWork={str(remote).lower()}&offset={offset}").json()
            for job in data["data"]:
                if datetime.strptime(str(job['publishedDate']), "%Y-%m-%dT%H:%M:%S.%fZ").date() < start_date:
                    reach_limit_date = True
                    break
                filtered_job_list.append(job)
            if reach_limit_date:
                break
            offset += 10
        return filtered_job_list


