import json
import requests
import wget

#api_url = 'https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/getFile?file_id=AgACAgIAAxkBAAIBqmDh_RUzO6Ce4ciXp0BW3tgpyYStAALnszEbLD8QS5x0280w5D89AQADAgADcwADIAQ'

#r = requests.get(api_url)
#print(r.json())
#r_j=r.json()
#dir_image = r_j['result']['file_path']
#print(dir_image)
#print(requests.post("https://ya.ru"))

#f=open(r'1.zip',"wb") #открываем файл для записи, в режиме wb
#ufr = requests.get("https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/photos/file_0.jpg") #делаем запрос
#f.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
#f.close()

wget.download("https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/photos/file_0.jpg")

#def save_from_www(link):
#    filename=link.split('/')[-1]
#    print(filename)
#    r=requests.get(link,allow_redirect=True)
#    open(filename,"wb").write(r.content)

#link1="https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/photos/file_0.jpg"

#print(r[0])