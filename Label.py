from DataPack import Principal


class Label:
    def __init__(self, owner, readers):
        self.owner = owner.principal.name
        if isinstance(readers, list):
            read = []
            for r in readers:
                if isinstance(r, Principal):
                    read.append(r.name)
                else:
                    read.append(r.principal.name)
            self.readers = read
        else:
            read = [readers.principal.name]
            self.readers = set(read)

    def can_read(self, principal):
        return principal == self.owner or principal in self.readers

    def add_reader(self, owner, readers):
        if owner == self.owner:
            if readers not in self.readers:
                self.readers.add(readers)
                print(
                    f">>Logic<< Declassified from owner {owner} by adding reader {readers} || o: {self.owner}"
                    f" --> r: {self.readers}")
            else:
                print(f">>Label<< Reader {readers} already existed inside L : {owner, readers}")
            return True
        else:
            raise Exception("Only the Owners can add new readers")

    def remove_reader(self, owner, removed):
        if owner == self.owner:
            self.readers.discard(removed)
        else:
            raise Exception("Only the owners can remove reader")

    def intersect_readers(self, other_label):
        print(f">>logic<< {self} U {other_label}, result {self.readers.intersection(other_label.readers)}")
        return self.readers.intersection(other_label.readers)

    def relabelling(self, label, owner, readers):
        self.owner = owner.principal.name
        read = [readers.principal.name]
        self.readers = set(read)
        # print(f">>Label<< Reset label, o {owner.principal.name}, r {set(read)}")
        return label
