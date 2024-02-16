from PyQt5.QtWidgets import *
from PyQt5 import uic
import json


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("app.ui", self)
        self.show()

        self.file = None
        self.FileOpenButton.clicked.connect(self.open_file)
        self.AddItemUI.clicked.connect(self.additem1)
        self.AddItemJSON.clicked.connect(self.additem2)
        self.SearchBar.textChanged.connect(self.search)
        self.data = []

    def search(self):
        # Getting the search content.
        search = self.SearchBar.text()

        #defining the variable for the data to show.
        data = []
        
        # Checking the presence of the search content in every row.
        for i in self.data:
            if search.lower() in i["item"].lower():
                CP = int(i["CP"])
                SP = int(i["SP"])
                if SP > CP:
                    profit = str((SP-CP)*100/CP)

                elif SP == CP:
                    profit = str(0)
                
                else:
                    loss = ((CP-SP)*100/CP)
                    profit = f"-{loss}"

                i["profit"] = profit

                data.append(i)

            else:
                continue
        
        # Presenting the data into the table.
        self.ItemTable.setRowCount(len(data))
        row = 0
        for i2 in range(0, len(data)):
            self.ItemTable.setItem(row, 0, QTableWidgetItem(data[i2]["item"]))
            self.ItemTable.setItem(row, 1, QTableWidgetItem(str(data[i2]["CP"])))
            self.ItemTable.setItem(row, 2, QTableWidgetItem(str(data[i2]["SP"])))
            self.ItemTable.setItem(row, 3, QTableWidgetItem(str(data[i2]["profit"])))
            row += 1

    def open_file(self): #incomplete
        file = QFileDialog.getOpenFileName(self, "JSON FILE TO OPEN", "", "JSON FILES (*.json);; ALL FILES (*)")

        if file != ('', ''):
            self.FileNameLabel.setText(file[0])
            self.view(file[0])
            self.file = file[0]

        else:
            windowmessagebox = QMessageBox()
            windowmessagebox.setText('Process Cancelled')
            windowmessagebox.exec_()

    def view(self, file_name):
        file = open(file_name, "rt")
        file_contents = file.read()
        items = json.loads(file_contents)
        self.data = items

        self.ItemTable.setRowCount(len(items))
        row = 0
        for i in range(0, len(items)):
            CP = items[i]["CP"]
            SP = items[i]["SP"]
            if SP > CP:
                profit = str((SP-CP)*100/CP)

            elif SP == CP:
                profit = str(0)
            
            else:
                loss = ((CP-SP)*100/CP)
                profit = f"-{loss}"
            
            self.ItemTable.setItem(row, 0, QTableWidgetItem(items[i]["item"]))
            self.ItemTable.setItem(row, 1, QTableWidgetItem(str(items[i]["CP"])))
            self.ItemTable.setItem(row, 2, QTableWidgetItem(str(items[i]["SP"])))
            self.ItemTable.setItem(row, 3, QTableWidgetItem(str(profit)))
            row += 1
        
        self.JSONCode.setText(file_contents)
        self.SearchBar.setText("")
    
    def additem1(self):
        try:
            ItemName = str(self.ItemName.text())
            CostPrice = int(self.ItemCost.text())
            SellingPrice = int(self.ItemMRP.text())
            json_file = open(self.file, "rt")
            content = {"item":ItemName, "CP":CostPrice, "SP":SellingPrice}
            whole_content = json.load(json_file)
            whole_content.append(content)
            whole_json_content = json.dumps(whole_content)
            json_file.close()
            file = open(self.file, "w")
            file.write(whole_json_content)
            file.close()
            self.view(self.file)
            qtmessagebox = QMessageBox()
            qtmessagebox.setText("Added Successfully")
            qtmessagebox.exec_()
        
        except Exception as E:
            qtmessagebox = QMessageBox()
            qtmessagebox.setText(f"ERROR")
            qtmessagebox.exec_()
            self.view(self.file)
        

    def additem2(self):
        try:
            code = self.JSONCode.toPlainText()
            file = open(self.file, "w")
            file.write(code)
            file.close()

            alertbox = QMessageBox()
            alertbox.setText("Saved Successfully")
            alertbox.exec_()
            self.view(self.file)

        except:
            alertbox = QMessageBox()
            alertbox.setText("ERROR")
            alertbox.exec_()
            self.view(self.file)


def main():
    app = QApplication([])
    window = Window()
    app.exec_()


if __name__ == '__main__':
    main()
