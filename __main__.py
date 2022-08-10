from PySide2 import QtWidgets, QtGui
import socket

import server  # DON`T REMOVE

def client():
    filename = 'image.png'
    image_data = b''
    data_received = []
    # connect to the server
    s = socket.socket()
    s.connect(('localhost', 8888))
    while True:
        # receive data from server
        s.sendall(b"next")
        data = s.recv(2048)
        if data:
            data_received.append(data)
        else:
            s.close()
            break
    print(f'{len(data_received)} packages received')

    # indexing received data
    sorted_data = {}
    for i in range(len(data_received)):
        index = i.to_bytes(1, byteorder="big")
        for j in data_received:
            if j.startswith(index):
                sorted_data[i] = j.replace(index, b'', 1)

    # compile data into one byte string
    for i in range(len(sorted_data)):
        image_data = image_data + sorted_data[i]


    # write a file
    with open(filename, 'wb') as f:
        f.write(image_data)

    return filename


def main():
    path = client()
    app = QtWidgets.QApplication([])
    label = QtWidgets.QLabel()
    label.setMinimumSize(100, 100)
    label.setPixmap(QtGui.QPixmap(path))
    label.show()
    app.exec_()


if __name__ == '__main__':
    main()
