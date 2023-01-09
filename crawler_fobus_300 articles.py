
import requests
from lxml import etree
import lxml


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:7890") # 国内设置代理,可注释
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(executable_path='C:/bin/chromedriver.exe', chrome_options=chromeOptions)

home = 'https://www.forbes.com/business/' # 主页
driver.get(home) # 进入主页
sleep(3)

# click 30 次
n = 30
for i in range(n):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 滚动到底部
    print('-'*10 + "scroll to bottom" + '-'*10)
    sleep(3) # 给予页面加载时间
    # 点击more articles
    button = driver.find_element(by=By.CLASS_NAME,value='load-more')
    button.click()
    print('-'*10 + "click more articles" + '-'*10)
    sleep(3) # 给予页面加载时间
    
articles = driver.find_elements(by=By.CLASS_NAME, value='stream-item__title') # 读取所有文章
n = len(articles)
print("一共爬取 {} 个文章".format(n))

proxies = {}
proxies = { "http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"} # 国内设置代理,可注释

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'referer':'https://www.forbes.com/business/',

}

# 爬取页面
def page_txt(title, url):
    response = requests.get(url, headers=headers, timeout=5, proxies=proxies)
    page_text = response.text
    tree = etree.HTML(page_text)
    
    artiles = tree.xpath('//*[@id="article-stream-0"]/div/div[2]//p//text()')
    artile = ''.join(artiles)
    path = f'{title}.txt'
    # 去掉不符合命名条件的数据
    strings = '\/:*?"<>|'
    for s in strings:
        path = path.replace(s, " ")
    f = open(f'article/{path}','w', encoding='utf-8')
    f.write(artile) # 写入文章
    f.close()
    
# 遍历所有的文章，并且进行爬取保存
for num, article in enumerate(articles):
    title = article.text
    url = article.get_attribute('href')
    # print(title,url)
    page_txt(title, url)
    print(f"{num}/{n}",title + "已爬取成功")
    sleep(3) # 休息一下，防止频繁爬取被发现
driver.quit()

    

