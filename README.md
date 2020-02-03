# UpdateWatcher
A python3 service that grabs website updates and checks for changes, e.g. for new version releases. Supports Gotify for notifications.

## Installation
- Just download or clone
- `pip3 install -r requirements.txt`
- Copy config_sample.yaml to config.yaml
- Set up the config
- `python3 main.py`

## Configuration
A sample configuration to watch the GitHub releases page of Gotify is supplied. Generally all sites can be scraped with CSS selectors, if they don't load their content with XHR and active javascript. This only parses plain HTML GET responses.

You can set the update interval in seconds. Please don't abuse other sites with high refresh rates (e.g. every second). You may be blocked by them at some point.

For the Gotify notification service, specify the URL to your server with an application token previously created.
```yaml
# update interval in seconds
update_interval: 86400 # 60 * 60 * 24 = once a day

# notification service. gotify for now
notification_service:
  type: "gotify"
  url: "https://your.gotify.server/message?token=your_token"
```
You can supply different selectors for the notification text and the comparison against the SQLite database. 
The script will send a notification for each update, so you can delete a notification that you've already updated. I may do bulk update notifications in the future.

```yaml
sites:
  # the name of the application
  - name: "Gotify Server"
    # the url to watch for changes
    url: "https://github.com/gotify/server/releases"

    # the CSS selector to watch for changes
    selector: ".label-latest a.muted-link span"

    # selector used for notification service description
    notification_selector: ".label-latest a.muted-link span"
```

Note: Everything below the CSS selector will be checked for changes. If you include something like "Page speed render time" or "Comments section" you may get more updates than intended.

## Bugs, improvements, PRs
Open an issue :-)

## License
See LICENSE file
