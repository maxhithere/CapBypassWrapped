
import httpx
import logging
import json
import time
from typing import Dict, Optional, Union
import re


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]')

BASE_URL = "https://capbypass.com/api"

class CapBypassWrapped:
    def __init__(self, client_key: str, verbal: bool = False, custom_http_client: Optional[httpx.Client] = None):
        self.client_key = client_key
        self.verbal = verbal
        self.custom_http_client = custom_http_client or httpx

    def make_request(self, url, method, data=None):
        return getattr(self.custom_http_client, method.lower())(url, json=data)
    
    def format_proxy(self, proxy):
        regex = r"(?:https://)?(?:(?P<username>\S+):(?P<password>\S+)@)?(?P<hostname>\S+):(?P<port>\S+)"
        match = re.match(regex, proxy)
        if match:
            formatted_string = f"{match['hostname']}"
            if match.group('port'):
                formatted_string += f":{match['port']}"
            if match.group('username'):
                formatted_string += f"@{match['username']}"
            if match.group('password'):
                formatted_string += f":{match['password']}"
            return formatted_string
        else:
            return None
    
    def is_base64_encoded(str):
        regex = r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$'
        return bool(re.match(regex, str))

    def create_task(
        self,
        task_type: str,
        website_url: str,
        website_pub_key: str,
        website_subdomain: str,
        proxy: str,
        blob: Optional[str] = None,
    ) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        url = f"{BASE_URL}/createTask"
        if task_type == "FunCaptchaTask" or task_type == "FunCaptchaTaskProxyLess":
            dumped_blob = json.dumps({"blob": blob})
            proxy = self.format_proxy(proxy)
            response = self.make_request(
                url,
                method="POST",
                data={
                    "clientKey": self.client_key,
                    "task": {
                        "type": "FunCaptchaTask",
                        "websiteURL": website_url,
                        "websitePublicKey": website_pub_key,
                        "funcaptchaApiJSSubdomain": website_subdomain,
                        "data": dumped_blob,
                        "proxy": proxy,
                    },
                },
            )
            if response.status_code == 200:
                if self.verbal:
                    logging.info("FunCaptchaTask created successfully")
                    task_id = response.json().get("taskId")
                    return {"taskId": task_id}
            elif response.status_code != 200:
                    if self.verbal:
                        logging.warn("FunCaptchaTask failed to create")
                    return {
                        "errorCode": response.status_code,
                        "errorDescription": response.text,
                    }
            else:
                if self.verbal:
                    logging.warning("Invalid task type")
                return None

    def get_task_result(self, task_id: str) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        url = f"{BASE_URL}/getTaskResult"
        response = self.make_request(
            url,
            method="POST",
            data={"clientKey": self.client_key, "taskId": task_id},
        )
        if response.status_code == 200:
            if self.verbal:
                logging.info("Task result retrieved successfully")
            return response.json()
        else:
            if self.verbal:
                logging.warn("Task result retrieval failed")
            return {"errorCode": response.status_code, "errorDescription": response.json().get("errorDescription")}

    def get_balance(self) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        url = f"{BASE_URL}/getBalance"
        response = self.make_request(
            url,
            method="POST",
            data={"clientKey": self.client_key},
        )
        if response.status_code == 200:
            if self.verbal:
                logging.info("Balance retrieved successfully")
            return response.json()
        else:
            if self.verbal:
                logging.warn("Balance retrieval failed")
            return {"errorCode": response.status_code, "errorDescription": response.text}
        
    def get_status(self) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        url = f"{BASE_URL}/status"
        response = self.make_request(
            url,
            method="GET",
        )
        if response.status_code == 200:
            if self.verbal:
                logging.info("Status retrieved successfully")
            return response.json()
        else:
            if self.verbal:
                logging.warn("Status retrieval failed")
            return {"errorCode": response.status_code, "errorDescription": response.text}
        
    
    def create_and_get_task_result(self, task_type: str, website_url: str, website_pub_key: str, website_subdomain: str, proxy: str, blob: Optional[str] = None, delay: int = 5) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        task = self.create_task(task_type, website_url, website_pub_key, website_subdomain, proxy, blob)
        if task.get("taskId"):
            task_id = task.get("taskId")
            start = time.time()
            while True:
                task_result = self.get_task_result(task_id)
                if task_result.get("status") == "READY":
                    task_result["time"] = time.time() - start
                    return task_result
                elif time.time() - start > 200:
                    return {"errorCode": 400, "errorDescription": "Task took too long to complete"}
                time.sleep(delay)
        else:
            return task 
        
    def create_classification_task(
        self,
        task_type: str,
        image: str,
        question: str,
    ) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        url = f"{BASE_URL}/createTask"
        if task_type == "FunCaptchaClassification":
            check = self.is_base64_encoded(image)
            if not check:
                if self.verbal:
                    logging.warning("Image is not base64 encoded")
                return {"errorCode": 1, "errorDescription": "Image is not base64 encoded"}
            response = self.make_request(
                url,
                method="POST",
                data={
                    "clientKey": self.client_key,
                    "task": {
                        "type": "FunCaptchaClassification",
                        "image": image,
                        "question": question
                    }
                },
            )
            if response.status_code == 200:
                if self.verbal:
                    logging.info("FunCaptcha Classification Task created successfully")
                    task_id = response.json().get("taskId")
                    return {"taskId": task_id}
            elif response.status_code != 200:
                    if self.verbal:
                        logging.warn("FunCaptcha Classification Task failed to create")
                    return {
                        "errorCode": response.status_code,
                        "errorDescription": response.text,
                    }
            else:
                if self.verbal:
                    logging.warning("Invalid task type")
                return None
        
    def create_and_get_classification_task_result(self, task_type: str, image: str, question: str, delay: int = 5) -> Union[Dict[str, Union[str, bool]], Dict[str, Union[int, str, bool]]]:
        task = self.create_classification_task(task_type, image, question)
        if task.get("taskId"):
            task_id = task.get("taskId")
            start = time.time()
            while True:
                task_result = self.get_task_result(task_id)
                if task_result.get("status") == "READY":
                    task_result["time"] = time.time() - start
                    return task_result
                elif time.time() - start > 200:
                    return {"errorCode": 400, "errorDescription": "Task took too long to complete"}
                time.sleep(delay)
        else:
            return task 
        
