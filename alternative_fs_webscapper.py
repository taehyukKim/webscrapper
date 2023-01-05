from bs4 import BeautifulSoup
import requests
import pandas as pd

title = []
sold = []
price = []


family_url_list = []
optic_daughter_url_list = []
dau_page_number_index =[]
dot_progressive =""
data_sheet = []

family_url_list.append("https://www.fs.com/c/200-400-800g-modules-3859")
family_url_list.append("https://www.fs.com/c/50g-100g-modules-3857")
family_url_list.append("https://www.fs.com/c/25-40g-modules-1113")
family_url_list.append("https://www.fs.com/c/10g-modules-56")
family_url_list.append("https://www.fs.com/c/100m-1g-modules-57")
family_url_list.append("https://www.fs.com/c/infiniband-fc-modules-2688")
family_url_list.append("https://www.fs.com/c/other-modules-3681")
family_url_list.append("https://www.fs.com/c/accessories-61")

print(family_url_list[0])

for pagination_index in range(len(family_url_list)):
    optic_daughter_url = family_url_list[pagination_index]
    
    optic_daughter_url_list.append(optic_daughter_url)
    daughter_page_optic = requests.get(optic_daughter_url)
    
    soup_daughter = BeautifulSoup(daughter_page_optic.content, 'html.parser')
    
    daughter_page_number = soup_daughter.find_all('button', class_="page_num")
    
    #debuggin during the website is updated!
    if len(daughter_page_number) == 0:
        dau_page_number_index.append("0")
    else:
        dau_page_number_index.append(int(daughter_page_number[-1].text))
    dot_progressive = dot_progressive + "."
    print(dot_progressive)
#print("family_url_list",family_url_list)
#print("optic_daughter_url_list",optic_daughter_url_list)
#print("dau_page_number_index",dau_page_number_index)
#print("daughter_page_optic",daughter_page_optic)
#print("daughter_page_number",daughter_page_number)
#data_sheet = []
file_name = ["200G_400G_800G Modules","50G_100G Modules","25/40G Modules","10G Modules","100M_1G Modules","InfiniBand_FC Modules","Other Modules","Accessories"]
count = 0
print("##################################################")
print("0. 200G/400G/800G Modules")
print("1. 50G/100G Modules")
print("2. 25G/40G Modules")
print("3. 10G Modules")
print("4. 100M/1G Modules")
print("5. InfiniBand/FC Modules")
print("6. Other Modules")
print("7. Accessories")
familynumber = input("What family you want? : ")
while familynumber != "q":
    familynumber = int(familynumber)
    # mutiple page on specific product family
        #generate product url
    for page_num in range(dau_page_number_index[familynumber]): # (page_list-1) EACH FAMILY PAGE NUMBER you have to change this index[0] 
        page_num = page_num + 1
        url = optic_daughter_url_list[familynumber]+"?page={}".format(page_num)
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
            print("Finished", "count : ",count,"page number : ",page_num,"page_list : ",dau_page_number_index[familynumber])
        #print(title)
        #print(title[0])
        # #print(sold)
        #print(len(title),len(sold))
        #print(title[0],title[1])
        #print(price)

        
    data = {'product_name':title,'sold#':sold,'price':price}
    df = pd.DataFrame(data)
    print("Data saved!")
    
    # generate CSV file for

    df.to_csv(r'C:\\Users\\ktkim\Desktop\web_scraper\\{}_FS_Product.csv'.format(file_name[familynumber]),index=False, header = True)
    familynumber = input("What family you want? : ")
else:
    print("STUTDOWN the webscrapping")
