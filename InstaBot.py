from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import time
import random


class InstaBot(object):
    def __init__(self, username, password, hashtag):
        """Initialization of the InstaBot

        Arguments:
            object {Instance} -- self is self
            username {String} -- Username to provide to Instagram for login
            password {String} -- Password to provide to Instagram to login
            hashtag {String} -- Hashtag to search on Instagram
        """
        self.username = username
        self.password = password
        self._comments = ['Super', 'Nice', 'Génial', 'Au top',
                          'Jolie photo', 'OMG', 'Nice tips',
                          'Greet feed!', 'Inspiring!', 'Excelent',
                          'Love it', 'Nice catch']

    def launch_browser(self):
        """Launching the webdriver browser
        """
        self.driver = webdriver.Chrome()

    def close_browser(self):
        """Closing the webdriver browser
        """
        self.driver.close()

    def login(self):
        """Login to Instagram
        """
        driver = self.driver
        driver.get('https://www.instagram.com/')
        time.sleep(2)
        elem = driver.find_element_by_name('username')
        elem.send_keys(self.username)
        elem = driver.find_element_by_name(
            'password')
        elem.send_keys(self.password)
        time.sleep(1)
        elem.submit()

        # acpt = driver.find_elements_by_class_name('')
        acpt = ui.WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm")))
        acpt.click()

        # "button[text() = 'Not Now']").click()
        time.sleep(2)

    def collect_links_of_photos(self, hashtag, number_of_scroll):
        """Collecting links based on the hashtag provided and a number of scroll to bottom

        Arguments:
            hashtag {String} -- Hashtag to query on Instagram
            number_of_scroll {Integer} -- Number of scroll to bottom to do

        Returns:
            List -- A list of Instagram links
        """
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        link = set()
        for scroll in range(number_of_scroll):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeigh);")
                time.sleep(1)
                for x in range(1, 10):
                    for y in range(1, 3):
                        cur_link = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[' + str(x) + ']/div[' + str(
                            y) + ']/a')
                        link.add(cur_link.get_attribute('href'))
            except Exception:
                print(Exception)
                continue
        return link

    def like_collected_photos(self, link):
        """Liking an instagram link

        Arguments:
            link {String} -- URL of the Instagram photo to like
        """
        driver = self.driver
        driver.get(link)
        time.sleep(2)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeigh);")
        try:
            time.sleep(random.randint(1, 3))
            like = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
            like.click()
            time.sleep(random.randint(1, 3))
        except Exception as e:
            print(e)
            time.sleep(2)

    def commenting_on_photos(self, comments):
        driver = self.driver
        try:
            button = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[2]/button/span')
            button.click()
        except NoSuchElementException as e:
            print(e)
        try:
            comment_area = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
            comment_area.send_keys = ''
            comment_area.clear()
            for comment in comments:
                comment_area.send_keys(comment)
                time.sleep((random.randint(1, 5) / 30))
            return comment_area
        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False


def launch_bot(bot_username, bot_password, hashtag):
    """Launch the bot with its parameters

    Arguments:
        bot_username {String} -- Instagram username
        bot_password {String} -- Instagram password
    """
    bot = InstaBot(bot_username, bot_password, hashtag)
    bot.launch_browser()
    bot.login()
    collected_links = bot.collect_links_of_photos(hashtag, 3)
    for link in collected_links:
        bot.like_collected_photos(link)
    # bot.like_photos(hashtag)
    # bot.close_browser()


if __name__ == "__main__":
    launch_bot('YOUR_USERNAME', 'YOUR_PASSWORD', 'programming')
