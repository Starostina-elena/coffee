import sys
import sqlite3

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox

from ui_files.main import Ui_MainWindow


class Coffee(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show_table()

    def show_table(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec_())
