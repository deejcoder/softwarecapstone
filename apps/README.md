### How to add a new app
1. Create a new directory in the apps folder
    ```bash
    mkdir -p apps/<app_name>
    ```
2. Create a new django app
    ```bash
    python manage.py startapp <app_name> apps/<app_name>
    ```
3. Configure the new app

    a. Edit `apps/<app_name>/__init__.py` with the following:
    ```python
    from .apps import <app_name>Config
    # assure <app_name> is capitlized at the start.
    ```
    b. Edit `apps/<app_name>/apps.py`, assure the following exists:
    ```python
    class <app_name>Config(AppConfig):
        name = 'apps.<app_name>'
    ```
    c. Edit `techpalmy/settings.py` and add the following to PROJECT_APPS:
    ```
    apps.<app_name>,
    ```

You are now set to run the website, `python manage.py runserver`.