from srv_helper import *




page_enter = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'

name = 'Tishchenko_GL'
passe = 'cmec789'


driver.get(page_enter)


authorization_func(name, passe)
