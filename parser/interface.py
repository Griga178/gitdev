# import sys
from my_funcs import *
from my_parser import *
from my_classes import *

from PySide6.QtGui import *
from PySide6.QtWidgets import *

import parse_interface as ui



class Parser_interface(QMainWindow, ui.Ui_MainWindow):
    """docstring for Parser_interface."""

    def __init__(self):
        super(Parser_interface, self).__init__()
        self.setupUi(self)

        # print(My_class.one_param)
        # НАСТРОКА КНОПОК ШАПКИ (ПАРСЕР, БАЗА ДАННЫХ)

        # НАСТРОКА КНОПКИ СТАРТА ПАРСИНГА
        self.pushButton.clicked.connect(self.start_parse)
        self.lineEdit.returnPressed.connect(self.start_parse)
        self.row_counter = 0

        # self.toolBar.actionTriggered[QAction].connect(self.toolbtnpressed)
        self.actionParser.triggered.connect(self.tool_btn_clk_parser)
        self.actionData_Base.triggered.connect(self.tool_btn_clk_data)

    def tool_btn_clk_parser(self):
        self.tabWidget.setVisible(1)
        # self.db_tab.setVisible(0)

    def tool_btn_clk_data(self):
        self.tabWidget.setVisible(0)
        # self.db_tab.setVisible(1)

    def start_parse(self):
        self.progressBar.setValue(0)

        text_link = self.lineEdit.text()

        # ВЫДЕЛЕНИЕ ССЫЛОК СПОМОЩЬЮ РЕГУЛЯРОК
        text_link = re.findall(r'[\w\S]+', text_link) #:/.-

        if len(text_link) > 0:

            # ПРОЦЕСС ПАРСИНГА И ВОЗВРАЩЕНИЯ СЛОВАРЯ
            parser_funcs = My_parser()

            # if type(text_link) == str:
            #     page = [text_link.strip()]

            for link in text_link:
                parser_funcs.parse_one_link(link)
                # ДЛЯ ОТОБРАЖЕНИЯ СТАТУСА РАБОТЫ
                pro_cent = round((parser_funcs.parser_counter/len(text_link))*100)
                self.progressBar.setValue(pro_cent)
                if pro_cent == 100:

                    parser_funcs.parser_counter = 0

            self.lineEdit.clear()
            l_d = parser_funcs.parsed_links

            for link in text_link:
                try:
                    main_page = l_d[link].main_page
                    product = "False"
                    model = "False"
                    link = l_d[link].link
                    price = str(l_d[link].pars_price)
                    if price:
                        status = 'Отпарсено'
                    else:
                        status = 'Ошибка!'
                    self.row_counter += 1
                    self.tableWidget.setRowCount(self.row_counter)
                    self.tableWidget.setItem(self.row_counter-1, 0, QTableWidgetItem(main_page))
                    self.tableWidget.setItem(self.row_counter-1, 1, QTableWidgetItem(product))
                    self.tableWidget.setItem(self.row_counter-1, 2, QTableWidgetItem(model))
                    self.tableWidget.setItem(self.row_counter-1, 3, QTableWidgetItem(price))
                    self.tableWidget.setItem(self.row_counter-1, 4, QTableWidgetItem(status))
                    self.tableWidget.setItem(self.row_counter-1, 5, QTableWidgetItem(link))
                except:
                    print(f'Из этого {link} не удалось создать ссылку')




if __name__ == '__main__':
    app = QApplication([])
    w = Parser_interface()
    w.show()
    app.exec()
