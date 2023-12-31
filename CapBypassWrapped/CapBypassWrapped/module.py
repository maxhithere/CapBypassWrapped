
import requests
import logging
import json
import time
from typing import Dict, Optional, Union


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]')

BASE_URL = "https://api.capbypass.com"

def make_request(url, method, data=None):
    url = f"{url}"
    if method == "GET":
        response = requests.get(url, json=data)
    elif method == "POST":
        response = requests.post(url, json=data)
    return response

def create_task(
    client_key: str,
    task_type: str,
    website_url: str,
    website_pub_key: str,
    website_subdomain: str,
    blob: Optional[str] = None,
    verbal: bool = False,
    app_id: Optional[str] = None,
) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
    url = f"{BASE_URL}/createTask"
    if task_type == "FunCaptchaTask":
        dumped_blob = json.dumps({"blob": blob})
        response = make_request(
            url,
            method="POST",
            data={
                "clientKey": client_key,
                "appId": app_id,
                "task": {
                    "type": "FunCaptchaTaskProxyLess",
                    "websiteURL": website_url,
                    "websitePublicKey": website_pub_key,
                    "funcaptchaApiJSSubdomain": website_subdomain,
                    "data[blob]": dumped_blob,
                },
            },
        )
        if response.status_code == 200:
            if verbal:
                logging.info("FunCaptchaTask created successfully, solving...")
                task_id = response.json().get("taskId")
                status = get_task_result(client_key, task_id, verbal)
                stat = status.get("status", "failed")
                while stat != "ready":
                    time.sleep(0.3)
                    status = get_task_result(client_key, task_id, verbal)
                    stat = status.get("status", "failed")
                    if stat == "ready":
                        logging.info("FunCaptchaTask solved successfully")
                        solution = status.get("solution")
                        return {"solution": solution, "solved": True}
                    if stat == "failed":
                        if verbal:
                            logging.warning(f"Failed to solve captcha: {status}")
                        return {
                            "errorCode": 1,
                            "errorDescription": status,
                            "solved": False,
                        }

            else:
                if verbal:
                    logging.warn("FunCaptchaTask failed to create")
                return {
                    "errorCode": response.status_code,
                    "errorDescription": response.reason,
                    "solved": False,
                }
        else:
            if verbal:
                logging.warning("Invalid task type")

def get_task_result(
    client_key: str,
    task_id: str,
    verbal: bool = False
) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
    url = f"{BASE_URL}/getTaskResult"
    response = make_request(
        url,
        method="POST",
        data={"clientKey": client_key, "taskId": task_id}
    )
    if response.status_code == 200:
        if verbal:
            logging.info("Task result retrieved successfully")
        return response.json()
    else:
        if verbal:
            logging.warn("Task result retrieval failed")
        return {"errorCode": response.status_code, "errorDescription": response.reason}

def get_balance(
    client_key: str,
    verbal: bool = False
) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
    url = f"{BASE_URL}/getBalance"
    response = make_request(
        url,
        method="POST",
        data={"clientKey": client_key}
    )
    if response.status_code == 200:
        if verbal:
            logging.info("Balance retrieved successfully")
        return response.json()
    else:
        if verbal:
            logging.warn("Balance retrieval failed")
        return {"errorCode": response.status_code, "errorDescription": response.reason}
