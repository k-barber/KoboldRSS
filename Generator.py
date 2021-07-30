import requests
from datetime import datetime, timedelta
import os
import time
import io

top = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="/Pages/styles.css">
    <title>RSS-Generator: Feeds</title>
</head>

<body>
    <a href="/"><img src="/Img/Bocchi.png" id="bocchi"/></a>
    <div id="container">
        <div>
            <a href="http://www.rssboard.org/rss-draft-1" target="_blank"><img id="icon" src="/Img/RSS.png"></a>
            <p><a href="/">Home</a> &gt; My Feeds</p>
            <h1>K-Barber's RSS-Generator: My Feeds</h1>
            <p>A list of your feeds:</p>
            <ul>
'''

bottom = '''
            </ul>
            <button onclick="refresh()">Refresh</button>
        </div>
    </div>
    <script>
        function refresh() {
            location.reload(true);
        }
    </script>
</body>
</html>
'''


class GeneratorInstance:

    debug_mode = False
    shell = None
    browser_instance = None
    start_time = None

    def log(self, text):
        self.shell.print_generator_output(text)

    def __init__(self, shell_param, debug, browser_instance):
        self.debug_mode = debug
        self.shell = shell_param
        self.browser_instance = browser_instance
        self.start_time = datetime.now()
        self.log("Generator starts")

    def check_for_updates(self):
        now = datetime.now()
        modified = datetime.fromtimestamp(
            os.path.getmtime('Feed_Definitions.txt'))
        if (modified >= self.start_time):
            self.log("Feed Definitions have been updated, regenerating feed list")
            self.start_time = now
            self.shell.create_channels()

    def run(self):
        self.update_channels()
        for i in range(0, 300):
            if(self.is_aborted()):
                return
            time.sleep(1)
        self.run()

    def update_channels(self):
        self.log("Checking browser")
        self.browser_instance.login_check(self.shell.channels)
        if(self.is_aborted()):
            return
        if self.browser_instance.start() == True:
            now = datetime.now()
            self.log("Updating Channels")
            for channel in self.shell.channels:
                if(self.is_aborted()):
                    return
                if (channel.lastBuildDate is not None):
                    if (now >= channel.lastBuildDate + timedelta(minutes=int(channel.ttl))):
                        self.generate_items(channel)
                else:
                    self.generate_items(channel)
            if(self.is_aborted()):
                return
            else:
                self.log("Updating in 5 Minutes")
        else:
            self.log("browser failed to start, please restart generator")

    def is_aborted(self):
        if (self.shell.generator_stop_signal.is_set()):
            self.stop()
            return 1
        else:
            return 0

    def stop(self):
        self.shell.generator_stopped_signal.set()

    def generate_items(self, channel):
        text = ""
        self.log("Updating " + channel.title)

        timer = 2
        count = 0
        while (text == ""):
            try:
                if ((channel.logged_URL is not None) or (channel.delay is not None)):
                    text = self.browser_instance.generic_scrape(
                        channel.link, channel.delay)
                else:
                    response = None
                    response = requests.get(channel.link, headers={
                                            'User-agent': 'RSS Generator Bot'})
                    text = response.text
            except Exception as err:
                self.log("Error scraping " + channel.title)
                self.log("Retrying in " + str(timer) + " seconds.")
                if(self.is_aborted()):
                    return
                time.sleep(timer)
                timer = timer * 2
                if (count == 4):
                    f = io.open("error-log.txt", "a", encoding="utf-8")
                    f.write("-------------" +
                            str(datetime.now()) + "-------------\n")
                    f.write(channel.title + "\n")
                    f.write(str(err) + "\n")
                    f.close()
                    break
                else:
                    count += 1
        if (text != ""):
            result = channel.generate_items(text)
            if (result != -1):
                channel.save_channel()
                return
        self.log("Scraping " + channel.title + " failed")
        self.log("Please check 'error-log.txt'")
