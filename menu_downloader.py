# -*- coding: utf-8 -*-

'''
Simple Menu downloader
Autor: André F L Alves
Email:andreflalves@gmail.com
'''

import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#this function is used to check if a promotion exists
def check_exists_by_class(e_class):
    try:
        driver.find_element_by_css_selector(e_class)
    except NoSuchElementException:
        return False
    return True

driver = webdriver.Firefox()

#navigating to bauru restaurants
restaurants = []

driver.get("http://www.paparango.com.br/passo2/bauru-sp")
element = driver.find_element_by_xpath(\
                              '//*[@id="area-cidades-papa"]/div[2]/ul/li[2]/a')
element.click()

element3 = driver.find_element_by_id("tab_balcao")
element3.click()

element2 = driver.find_element_by_id("btn_pedido_balcao")
element2.click()

#creating a list with the link for each restaurant
rest = driver.find_elements_by_css_selector(\
                                   ".cada_restaurante.mb15.relative.arredonda")
for r in rest:
    link = r.find_element_by_css_selector('a').get_attribute('href')
    print link
    restaurants.append(link)
  
rest_json = {}
i = 0

#getting each restaurante menu
for rest in restaurants:
    driver.get(rest)
    print driver.title
    if rest != "http://www.paparango.com.br/delivery/bauru-sp/planeta-lanches"\
            and "donatello-pizzaria" not in rest:
    
        #closing pop up about delivery details & promotions
        if check_exists_by_class(".fancybox-skin"):
            print "Closing promotion popup"
            driver.find_element_by_id("fecha_promocao").click()
        
        r_name = driver.find_elements_by_class_name("tit_res_p3")[0].text
        rest_json[r_name] = {}
        #print driver.page_source
    
    
    #getting all categories
        categories = driver.find_elements_by_class_name("titulo_comidas")
        
        for category in categories:
            #category name
            category_name = category.find_elements_by_css_selector( \
                                                      '.fl.altura_titulo.ls-1')
            print "Scrapping Category = " + category_name[0].text
            
            items = category.find_elements_by_class_name("cada_prato")
            rest_json[r_name][category_name[0].text] = {}
        
            #inserting items in each category
            for item in items:
    
                item_data = item.find_elements_by_class_name('tit_prato')
                #getting Item name and description
                for x in item_data:
                    #print "Item text = " + x.text
                
                    #item name
                    i_name = x.text.split("\n")[0]
                    rest_json[r_name][category_name[0].text][i_name] = []
                    #print "Item Name = " + i_name
                    
                    #item description
                    i_desc = x.text.split("\n")[1]
                    rest_json[r_name][category_name[0].text][i_name].append(\
                                                                        i_desc)
                    #print "Item Description = " + i_desc
                
                #item price
                i_price = item.find_elements_by_class_name('preco')
                rest_json[r_name][category_name[0].text][i_name].append(\
                                                               i_price[0].text)
                #print "Item price = {}" .format(i_price[0].text)
                
        i = i + 1
        

j = json.dumps(rest_json, sort_keys=True,
                    indent=4, separators=(',', ': '))  

with open('data.txt', 'w') as f: 
     f.write(j)
