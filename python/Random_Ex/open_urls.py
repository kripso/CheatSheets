import webbrowser

tabs = input("tabs at a time: ")
urls = input("urls file path: ")

with open("./urls.txt") as file:
    for index, url in enumerate(file):

        webbrowser.open_new_tab(url)
        if index % tabs == 0:
            input("Press any key to continue...")
