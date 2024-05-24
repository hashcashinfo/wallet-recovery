import sys
import os
import re
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow, QAction, qApp
from pycoin.symbols.btc import network as btcnet
from pycoin.symbols.doge import network as dogenet
from pycoin.symbols.ltc import network as ltcnet

def extractPrivKeys(filebinary):
    secre = re.compile(b'(\x01\x01\x04[\x10-\x20].{34})')
    secset = set()
    for match in secre.findall(filebinary):
        key = match.hex()
        numtoread = int.from_bytes(bytes.fromhex(str(key[6:8])), 'big')
        keyexpo = bytes.fromhex(key[8:][:numtoread * 2])
        secint = int.from_bytes(keyexpo, 'big')
        secset.add(secint)
    return secset

def extractKeyMetas(filebinary):
    kmre = re.compile(b'\x07keymeta!([\x02|\x03][\x00-\xFF].{32})')
    kmetaset = set()
    for match in kmre.findall(filebinary):
        key = match.hex()
        kmetaset.add(key)
    return kmetaset

def generate_addresses(secset, currency):
    if currency == "BTC":
        net = btcnet
    elif currency == "DOGE":
        net = dogenet
    elif currency == "LTC":
        net = ltcnet
    else:
        raise ValueError("Invalid currency")

    addr_set = set()
    for seci in secset:
        keyp = net.keys.private(is_compressed=True, secret_exponent=seci)
        addr_set.add(keyp.address())
    return addr_set

class WalletRecoveryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wallet Recovery')
        self.setMinimumSize(640, 640)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.script_logs = QTextEdit()
        self.script_logs.setReadOnly(True)
        layout.addWidget(self.script_logs)

        self.file_select_button = QPushButton('Select Wallet File')
        self.file_select_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_select_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Coin', 'Address'])
        layout.addWidget(self.table_widget)

        self.export_csv_button = QPushButton('Export to CSV')
        self.export_csv_button.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_csv_button)

        self.central_widget.setLayout(layout)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        select_action = QAction('Select Wallet File', self)
        select_action.triggered.connect(self.select_file)
        file_menu.addAction(select_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(qApp.quit)
        file_menu.addAction(exit_action)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Wallet File", "", "All Files (*);;Dat Files (*.dat)", options=options)
        if file_name:
            self.recover_wallet(file_name)

    def recover_wallet(self, file_name):
        with open(file_name, 'rb') as f:
            walletbinary = f.read()

        keymetas = extractKeyMetas(walletbinary)
        secrets = extractPrivKeys(walletbinary)

        btc_addresses = generate_addresses(secrets, "BTC")
        doge_addresses = generate_addresses(secrets, "DOGE")
        ltc_addresses = generate_addresses(secrets, "LTC")

        self.script_logs.clear()
        self.script_logs.append(f"Opened file: {os.path.abspath(file_name)}")
        self.script_logs.append(f"There are potentially {len(keymetas)} Keymetas and {len(secrets)} Private Keys in this wallet")

        self.populate_table([
            ("BTC", btc_addresses),
            ("Dogecoin", doge_addresses),
            ("Litecoin", ltc_addresses)
        ])

    def populate_table(self, addresses):
        self.table_widget.setRowCount(0)
        for coin, addr_set in addresses:
            for address in addr_set:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(coin))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(address))

        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setMinimumSectionSize(150)

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)", options=options)
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Coin', 'Address'])
                for row in range(self.table_widget.rowCount()):
                    coin = self.table_widget.item(row, 0).text()
                    address = self.table_widget.item(row, 1).text()
                    writer.writerow([coin, address])
            self.script_logs.append(f"CSV exported to: {os.path.abspath(file_name)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WalletRecoveryApp()
    window.show()
    sys.exit(app.exec_())
