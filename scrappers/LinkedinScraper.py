
import time
import traceback
from datetime import datetime
from linkedin_api import Linkedin
from scrappers.Database import Database
from settings import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, use_cookies
from requests.cookies import RequestsCookieJar, create_cookie
from linkedin_api.cookie_repository import CookieRepository
import json


class LinkedinScraper:
    def __init__(self) -> None:
        if use_cookies:
            cookies = json.load(open('./cookies.json'))
            cookie_jar = RequestsCookieJar()
            for cookie_data in cookies:
                cookie = create_cookie(
                    domain=cookie_data["domain"],
                    name=cookie_data["name"],
                    value=cookie_data["value"],
                    path=cookie_data["path"],
                    secure=cookie_data["secure"],
                    expires=cookie_data.get("expirationDate", None),
                    rest={
                        "HttpOnly": cookie_data.get("httpOnly", False),
                        "SameSite": cookie_data.get("sameSite", "unspecified"),
                        "HostOnly": cookie_data.get("hostOnly", False),
                    }
                )
                cookie_jar.set_cookie(cookie)
            new_repo = CookieRepository()
            new_repo.save(cookie_jar, '')
            self.__api: Linkedin = Linkedin("", "", cookies=cookie_jar)
        else:
            if not (LINKEDIN_EMAIL and LINKEDIN_PASSWORD):
                raise ImportError("Cannot import LINKEDIN_EMAIL and LINKEDIN_PASSWORD from settings.py")
            self.__api: Linkedin = Linkedin(username=LINKEDIN_EMAIL, password=LINKEDIN_PASSWORD, refresh_cookies=True)

    def search_jobs(self, job_name: str, listed_at: int) -> list[dict[str, str]]:
        db: Database = Database()
        new_job_list: list[dict[str, str]] = []
        search_params = {
                "keywords": f'\"{job_name}\" -joinrs -bairesdev -netvagas',
                "remote": ["2"],
                "listed_at": listed_at,
            }
        try:
            jobs = self.__api.search_jobs(**search_params)

            for job in jobs:
                try:
                    job_id = job["entityUrn"].split(":")[-1]
                    is_job_in_database = db.is_job_in_database(str(job_id))
                    if not is_job_in_database:
                        details = self.__api.get_job(job_id)
                        new_job: dict[str, str] = {
                            "name": details.get('title', None),
                            "description": details.get('description').get('text'),
                            "type": None,
                            "publishedDate": datetime.fromtimestamp(details.get("listedAt", None)/1000).date(),
                            "applicationDeadline": None,
                            "isRemoteWork": details.get('workRemoteAllowed', None),
                            "website": "linkedin",
                            "id": f"{job_id}"
                        }
                        if details.get("applyMethod").get("com.linkedin.voyager.jobs.OffsiteApply"):
                            new_job["jobUrl"] = details.get("applyMethod").get("com.linkedin.voyager.jobs.OffsiteApply").get("companyApplyUrl").replace("?jobBoardSource=linkedin", "")
                        elif details.get("applyMethod").get("com.linkedin.voyager.jobs.ComplexOnsiteApply"):
                            new_job["jobUrl"] = details.get("applyMethod").get("com.linkedin.voyager.jobs.ComplexOnsiteApply").get("easyApplyUrl")
                        elif details.get("applyMethod").get('com.linkedin.voyager.jobs.SimpleOnsiteApply'):
                            new_job["jobUrl"] = f"https://www.linkedin.com/jobs/view/{job_id}/"
                        if details.get('companyDetails').get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany'):
                            new_job["careerPageName"] = details.get('companyDetails', {}).get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany').get("companyResolutionResult").get("name")
                        elif details.get('companyDetails').get('com.linkedin.voyager.jobs.JobPostingCompanyName'):
                            new_job["careerPageName"] = details.get('companyDetails').get('com.linkedin.voyager.jobs.JobPostingCompanyName').get("companyName")
                        if not new_job["jobUrl"] or not new_job["careerPageName"]:
                            raise Exception

                        time.sleep(2)
                        new_job_list.append(new_job)
                except Exception as e:
                    print(f"Error processing job {job_id}: {str(e)}")
                    print(details)
                    traceback.print_exc()
                    continue

        except Exception as e:
            print(f"Error performing job search: {str(e)}")
            traceback.print_exc()
        return new_job_list

