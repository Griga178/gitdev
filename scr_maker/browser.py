import webbrowser

def open_page(url):
    webbrowser.get(using = 'windows-default').open_new_tab(url)
