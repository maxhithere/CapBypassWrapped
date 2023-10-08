# CapBypassWrapped

`CapBypassWrapped` is a Python module that provides a wrapper for CapBypass, a captcha solving service. This module allows developers to easily integrate captcha solving functionality into their applications without having to write complex code.

## Installation

To install `CapBypassWrapped`, simply run the following command:

```
pip install CapBypassWrapped
```

## Usage

To use `CapBypassWrapped` classes, import them from the module:

```python
from CapBypassWrapped.module import GetBalance, CreateTask, GetTaskResult, CreateClassificationTask
```

There are lots of different functions you can use with lots of customizability.

Here is every function below and how to initiate each one:

```python
def get_balance():
    result = GetBalance().Data(client_key="key")
    print(result['balance'])

def get_task_result():
    result = GetTaskResult().Data(client_key="key", task_id="Task ID")
    print(result['task'])

def create_funcaptcha_task():
    result = CreateTask().Data(client_key="key", task_type="FunCaptchaTask", website_url="https://www.google.com", website_public_key="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
    print(result['solution'])

def create_hcaptcha_task():
    result = CreateTask().Data(client_key="key", task_type="HCaptchaTask", website_url="https://www.google.com", website_public_key="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", invisible=False, rqdata="Data", user_agent="User Agent")
    print(result['solution'])

def create_funcaptcha_classification_task():
    result = CreateClassificationTask().Data(client_key="key", task_type="FunCaptchaClassification", question="Select all images with a car", images="Base64 Encoded Image")
    print(result['solution'])

def create_hcaptcha_classification_task():
    result = CreateClassificationTask().Data(client_key="key", task_type="HCaptchaClassification", question="Select the point of the bear's nose.", queries=["Base64 Encoded Image", "Base64 Encoded Image"])
    print(result['solution'])
```

There are also extra parameters for creating tasks such as `proxy`, `app_id`, `verbal`

## License

`CapBypassWrapped` is licensed under the Apache License. See the LICENSE file for more information.

## Contact

If you have any questions or comments about `CapBypassWrapped`, please contact me on discord at @maxhithere