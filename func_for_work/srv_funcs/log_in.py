def log_in(driver, user_name, user_passw):

    tag = 'input'
    atribute = 'name'
    atr_val = 'ctl00$FasContent$TextLogin'
    atr_val_p = 'ctl00$FasContent$TextPassword'
    atr_val_enter = 'ctl00$FasContent$ButtonLogin'

    login = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    password = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_p}']")
    button_enter = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_enter}']")

    login.send_keys(user_name)
    password.send_keys(user_passw)
    button_enter.click()

    print(f'Enter to the sytem: {driver.title}')
