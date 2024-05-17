import webbrowser 
with open('C:/Users/User/Desktop/website.txt') as reader: 
    for link in reader: 
        webbrowser.open(link.strip()) 
