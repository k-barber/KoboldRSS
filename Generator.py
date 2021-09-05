from RSSChannel import RSSChannel
import requests
from datetime import datetime, timedelta
import os
import time
import io


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
        modified = datetime.fromtimestamp(os.path.getmtime("Feed_Definitions.txt"))
        if modified >= self.start_time:
            self.log("Feed Definitions have been updated, regenerating feed list")
            self.start_time = self.shell.create_channels() + timedelta(minutes=1)
            return True
        return False

    def run(self):
        self.update_channels()
        for _ in range(0, 60):
            if self.is_aborted():
                return
            time.sleep(5)
            if self.is_aborted():
                return
            if self.check_for_updates():
                break
        self.run()

    def update_channels(self):
        self.log("Checking browser")
        try:
            self.browser_instance.login_check(self.shell.channels)
        except Exception as err:
            self.log("Error starting browser")
            self.log((str(err) + "\n"))
        if self.is_aborted():
            return
        if self.browser_instance.start() == True:
            now = datetime.now()
            self.log("Updating Channels")
            for channel in self.shell.channels:
                if self.is_aborted():
                    return

                if channel.lastBuildDate is not None:
                    if now >= channel.lastBuildDate + timedelta(
                        minutes=int(channel.ttl)
                    ):
                        self.generate_items(channel)
                else:
                    self.generate_items(channel)
            if self.is_aborted():
                return
            else:
                self.log("Updating in 5 Minutes")
                self.start_time = self.shell.recompile_definitions() + timedelta(
                    minutes=1
                )
        else:
            self.log("browser failed to start, please restart generator")

    def is_aborted(self):
        if self.shell.generator_stop_signal.is_set():
            self.stop()
            return 1
        else:
            return 0

    def stop(self):
        self.shell.generator_stopped_signal.set()

    def generate_items(self, channel: RSSChannel):
        text = ""
        self.log("Updating " + channel.title)

        timer = 2
        count = 0
        while text == "":
            try:
                if (channel.logged_URL is not None) or (channel.delay is not None):
                    text = self.browser_instance.generic_scrape(
                        channel.link, channel.delay
                    )
                else:
                    response = None
                    response = requests.get(
                        channel.link, headers={"User-agent": "KoboldRSS Bot"}
                    )
                    text = response.text
            except Exception as err:
                self.log("Error scraping " + channel.title)
                self.log("Retrying in " + str(timer) + " seconds.")
                if self.is_aborted():
                    return
                time.sleep(timer)
                timer = timer * 2
                if count == 4:
                    f = io.open("error-log.txt", "a", encoding="utf-8")
                    f.write("-------------" + str(datetime.now()) + "-------------\n")
                    f.write(channel.title + "\n")
                    f.write(str(err) + "\n")
                    f.close()
                    break
                else:
                    count += 1
        if text != "":
            result = channel.generate_items(text)
            if len(result) == 2 and result[0] == "ERROR":
                self.log(result[1])
                self.log("Scraping " + channel.title + " failed")
                self.log("Please check 'error-log.txt'")
            else:
                channel.save_channel()
                return
