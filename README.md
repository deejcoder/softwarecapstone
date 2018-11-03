# softwarecapstone
Software Capstone Project, Internal 3

[![CircleCI](https://circleci.com/gh/dy1zan/softwarecapstone.svg?style=shield&circle-token=9769eaace82e4eae838ec5f567239f527548d6a0)](https://circleci.com/gh/dy1zan/softwarecapstone)

## Wiki
Please do check the Wiki regularly. [Wiki](https://github.com/dy1zan/softwarecapstone/wiki) updates are not sent to Discord.


## Roadmap
```
- techpalmy/    ; root project folder (contains settings.py)
- static/       ; root static files such as jquery-min.js
- templates/    ; root templates e.g index.html
- media/        ; media that users upload such as user avatars
- apps/         ; project apps
    |- user
    |- jobs
    |- event
    |- ...
- configs/      ; for configuration scripts/templates
- docs/         ; for documentation; files, images
```

## Updating requirements.txt
`requirements.txt` contains a list of project pre-requirements. They must be installed before the website can be run. It's important to keep this updated: when you add any python dependencies, add it to `requirements.txt`.

You can also automate this using,
```bash
pip install pipreqs
pipreqs /path/to/project
```

To install requirements, before starting the website: `pip install -r requirements.txt`.