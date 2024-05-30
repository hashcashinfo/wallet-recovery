import os
import sys
import re
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMainWindow, QAction, qApp, QCheckBox, QHBoxLayout
import bit
from bit.format import bytes_to_wif

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

def getaddr(wif, network):
    key = bit.Key(wif)
    addr = bit.format.address_to_public_key_hash(key.address)
    if network == 'doge':
        return bit.format.b58encode_check(b'\x1E' + addr)
    if network == 'btc':
        return bit.format.b58encode_check(b'\x00' + addr)
    if network == 'ltc':
        return bit.format.b58encode_check(b'\x30' + addr)
    # return addr

def generate_wifs(secset, is_compressed):
    WIFs = set()
    for seci in secset:
        keyp = bit.Key.from_int(seci)
        wif = bytes_to_wif(keyp.to_bytes(), compressed=is_compressed)
        WIFs.add(wif)
    return WIFs

class WalletRecoveryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wallet Recovery')
        self.setMinimumSize(900, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.script_logs = QTextEdit()
        self.script_logs.setReadOnly(True)
        layout.addWidget(self.script_logs)

        self.checkbox_layout = QHBoxLayout()
        self.btc_checkbox = QCheckBox('Bitcoin')
        self.btc_checkbox.setChecked(True)
        self.doge_checkbox = QCheckBox('Dogecoin')
        self.ltc_checkbox = QCheckBox('Litecoin')
        self.checkbox_layout.addWidget(self.btc_checkbox)
        self.checkbox_layout.addWidget(self.doge_checkbox)
        self.checkbox_layout.addWidget(self.ltc_checkbox)
        layout.addLayout(self.checkbox_layout)

        self.file_select_button = QPushButton('Select Wallet File')
        self.file_select_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_select_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5) 
        self.table_widget.setHorizontalHeaderLabels(['Coin', 'Address', 'WIF', 'Address Uncompressed', 'WIF Uncompressed'])
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
        if file_name and os.path.isfile(file_name):  # Ensure the selected path is a file
            self.recover_wallet(file_name)
        else:
            self.script_logs.append("Selected path is not a valid file. Please select a valid wallet file.")

    def recover_wallet(self, file_name):
        try:
            with open(file_name, 'rb') as f:
                walletbinary = f.read()
        except Exception as e:
            self.script_logs.append(f"Failed to read file: {e}")
            return

        keymetas = extractKeyMetas(walletbinary)
        secrets = extractPrivKeys(walletbinary)

        addresses = []

        if self.btc_checkbox.isChecked():
            btc_wifs = generate_wifs(secrets, True)
            btc_addresses = {wif: getaddr(wif, 'btc') for wif in btc_wifs}
            btc_uncompressed_wifs = generate_wifs(secrets, False)
            btc_uncompressed_addresses = {wif: getaddr(wif, 'btc') for wif in btc_uncompressed_wifs}
            addresses.append(("BTC", btc_addresses, btc_uncompressed_addresses))

        if self.doge_checkbox.isChecked():
            doge_wifs = generate_wifs(secrets, True)
            doge_addresses = {wif: getaddr(wif, 'doge') for wif in doge_wifs}
            doge_uncompressed_wifs = generate_wifs(secrets, False)
            doge_uncompressed_addresses = {wif: getaddr(wif, 'doge') for wif in doge_uncompressed_wifs}
            addresses.append(("Dogecoin", doge_addresses, doge_uncompressed_addresses))

        if self.ltc_checkbox.isChecked():
            ltc_wifs = generate_wifs(secrets, True)
            ltc_addresses = {wif: getaddr(wif, 'ltc') for wif in ltc_wifs}
            ltc_uncompressed_wifs = generate_wifs(secrets, False)
            ltc_uncompressed_addresses = {wif: getaddr(wif, 'ltc') for wif in ltc_uncompressed_wifs}
            addresses.append(("Litecoin", ltc_addresses, ltc_uncompressed_addresses))

        self.script_logs.clear()
        self.script_logs.append(f"Opened file: {os.path.abspath(file_name)}")
        self.script_logs.append(f"There are potentially {len(keymetas)} Keymetas and {len(secrets)} Private Keys in this wallet")

        self.populate_table(addresses)

    def populate_table(self, addresses):
        self.table_widget.setRowCount(0)
        for coin, addr_dict, uncompressed_addr_dict in addresses:
            for wif, address in addr_dict.items():
                uncompressed_wif = [k for k, v in uncompressed_addr_dict.items() if v == address]
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(coin))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(address))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(wif))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(uncompressed_addr_dict[uncompressed_wif[0]] if uncompressed_wif else ""))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(uncompressed_wif[0] if uncompressed_wif else ""))

        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setMinimumSectionSize(150)

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)", options=options)
        if file_name:
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Coin', 'Address Compressed', 'WIF Compressed', 'Address Uncompressed', 'WIF Uncompressed'])
                for row in range(self.table_widget.rowCount()):
                    coin = self.table_widget.item(row, 0).text()
                    address = self.table_widget.item(row, 1).text()
                    wif = self.table_widget.item(row, 2).text()
                    address_uncompressed = self.table_widget.item(row, 3).text()
                    wif_uncompressed = self.table_widget.item(row, 4).text()
                    writer.writerow([coin, address, wif, address_uncompressed, wif_uncompressed])
            self.script_logs.append(f"CSV exported to: {os.path.abspath(file_name)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WalletRecoveryApp()
    window.show()
    sys.exit(app.exec_())
