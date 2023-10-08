import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]')

class Requester:
    def __init__(self, url):
        self.url = url

    def make_request(self, method, data=None):
        url = f"{self.url}"
        if method == "GET":
            response = requests.get(url, json=data)
        elif method == "POST":
            response = requests.post(url, json=data)
        return response

class CreateTask(Requester):
    def __init__(self):
        super().__init__("https://capbypass.com/api/createTask")

        """

        POST /api/createTask
        Creates a task for solving the selected captcha type.

        """

    def Data(self, client_key, task_type, app_id=None, website_url=None, website_pub_key=None, website_subdomain=None, blob=None, proxy=None, invisible=False, rqdata=None, user_agent=None, verbal=False):
        if task_type == "HCaptchaTask":
            response = self.make_request(path="/createTask", method="POST", data={"clientKey": client_key, "appId": app_id, "task": {"type": "HCaptchaTask", "websiteURL": website_url, "websiteKey": website_pub_key, "isInvisible": invisible, "enterprisePayload": {"rqdata": rqdata}, "userAgent": user_agent, "proxy": proxy}})
            if response.status_code == 200:
                if verbal:
                    logging.info("HCaptchaTask solved successfully")
                return response.json()
            else:
                if verbal:
                    logging.warn("HCaptchaTask failed to solve")
                return {"errorCode": response.status_code, "errorDescription": response.reason, "solved": False}
        elif task_type == "FunCaptchaTask":
            response = self.make_request(path="/createTask", method="POST", data={"clientKey": client_key, "appId": app_id, "task": {"type": "FunCaptchaTask", "websiteURL": website_url, "websitePublicKey": website_pub_key, "websiteSubdomain": website_subdomain, "data[blob]": blob, "proxy": proxy}})
            if response.status_code == 200:
                if verbal:
                    logging.info("FunCaptchaTask solved successfully")
                return response.json()
            else:
                if verbal:
                    logging.warn("FunCaptchaTask failed to solve")
                return {"errorCode": response.status_code, "errorDescription": response.reason, "solved": False}
        
    
class CreateClassificationTask(Requester):
    def __init__(self,):
        super().__init__("https://capbypass.com/api/createTask")

        """
        POST /api/createTask
        This task will only return the correct answers of the image, and not a solved token.
        """

    def Data(self, client_key, task_type, question, queries=None, images=None, app_id=None, verbal=False):
        if task_type == "FunCaptchaClassification":
            response = self.make_request(method="POST", data={"clientKey": client_key, "appId": app_id, "task": {"type": "FunCaptchaClassification", "image": images, "question": question}})
            if response.status_code == 200:
                if verbal:
                    logging.info("FunCaptchaClassification Task solved successfully")
                return response.json()
            else:
                if verbal:
                    logging.warn("FunCaptchaClassification Task failed to solve")
                return {"errorCode": response.status_code, "errorDescription": response.reason, "solved": False}
        elif task_type == "HCaptchaClassification":
            response = self.make_request(method="POST", data={"clientKey": client_key, "appId": app_id, "task": {"type": "HCaptchaClassification", "queries": queries, "question": question}})
            if response.status_code == 200:
                if verbal:
                    logging.info("HCaptchaClassification Task solved successfully")
                return response.json()
            else:
                if verbal:
                    logging.warn("HCaptchaClassification Task failed to solve")
                return {"errorCode": response.status_code, "errorDescription": response.reason, "solved": False}

class GetTaskResult(Requester):
    def __init__(self):
        super().__init__("https://capbypass.com/api/getTaskResult")

        """
        POST /api/getTaskResult
        Retrieves the solution for the specified task.
        """

    def Data(self, client_key, task_id, verbal=False):
        response = self.make_request(method="POST", data={"clientKey": client_key, "taskId": task_id})
        if response.status_code == 200:
            if verbal:
                logging.info("Task result retrieved successfully")
            return response.json()
        else:
            if verbal:
                logging.warn("Task result retrieval failed")
            return {"errorCode": response.status_code, "errorDescription": response.reason}

class GetBalance(Requester):
    def __init__(self):
        super().__init__("https://capbypass.com/api/getBalance")

        """
        POST /api/getBalance
        Retrieves the account balance using the provided account key.
        """

    def Data(self, client_key, verbal=False):
        response = self.make_request(method="POST", data={"clientKey": client_key})
        if response.status_code == 200:
            if verbal:
                logging.info("Balance retrieved successfully")
            return response.json()
        else:
            if verbal:
                logging.warn("Balance retrieval failed")
            return {"errorCode": response.status_code, "errorDescription": response.reason}