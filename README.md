# ProgressBars
A python library to display progress of loops to the user.

# Installation
This library can be installed using pip.
```
pip install progressbars
```

# Usage
The class you'll be using is called the ProgressBar class, here is an example of how to use it.
```python
from progressbars import ProgressBar

import time

def createAccount(name: str) -> None:
    time.sleep(1.5) # This function takes a few seconds to create an account

names = [
  "John",
  "Tom",
  "Candace"
]

# Create an account for everyone in the names list
for name in ProgressBar(names):
    createAccount(name)
```
