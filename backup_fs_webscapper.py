
from bs4 import BeautifulSoup
import requests
import pandas as pd










global title, sold, price, family_url_list, dau_page_number_index, optic_daughter_url_list, data_sheet

title = []
sold = []
price = []
family_url_list = []
dau_page_number_index =[]
optic_daughter_url_list = []
data_sheet = []

def serverConnect_par():
    optic_parent_url = "https://www.fs.com/c/optics-and-transceivers-9"
    parent_page_optic = requests.get(optic_parent_url)

    #soup = BeautifulSoup(page.content, 'html.parser')
    soup_parent = BeautifulSoup(parent_page_optic.content, 'html.parser')
    global family_lists
    family_lists = soup_parent.find_all('div', class_="new_products_list isPc_Pad")

def serverConnect_dau():
    for family_list in family_lists:
        family_optic_href = [i['href'] for i in family_list.find_all('a', href=True)]
    for index in range(len(family_optic_href)):
        prefix = "https://www.fs.com" + family_optic_href[index]
        family_url_list.append(prefix)
    print(len(family_url_list))

def serverConnect_page():
    for pagination_index in range(len(family_url_list)):
        global daughter_page_number
        global daughter_page_optic
        
        optic_daughter_url = family_url_list[pagination_index]
        optic_daughter_url_list.append(optic_daughter_url)
        daughter_page_optic = requests.get(optic_daughter_url)
        
        soup_daughter = BeautifulSoup(daughter_page_optic.content, 'html.parser')
        
        daughter_page_number = soup_daughter.find_all('button', class_="page_num")
        
        #debuggin during the website is updated!
        if len(daughter_page_number) == 0:
            continue
        else:
            dau_page_number_index.append(int(daughter_page_number[-1].text))
        
print("family_url_list",family_url_list)
print("optic_daughter_url_list",optic_daughter_url_list)
print("dau_page_number_index",dau_page_number_index)
print("daughter_page_optic",daughter_page_optic)
print("daughter_page_number",daughter_page_number)




# mutiple page on specific product family
    #generate product url
for url_list in range(1): # FAMILY NUMBER VAR : len(optic_daughter_url_list)
    for page_list in dau_page_number_index:
        for page_num in range(page_list): # (page_list-1) EACH FAMILY PAGE NUMBER you have to change this index[0] 
            page_num = page_num + 1
            url = optic_daughter_url_list[url_list]+"?page={}".format(page_num)
            page = requests.get(url)

        #print(page) -> checkin the page work well or not. if you print the response [200], it is sucessed to connect!
            soup = BeautifulSoup(page.content, 'html.parser')
            item_lists = soup.find_all('div', class_="grid_item")
            sold_lists = soup.find_all('section', class_="sold_reviews")
            price_lists = soup.find_all('div',class_='realPrice')



            for item_each in item_lists:
                product_num = item_each.find('h3')
                product_num = product_num.text
                product_num = product_num.replace('\n',"")
                title.append(product_num)

            for sold_each in sold_lists:
                sold_num = sold_each.find('i')
                sold_num = sold_num.text
                sold.append(sold_num)

            for price_each in price_lists:
                price_num = price_each.find('span')
                price_num = price_num.text
                price_num = price_num.replace('US$\xa0',"")
                price.append(price_num)
                count = count + 1
                print("Finished", "count : ",count,"page number : ",page_num,"page_list : ",page_list)
            #print(title)
            #print(title[0])
            # #print(sold)
            #print(len(title),len(sold))
            #print(title[0],title[1])
            #print(price)
            
        data = {'product_name':title,'sold#':sold,'price':price}
        df = pd.DataFrame(data)
        
        data_sheet.append(df)
        print("Data saved!")
        
# generate CSV file for

for data_sheet_number in range(len(data_sheet)):
    data_sheet[data_sheet_number].to_csv(r'C:\\Users\\ktkim\Desktop\web_scraper\\export_dataframe{}.csv'.format(data_sheet_number),index=False, header = True)
    
    
window.mainloop()