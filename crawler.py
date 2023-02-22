import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import os
import time
from tqdm import tqdm
import argparse
from translation import str2bool


class ImageCrawler:
    def __init__(self, **kwargs):
        super(ImageCrawler, self).__init__()
        self.driver = webdriver.Chrome()
        self.wait = kwargs["wait"]
        self.keyword = kwargs["keyword"]
        self.site = kwargs["site"].lower()
        self.ccl = kwargs["CCL"]
        self.save_folder = f"{self.site}_{self.keyword}"
        self.log_file = None

    def create_folder_if_not_exists(self):
        try:
            if not os.path.exists(self.save_folder):
                os.makedirs(self.save_folder)
        except OSError:
            print("Error To Create directory. " + self.save_folder)
        self.log_file = open(os.path.join(self.save_folder, "log.txt"), "w")

    def make_url(self):
        if self.site == "naver" or self.site == "네이버": # 네이버 이미지 검색
            base_url = (
                "https://search.naver.com/search.naver?where=image&section=image&query="
            )
            if self.ccl: # CCL 상업적 이용 가능 옵션
                end_url = (
                    "&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=2"
                    "&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&recent=0&datetype=0&startdate=0&enddate=0&gif=0&optStr=&nso_open=1"
                )
                return base_url + quote_plus(self.keyword) + end_url
            return base_url + quote_plus(self.keyword)

        elif self.site == "google" or self.site == "구글": # 구글 이미지 검색
            base_url = f"https://www.google.co.kr/search?q={self.keyword}&tbm=isch"
            if self.ccl: # CCL 상업적 이용 가능 옵션
                end_url = "&tbm=isch&tbs=il:ol&hl=ko&sa=X&ved=0CAAQ1vwEahcKEwiIzLmbjaj9AhUAAAAAHQAAAAAQAg&biw=2031&bih=1050"
                return base_url + end_url
            return base_url

    def infinite_scroll_down(self): # 최하단 까지 스크롤링
        if self.site == "naver" or self.site == "네이버":
            body = self.driver.find_element(By.TAG_NAME, "body")
            while True:
                body.send_keys(Keys.END)
                if (
                    self.driver.find_elements(
                        By.XPATH, '//div[contains(@class,"photo_loading")]'
                    )[0].get_attribute("style")
                    == ""
                ):
                    time.sleep(self.wait)
                else:
                    break

        elif self.site == "google" or self.site == "구글":
            prev_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            while True:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(self.wait)

                present_scroll_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if present_scroll_height == prev_scroll_height:
                    try:
                        self.driver.find_element(
                            By.CSS_SELECTOR, ".mye4qd"
                        ).click()  # 결과 더보기
                    except:
                        break

                prev_scroll_height = present_scroll_height  # update scroll height

    def get_image_urls(self, retry=3):
        print("***" * 20)
        print("Gathering All Image Information...")
        print("***" * 20)

        if self.site == "naver" or self.site == "네이버":
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.HOME)
            imgs = self.driver.find_elements(
                By.XPATH, '//img[@class="_image _listImage"]'
            )

            urls = []
            for n, img in tqdm(enumerate(imgs), total=len(imgs)):
                if n == 0:
                    img.click()
                    self.driver.implicitly_wait(self.wait)
                count = retry
                origin_img = self.driver.find_element(
                    By.XPATH, '//div[@class="image _imageBox"]//img'
                )
                time.sleep(self.wait)
                while count and not self.check_loaded(origin_img):
                    time.sleep(self.wait)
                    count -= 1

                if self.check_loaded(origin_img):
                    urls.append(origin_img.get_attribute("src"))

                body.send_keys(Keys.RIGHT)
            print(f"{len(urls)}/{len(imgs)} images are loaded")
        else:
            urls = self.driver.find_elements(
                By.CSS_SELECTOR, ".rg_i.Q4LuWd"
            )  # find image class

        print("***" * 20)
        print("All Image Information Gathered !!")
        print("***" * 20)
        print("\n")
        return urls

    def check_loaded(self, img):
        # thumbnail (for naver)
        if self.site == "naver" or self.site == "네이버":
            return False if img.get_attribute("src").endswith("type=a340") else True
        elif self.site == "google" or self.site == "구글":
            pass

    def log(self, index, url):
        self.log_file.write(f"{index+1}, {url}")
        self.log_file.write("\n")

    def save_images(self, image_urls):
        print("***" * 20)
        print("Image Crawling & Saving Start")
        print("***" * 20)
        print("\n")

        if self.site == "naver" or self.site == "네이버":
            for index, image_url in tqdm(enumerate(image_urls), total=len(image_urls)):
                urllib.request.urlretrieve(
                    image_url, os.path.join(self.save_folder, str(index + 1) + ".jpg")
                )
                self.log(index, image_url)
                self.driver.implicitly_wait(self.wait)
                time.sleep(self.wait)

        elif self.site == "google" or self.site == "구글":
            for index, image_url in tqdm(enumerate(image_urls), total=len(image_urls)):
                try:
                    image_url.click()
                    time.sleep(self.wait)
                    self.driver.implicitly_wait(self.wait)
                    image_url = self.driver.find_element(
                        By.XPATH,
                        "//*[@id='Sva75c']/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[1]/div[2]/div[2]/div/a/img",
                    ).get_attribute("src")

                    urllib.request.urlretrieve(
                        image_url,
                        os.path.join(self.save_folder, str(index + 1) + ".jpg"),
                    )
                    self.log(index, image_url)
                    self.driver.implicitly_wait(self.wait)
                except Exception as e:
                    print(e)
                    pass

    def run(self):
        # Keyword에 해당하는 Folder 생성
        self.create_folder_if_not_exists()

        # Keyword에 대한 URL 생성
        search_url = self.make_url()

        # chrome 브라우저 열기
        self.driver.implicitly_wait(self.wait)
        self.driver.get(search_url)

        # 최하단으로 scroll down
        self.infinite_scroll_down()

        # 이미지 URL 획득
        image_urls = self.get_image_urls()

        # Save Image
        self.save_images(image_urls=image_urls)

        # 브라우저 종료 및 로그 기록 종료
        self.driver.quit()
        self.log_file.close()

        print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--wait", type=float, required=True, help="Wait Time For Crawling"
    )
    parser.add_argument("--keyword", type=str, required=True)
    parser.add_argument(
        "--site", type=str, required=True, help="naver, 네이버, google, 구글"
    )
    parser.add_argument("--CCL", type=str2bool, required=True, default="True")
    args = parser.parse_args()

    crawler = ImageCrawler(**args.__dict__)

    crawler.run()
