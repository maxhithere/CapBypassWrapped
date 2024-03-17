# CapBypassWrapped

`CapBypassWrapped` is a Python module that provides a wrapper for CapBypass, a captcha solving service. This module allows developers to easily integrate captcha solving functionality into their applications without having to write complex code.

## Installation

To install `CapBypassWrapped`, simply run the following command:

```
pip install CapBypassWrapped
```

## Usage

To use `CapBypassWrapped` functions, just import the module:

```python
from CapBypassWrapped import CapBypassWrapped
```

Now initialize the CapBypassWrapped class with your according parameters.

```python
capbypass_instance = CapBypassWrapped(client_key="": str, verbal=False: bool, custom_http_client=None: any)
```

There are lots of different functions you can use with lots of customizability.

Here is every function below and how to initiate each one:

```python
capbypass_instance = CapBypassWrapped(client_key="": str, verbal=False: bool, custom_http_client=None: any)

def get_balance():
    result = capbypass_instance.get_balance()
    print(result) # returns {"credits": str, "errorId": int}

def get_status():
    result = capbypass_instance.get_status()
    print(result) # returns {"tasks":{"FunCaptchaTask": str,"FunCaptchaClassification": str},"problems": dict}

def get_task_result():
    result = CapBypassWrapped.get_task_result(task_id="": str) 
    print(result) # returns {"solution": str, "status": str, "errorId": int}  

def create_funcaptcha_task():
    result = CapBypassWrapped.create_task(task_type="": str, website_url="": str, website_public_key="": str) # optional - blob: str
    print(result) # returns {"taskId": str}  

def create_and_get_task_result_funcaptcha_task():
    result = CapBypassWrapped.create_and_get_task_result(task_type="": str, website_url="": str, website_public_key="": str, delay=5: int) # optional - blob: str
    print(result) # returns {"taskId": str, "solution": str, "time": int} 

def create_classification_funcaptcha_task():
    result = CapBypassWrapped.create_classification_task(task_type="": str, image="": str, question="": str)
    print(result) # returns {"taskId": str}  

def create_and_get_classification_funcaptcha_task_result():
    result = CapBypassWrapped.create_and_get_classification_task_result(task_type="": str, image="": str, question="": str, delay=5: int)
    print(result) # returns {"taskId": str, "solution": str, "time": int} 

```

## License

`CapBypassWrapped` is licensed under the Apache License. See the LICENSE file for more information.

## Contact

If you have any questions or comments about `CapBypassWrapped`, please contact me on discord at @maxhithere
