class Hashmap:

    def __init__(self):
        self.size = 100
        self.list = [[] for index in range(self.size)]

    def hash(self, key):
        key_string = str(key).lower()
        hash_value = 5381
        hash_multiplier = 33

        for character in key_string:
            hash_value = (hash_value * hash_multiplier) + ord(character)

        return hash_value % self.size

    def add(self, key, value):
        index = self.hash(key)

        if len(self.list[index]) == 0:
            self.list[index].append([key, value])

        else:

            for key_value_pair in self.list[index]:
                if key == key_value_pair[0]:
                    key_value_pair[1] = value
                    break

            else:
                self.list[index].append([key, value])

    def get(self, key):
        index = self.hash(key)

        if self.list[index]:
            for key_value_pair in self.list[index]:
                if key == key_value_pair[0]:
                    return key_value_pair[1]

        return None

    def remove(self, key):
        index = self.hash(key)

        if self.list[index]:
            for inner_index in range(len(self.list[index])):
                if key == self.list[index][inner_index][0]:
                    self.list[index].remove(inner_index)

        return None

    def clear(self):
        for each_list in self.list:
            each_list.clear()

