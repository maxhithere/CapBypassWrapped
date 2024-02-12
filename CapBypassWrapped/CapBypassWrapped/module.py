
import httpx
import logging
import json
import time
from typing import Dict, Optional, Union
import re


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]')

BASE_URL = "https://capbypass.com/api"

class CapBypass:
    def __init__(self, client_key: str, verbal: bool = False, custom_http_client: Optional[httpx.Client] = None):
        self.client_key = client_key
        self.verbal = verbal
        self.custom_http_client = custom_http_client or httpx

    def make_request(self, url, method, data=None):
        return getattr(self.custom_http_client, method.lower())(url, json=data)
    
    def format_proxy(proxy: str) -> Optional[str]:
        patterns = [
            r'https://([^:/]+):([^@/]+)@([^:/]+):(\d+)',
            r'https://([^:/]+):([^@/]+)@([^:/]+):(\d+)',
            r'https://([^:/]+):(\d+)',
            r'https://([^:/]+):(\d+):([^@/]+):([^@/]+)',
            r'https://([^:/]+):(\d+)@([^:/]+):([^@/]+)',
            r'([^:/]+):(\d+)',
            r'([^@/]+):([^@/]+):([^:/]+):(\d+)',
            r'([^@/]+):([^@/]+)@([^:/]+):(\d+)',
            r'([^:/]+):(\d+):([^@/]+):([^@/]+)',
            r'([^:/]+):(\d+)@([^@/]+):([^@/]+)'
        ]

        for pattern in patterns:
            match = re.match(pattern, proxy)
            if match:
                return ':'.join(match.groups())
        return None

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
                        "type": "FunCaptchaTaskProxyLess",
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
                else:
                    if self.verbal:
                        logging.warn("FunCaptchaTask failed to create")
                    return {
                        "errorCode": response.status_code,
                        "errorDescription": response.reason,
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
            return {"errorCode": response.status_code, "errorDescription": response.reason}

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
            return {"errorCode": response.status_code, "errorDescription": response.reason}