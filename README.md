# softwarecapstone
Software Capstone Project, Internal 3


### Common Linux commands,
1. `tail -f log.txt # prints all updates to log.txt to the console window.`


### Updating requirements.txt
If you are using a new Python package (e.g import x), it is good to execute
```pip install pipreqs```
```pipreqs /path/to/project```
This command will update requirements.txt. When we install the website on some system, the one setting it up can then simply perform `pip install -r requirements.txt` which will install the list of required Python packages. `requirements.txt` basically is a list of Python requirements for the website.
