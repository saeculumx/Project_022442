from DataAgent import DataAgent
from DataPack import Principal, Reference, DataPack
from Label import Label


class Auction_House:

    def __init__(self, name):
        self.principal = Principal(name)
        self.da = DataAgent(f"da_{name}")

    def register(self, customer, label):
        re = Label(self, [self, customer])
        if (label.owner and label.readers) != (re.owner and re.readers):
            label = label.relabelling(label, self, self)
        else:
            label = label.remove_reader(self, customer)
        label.add_reader(self.principal.name, self.da.principal.name)
        self.da.add_Data(self.principal.name, customer.principal.name, label)
        return True

    def remove(self, name, target):
        self.da.remove_data_access(name, self.principal, target)
        return True

    def shareWithTrustedPartner(self, name, partner):
        self.da.share_data(name, self.principal, partner)
        return True

    def switch_user_status(self, name, label):
        # print(label.owner,label.readers)
        i = self.da.change_status(self.principal.name, name.principal.name, label)
        print(
            f">>AUC<< Customer {name.principal.name} status have been changed to {i} for {self.principal.name}")
        return i

    def make_reference(self, name, label):
        if self.getUserStatus(name, label):
            ref = Reference(self.principal.name, name.principal.name, True)
            da = DataPack(ref, label)
            return da
        else:
            raise Exception("Reference cannot be made")

    def getUserStatus(self, name, label):
        re = Label(self, [self, name])
        if (label.owner and label.readers) != (re.owner and re.readers):
            label = label.relabelling(label, self, self)
        else:
            label = label.remove_reader(self, name)
        label.add_reader(self.principal.name, self.da.principal.name)
        cus = name.principal.name
        us = self.da.read_Data(cus, self.principal.name)
        return us

    def checkTrusted(self, name, label):
        trusted = self.da.checkTrusted(name, label)
        return trusted

    def check_reference(self, name, label, ref):
        re = Label(self, [self, name])
        if (label.owner and label.readers) != (re.owner and re.readers):
            label = label.relabelling(label, self, self)
        else:
            label = label.remove_reader(self, name)
        label.add_reader(self.principal.name, self.da.principal.name)
        if self.checkTrusted(ref.content.org, label):
            if not self.getUserStatus(name, label):
                self.switch_user_status(name, label)
                return True
            print(f">>AUC<< Customer {name} already high level")
            return False
        print(f">>AUC<< Reference organization {name} not trusted")
        return False
