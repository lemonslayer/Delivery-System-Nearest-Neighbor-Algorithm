class HashTable:
    def __init__(self,size):
        self.size = size;
        self.hash_table = self.create();

    def create(self):
        return [[] for _ in range(self.size)]

    def insert(self, key, value):
        hash_key = hash(key) % self.size
        bucket = self.hash_table[hash_key]

        for index, record in enumerate(bucket):
            record_key, record_value = record
            if record_key == key:
                bucket[index] = (key, value)
                return True
        bucket.append((key, value))
        return True

    def get(self, key):
        hash_key = hash(key) % self.size
        bucket = self.hash_table[hash_key]

        for index, record in enumerate(bucket):
            record_key, record_value = record
            if record_key == key:
                return record_value

        return None

    def delete(self, key):
        hash_key = hash(key) % self.size
        bucket = self.hash_table[hash_key]

        found = False

        for index, record in enumerate(bucket):
            record_key, record_value = record
            if record_key == key:
                found = True
                break

        if found == True:
            bucket.pop(index)

        return

    def __str__(self):
        return "".join(str(item) for item in self.hash_table)