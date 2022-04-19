import time


class AddressData:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.timeStamp = time.time()

    def __str__(self):
        return 'Nome: %s - Mac: %s' % (self.name, self.address)


class AddressBook:

    def __init__(self):
        self.addressData = []

    def includeItem(self, name, address):
        self.addressData = list(
            filter(lambda data: data.address != address, self.addressData))
        self.addressData.append(AddressData(name, address))

    def showData(self):
        for address in self.addressData:
            print(address)

    def updateData(self):
        while True:
            time.sleep(1)
            currentTime = time.time()
            self.addressData = list(
                filter(lambda data: currentTime - data.timeStamp < 15, self.addressData))
