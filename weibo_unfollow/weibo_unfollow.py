from selenium import webdriver
import time
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
#登陆
browser.get('http://weibo.com/login.php')
#//*[@style]   查找所有包含style的所有元素，所有的属性要加@
browser.find_element_by_xpath('//*[@id="loginname"]').clear()
#输入登录账号
browser.find_element_by_xpath('//*[@id="loginname"]').send_keys('Your ID')
browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').clear()
time.sleep(1)
#输入登陆密码
browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('your password')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/ul/li[1]/a/strong').click()
time.sleep(1)
#browser.find_element_by_link_text("设置")    通过文本定位元素

#取关数量
for cou in range(1,10):
     #定位悬停时的元素
    ActionChains(browser).move_to_element(browser.find_element_by_xpath('//*[@id="Pl_Official_RelationMyfollow__95"]/div/div/div/div[3]/ul/li[1]/div[1]/div[2]/div[5]/p/a[3]/em')).perform()
    time.sleep(2)
    browser.find_element_by_link_text("取消关注").click()
    time.sleep(1)
    #browser.find_element_by_xpath('//*[@id="layer_15660574768511"]/div[2]/div[4]/a[1]').click()
    browser.find_element_by_link_text("确定").click()
browser.quit()
