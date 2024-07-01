from bs4 import BeautifulSoup
import seleniumwire.undetected_chromedriver as uc
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

# Script variables
team = "pediatrics"
fileName = "_data.xlsx"
fullFile = team + fileName

def get_funding(text):
    return text

def read_data(dr, url):
    dr.get(url)
    time.sleep(3)
    body = dr.find_element(By.TAG_NAME, "body")
    # print(button.parent)
    # dr.implicitly_wait(2)
    # ActionChains(dr).move_to_element(button).click(button).perform()
    # dr.find_element(By.TAG_NAME, "input").click();
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click() 
    # wait for CloudFlare
    # wait = WebDriverWait(dr, 10)

    # wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='ray-id']")))
    # now get page content
    bs = BeautifulSoup(body.text,"html.parser")
    text = bs.findAll(string=True)

    return text;


def setup_driver():
    ## Set chrome Options
    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-blink-features")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-extensions")

    ## Disable loading images for faster crawling
    # options.add_argument("--disable-extensions")
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    

    # user_agents = [
    #     # Add your list of user agents here
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    # ]

    # select random user agent
    # user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    # options.add_argument(f'user-agent={user_agent}')

    # Initialize the WebDriver
    dr = uc.Chrome(options=options, use_subprocess=True)
    dr.maximize_window()
    return dr

def get_data():
    wb = load_workbook(filename = fullFile)
    # print(wb)
    sheet = wb["data"]
    # print(sheet)
    return sheet


# def make_data_file():   
#   #don't overwrite existing file
#   df = Path(fullFile)
#   if df.is_file():
#     return
#   # doesn't exist, create it
#   headers = ['PMID', 'DOI', ]
#   wb = Workbook()
#   wb.create_sheet("data")
#   wb.save(fullFile)
#   wb.path = fullFile

# setup reader
dr = None
try:
    dr = setup_driver()
except Exception as error:
    "Error during driver setup: {0}".format(error)

data = None
try:
    data = get_data()
except Exception as error:
    msg = "Error during driver setup: {0}".format(error)
    print(msg)

def process(text):
    print(text)

# main program loop
for i in range(2, data.max_row):
    doi = data.cell(row = i, column = 2).value
    url = "https://doi.org/" + doi
    # url = "https://www.nowsecure.nl/"
    print(url)
    text = read_data(dr, url)
    process(text)