import wikipediaapi

wiki = wikipediaapi.Wikipedia(user_agent='Wekipedia Search Engine (himanshudevatwal0@gmail.com)', language='en')

page_py = wiki.page('Python_(programming_language)')

print(page_py.exists())
print(page_py.title)
print(page_py.summary)
print(page_py.fullurl)
print(page_py.text)

print(len(page_py.links))

for title in list(page_py.links.keys())[:20]:
    print(title)