import sys
import sqlite3

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from UI.main import Ui_MainWindow
from UI.edit_db import Ui_Dialog


class EditDataBase(QDialog, Ui_Dialog):

    def __init__(self, mode, data=None):
        super().__init__()
        self.setupUi(self)

        if mode == 'new':
            self.setWindowTitle('Добавление элемента')
            self.coffee_id = None
        else:
            self.setWindowTitle('Редактирование элемента')
            self.lineEdit.setText(data[1])
            self.lineEdit_2.setText(data[2])
            self.lineEdit_3.setText(data[3])
            self.lineEdit_4.setText(data[4])
            self.lineEdit_5.setText(str(data[5]))
            self.lineEdit_6.setText(str(data[6]))
            self.coffee_id = data[0]

        self.pushButton.clicked.connect(self.save)

    def save(self):
        try:

            con = sqlite3.connect('data/coffee.sqlite')
            cur = con.cursor()

            name = self.lineEdit.text()
            value_of_fire = self.lineEdit_2.text()
            condition = self.lineEdit_3.text()
            description = self.lineEdit_4.text()
            price = int(self.lineEdit_5.text())
            size = int(self.lineEdit_6.text())

            if self.coffee_id:
                cur.execute(f"""
                            UPDATE coffee
                            SET
                                name = '{name}',
                                value_of_fire = '{value_of_fire}',
                                condition = '{condition}',
                                description = '{description}',
                                price = {price},
                                size = {size}
                            WHERE
                                id = {self.coffee_id}
                            """)
            else:
                cur.execute(f"""
                INSERT
                INTO coffee(name, value_of_fire, condition, description, price, size)
                VALUES('{name}', '{value_of_fire}', '{condition}', '{description}', {price}, {size}) 
                """)

            con.commit()
            con.close()

            ex.show_table()

            self.close()

        except Exception as e:
            print(e)
            self.message.setText('Некорректный ввод')


class Coffee(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show_table()

        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.new)

    def edit(self):

        global form

        self.tableView.selectRow(self.tableView.currentIndex().row())
        data = []
        for i in self.tableView.selectedIndexes():
            data.append(i.data())

        if data:
            form = EditDataBase('edit', data)
            form.show()

    def new(self):

        global form

        form = EditDataBase('new')
        form.show()

    def show_table(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        query = QSqlQuery(db)
        query.exec(f"""
        SELECT
            ID as ID,
            name as 'название сорта',
            value_of_fire as 'степень обжарки',
            condition as 'молотый/в зернах',
            description as 'описание вкуса',
            price as 'цена',
            size as 'размер упаковки'
        FROM coffee
        """)

        model.setQuery(query)

        while model.canFetchMore():
            model.fetchMore()
        model.fetchMore()

        self.tableView.setModel(model)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec_())
