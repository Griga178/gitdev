# import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select

binary_yandex_driver_file = '../yandexdriver.exe'

class Work_space():
    def __init__(self, user_name, password, **kwargs):
        self.user_name = user_name
        self.password = password
        self.main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops'
        self._launch_driver(**kwargs)
        self._authorize()

    def _launch_driver(self, **kwargs):
        self.driver = webdriver.Chrome(binary_yandex_driver_file)
        self.driver.implicitly_wait(kwargs.get('implicitly_wait', 1000))

    def _authorize(self):
        self.driver.get(self.main_page)
        self.driver.find_element("id", 'TextLogin').send_keys(self.user_name)
        self.driver.find_element("id", 'FasContent_TextPassword').send_keys(self.password)
        self.driver.find_element("id", 'FasContent_ButtonLogin').click()

    def quick_search(self, search_text):
        if self.driver.current_url != self.main_page:
            self.driver.get(self.main_page)
        if search_text:
            search_input = self.driver.find_element_by_xpath(f"//input[@type='text']")
            search_input.send_keys(search_text)
            select = Select()

            print(search_input.is_selected())
            print(search_input.is_enabled())
            # print(search_input.get_attribute())
            # print(search_input.get_property())
            # search_input.submit()
            search_input.click()
            print(search_input.is_selected())
            print(search_input.is_enabled())
        else:
            print("Не введен search_text")
        print(self.driver)

user_name, user_passw = 'Tishchenko_GL', 'cmec789'

work_space = Work_space(user_name, user_passw)
print(work_space.driver.title)
work_space.quick_search('04-4227/23-0-0')
# work_space.driver.close()


# WEB_ELEMENT
'tag_name', 'text', 'click', 'submit', 'clear', 'get_property', 'get_attribute', 'is_selected', 'is_enabled',
'send_keys', 'is_displayed', 'location_once_scrolled_into_view', 'size',
'value_of_css_property', 'location', 'rect', 'screenshot_as_base64',
'screenshot_as_png', 'screenshot',
'parent', 'id',

# DRIVER
'service', 'command_executor', 'session_id', 'capabilities', 'error_handler', 'w3c',
'launch_app', 'get_network_conditions', 'set_network_conditions', 'execute_cdp_cmd',
'quit', 'create_options',
'file_detector_context', 'mobile', 'name',
'start_client', 'stop_client', 'start_session',
'create_web_element',

'execute', 'get', 'title',
'execute_script', 'execute_async_script', 'current_url',

'page_source', 'close', 'current_window_handle', 'window_handles',
'maximize_window', 'fullscreen_window', 'minimize_window',

'switch_to', 'switch_to_active_element', 'switch_to_window',
'switch_to_frame', 'switch_to_default_content', 'switch_to_alert',

'back', 'forward', 'refresh',
'get_cookies', 'get_cookie', 'delete_cookie', 'delete_all_cookies','add_cookie',
'implicitly_wait', 'set_script_timeout', 'set_page_load_timeout',

'desired_capabilities', 'get_screenshot_as_file',
'save_screenshot', 'get_screenshot_as_png', 'get_screenshot_as_base64',
'set_window_size', 'get_window_size', 'set_window_position', 'get_window_position', 'get_window_rect',
'set_window_rect', 'file_detector', 'orientation', 'application_cache', 'log_types', 'get_log'


# COMMON FIND
'find_element_by_id', 'find_elements_by_id', 'find_element_by_name', 'find_elements_by_name',
'find_element_by_link_text', 'find_elements_by_link_text', 'find_element_by_partial_link_text', 'find_elements_by_partial_link_text',
'find_element_by_tag_name', 'find_elements_by_tag_name', 'find_element_by_xpath', 'find_elements_by_xpath',
'find_element_by_class_name', 'find_elements_by_class_name', 'find_element_by_css_selector', 'find_elements_by_css_selector',
'find_element', 'find_elements'
