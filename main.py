from selenium import webdriver
from time import sleep
from secrets import pw, user


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://www.instagram.com")
        sleep(2)
        # self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(10)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following  = self._get_names_()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
            .click()
        followers = self._get_names_()
        not_following_back = [user for user in following if user not in followers]
        print("List of not following back")
        print(not_following_back)

    def _get_names_(self):
        sleep(4)
        sugs = self.driver.find_element_by_xpath("//ul/li[last()]")
        self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(5)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                            return arguments[0].scrollHeight;
                            """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names



mybot = InstaBot(user,pw)
mybot.get_unfollowers()
