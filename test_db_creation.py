#!bin/usr/python3

'''
Testing Database creation using PyQt

Creates a SQLite DB, creates a table, adds data to the table, then closes
the connection
'''

import sys

from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class TestDB(QWidget):

    def __init__(self):

        super().__init__()

        self.createDB()
        self.query()

        self.show()
        # no gui is created, this just to close the application after it runs

    def createDB(self):

        # creates a test database

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('test.db')

        if not self.db.open():

            # displays an error message and stops the connection
            # if self.db.open() returns false
            
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.",
                    QMessageBox.Cancel)
            

            return False

    def query(self):

        # creates a table and adds one record to that table, then closes the
        # database

        query = QSqlQuery()

        query.exec_("CREATE TABLE Q_for_11_18(ID INT PRIMARY KEY, "
                    "FirstName VARCHAR(20), LastName VARCHAR(20)")
        query.exec_("INSERT INTO Q_for_11_18(99999, 'Pat', Coyle')")

        self.db.close()

        return True

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = TestDB()
    sys.exit(app.exec_())
