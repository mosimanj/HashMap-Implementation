# Name: Jacob Mosiman
# OSU Email: mosimaja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Portfolio Assignment
# Due Date: 6/6/24
# Description: Contains HashMap implementation using chaining method.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Inserts key/value pair into HashMap. If key already exists, updates the associated value.

        :param key:             String representing the key to be used to access associated value.
        :param value:           Object representing the value to be paired with associated key.

        :return:                None.
        """
        # Resizes table if load factor >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Access the bucket for the specified key. Calculated based on output of hash function.
        bucket = self._get_bucket(key)

        # If the LinkedList contains the key, update its associated value.
        existing_key = bucket.contains(key)
        if existing_key:
            existing_key.value = value
        # If the LinkedList does not contain the key, insert the key/value pair and increment HashMap size.
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes capacity of underlying table. If new_capacity is not prime, moves to next highest prime. If new_capacity
        less than 1, does nothing.

        :param new_capacity:    Integer of new capacity for table. If not prime, updated to next highest prime.

        :return:                None.
        """
        # If less than one, do nothing
        if new_capacity < 1:
            return

        # If new_capacity is not prime, update to next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store capacity and old table, then set capacity to new_capacity
        old_capacity = self._capacity
        old_buckets = self._buckets
        self._capacity = new_capacity

        # Initiate new underlying table (Dynamic Array) and fill each index with an empty LinkedList
        self._buckets = DynamicArray()
        self._size = 0                              # Size reset; incremented per put() call
        for bucket in range(new_capacity):
            self._buckets.append(LinkedList())

        # Put each key/value pair from old buckets to new buckets (with updated capacity)
        for index in range(old_capacity):
            bucket = old_buckets[index]
            for node in bucket:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table (size / capacity).

        :param:         None.

        :return:        None.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :param:         None.

        :return:        Integer representing number of empty buckets in the hash table.
        """
        empty_buckets = 0

        # Check each bucket in table. If empty, increment counter
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str):
        """
        Returns the value associated with the key if the key exists in the HashMap. Otherwise, returns None.

        :param key:     String representing the key whose value is to be returned (if present in HashMap).

        :return:        Object representing the value associated with the given key. None if key not present in HashMap.
        """

        # Access bucket for key
        bucket = self._get_bucket(key)

        # Check each node (key/value pair) in bucket, returning the value associated with specified key (if present)
        for node in bucket:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key exists in the HashMap, returns False otherwise.

        :param key:     String representing the key whose presence is being checked for.

        :return:        Boolean representing if the key is contained in our HashMap. True = exists, False = does not.
        """
        # If get() returns None, the HashMap does not contain the key.
        if self.get(key) is None:
            return False
        # If get() returns a value, the HashMap does contain the key.
        return True

    def remove(self, key: str) -> None:
        """
        Removes the specified key and its associated value if said key exists in the HashMap.

        :param key:     String representing key to be removed from HashMap (along with its associated value).

        :return:        None.
        """
        # Access bucket (LinkedList) hashed to key
        bucket = self._get_bucket(key)

        # Attempt to remove node with matching key. If successful, decrement HashMap size.
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing one Tuple for each key/value pair in the HashMap.

        :param:         None.

        :return:        DynamicArray containing a (key, value) Tuple for each key/value pair in the HashMap.
        """
        keys_and_values = DynamicArray()

        # Iterate through each bucket
        for index in range(self._capacity):
            bucket = self._buckets[index]
            # Iterate through each node in bucket and append a tuple for each key/value pair
            for node in bucket:
                keys_and_values.append((node.key, node.value))
            # Return the DynamicArray once all key/value pairs have been added
            if keys_and_values.length() == self._size:
                return keys_and_values

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing the table's capacity.

        :param:         None.

        :return:        None.
        """
        # Replace each bucket with a fresh (empty) LinkedList
        for index in range(self._capacity):
            self._buckets[index] = LinkedList()

        # Reset size
        self._size = 0

    def _get_bucket(self, key: str) -> LinkedList:
        """
        Uses hash function to calculate index of key and returns the associated bucket (LinkedList).

        :param key:     String representing a key whose bucket we are getting.

        :return:        LinkedList object (bucket) associated with the given key.
        """
        # Calculate index of bucket using hash function, then return that bucket.
        index = self._hash_function(key) % self._capacity
        return self._buckets[index]


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a DynamicArray and returns a tuple containing (mode, frequency). Input does not need to be sorted.

    :param da:          DynamicArray for which the mode and frequency will be found.

    :return:            Tuple containing DynamicArray of mode(s) and integer representing frequency of the mode.
    """
    map = HashMap()

    # Iterate through input array and add element as map key and frequency as its value.
    for index in range(da.length()):
        cur_val = da[index]
        existing_val = map.get(cur_val)
        # If key exists in map, increment its value by 1. Otherwise, add the new key with a value of 1.
        if existing_val:
            map.put(cur_val, existing_val+1)
        else:
            map.put(cur_val, 1)

    # Generate array of tuples in the form (value, frequency)
    val_freq_arr = map.get_keys_and_values()

    # Initialize the return variables
    mode = DynamicArray()
    freq = 0

    # Iterate through the array of tuples and assign the value and frequency to variables
    for index in range(val_freq_arr.length()):
        value = val_freq_arr[index][0]
        cur_freq = val_freq_arr[index][1]
        # If the current value has a higher frequency than current max, replace mode with value and update frequency
        if cur_freq > freq:
            mode = DynamicArray()
            mode.append(value)
            freq = cur_freq
        # If the current value's frequency ties the current max, add value to mode
        elif cur_freq == freq:
            mode.append(value)

    return mode, freq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
