from datetime import datetime
from typing import Any

import requests


def search_jobs_offers(start_date: datetime.date, remote: bool, job_name: str) -> list[dict[str, Any]]:
    offset: int = 0
    filtered_job_list: list[dict[str, Any]] = []
    reach_limit_date: bool = False
    while (True):
        data: list[dict[str, Any]] = requests.get(
            f"https://portal.api.gupy.io/api/v1/jobs?jobName=est%C3%A1gio&isRemoteWork={str(remote).lower()}&offset={offset}").json()
        for job in data["data"]:
            if datetime.strptime(str(job['publishedDate']), "%Y-%m-%dT%H:%M:%S.%fZ").date() < start_date:
                reach_limit_date = True
                break
            filtered_job_list.append(job)
        if reach_limit_date:
            break
        offset += 10
    return filtered_job_list


print(search_jobs_offers(datetime(2025, 2, 24).date(), True, "estágio"))