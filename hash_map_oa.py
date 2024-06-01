# Name: Jacob Mosiman
# OSU Email: mosimaja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Portfolio Assignment
# Due Date: 6/6/24
# Description: Contains HashMap implementation using open addressing method.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # Resize table if load factor >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Target first inactive element or active element with matching key
        target_ind = self._find_index(key, "add")
        target = self._buckets[target_ind]

        # If key exists and is active, update value
        if target and not target.is_tombstone:
            target.value = value
        # Otherwise, insert key/value at first inactive element
        else:
            self._buckets[target_ind] = HashEntry(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes capacity of underlying table. If new_capacity is not prime, moves to next highest prime. If new_capacity
        less than current number of elements in hash map, does nothing.

        :param new_capacity:    Integer of new capacity for table. If not prime, updated to next highest prime.

        :return:                None.
        """
        # If new capacity less than current # of elements, do nothing
        if new_capacity < self._size:
            return

        # If new capacity not prime, increment to next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store pre-call table and capacity
        old_buckets = self._buckets
        old_capacity = self._capacity

        # Update capacity to new capacity, then reset buckets and size
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0

        # Scale up table to capacity (filled with None initially)
        for bucket in range(self._capacity):
            self._buckets.append(None)

        # For each active HashEntry in old_buckets, put into buckets (rehash)
        for ind in range(old_capacity):
            entry = old_buckets[ind]
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)

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
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the key if the key exists in the HashMap. Otherwise, returns None.

        :param key:     String representing the key whose value is to be returned (if present in HashMap).

        :return:        Object representing the value associated with the given key. None if key not present in HashMap.
        """
        # Access element at index holding key or first empty element
        target = self._buckets[self._find_index(key, "search")]

        # If index held an entry, return its value - otherwise key not present
        if target:
            return target.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key exists in the HashMap, returns False otherwise.

        :param key:     String representing the key whose presence is being checked for.

        :return:        Boolean representing if the key is contained in our HashMap. True = exists, False = does not.
        """
        # If get() returns a value, key exists - otherwise it does not
        if self.get(key) is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the specified key and its associated value if said key exists in the HashMap.

        :param key:     String representing key to be removed from HashMap (along with its associated value).

        :return:        None.
        """
        # Access element at index holding key or first empty element
        target = self._buckets[self._find_index(key, "search")]

        # If index held an entry, 'delete' by activating tombstone status and decrement size
        if target:
            target.is_tombstone = True
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing one Tuple for each key/value pair in the HashMap.

        :param:         None.

        :return:        DynamicArray containing a (key, value) Tuple for each key/value pair in the HashMap.
        """
        # Initialize return array and counter (tracks # of key/value pairs added to array)
        keys_and_values = DynamicArray()
        counter = 0

        # Loop through and evaluate each element in buckets
        for index in range(self._capacity):
            cur_element = self._buckets[index]
            # If element holds an active entry, add to return array and increment counter
            if cur_element and not cur_element.is_tombstone:
                keys_and_values.append((cur_element.key, cur_element.value))
                counter += 1
            # Return array once all active key/value pairs have been added
            if counter == self._size:
                return keys_and_values

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing the table's capacity.

        :param:         None.

        :return:        None.
        """
        # Replace each bucket with None
        for index in range(self._capacity):
            self._buckets[index] = None

        self._size = 0

    def __iter__(self):
        """
        Iterator that allows HashMap to iterate across itself. Only active key/value pairs are iterable.

        :param:         None.

        :return:        self.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Obtains next active key/value pair in the HashMap and advances the iterator.
        """
        # Try moving forward until reaching active entry, unless reached end of buckets (exception)
        try:
            entry = self._buckets[self._index]

            while not entry or entry.is_tombstone:
                self._index += 1
                entry = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        # Increment index for next iteration, return current entry (key/value pair)
        self._index += 1
        return entry

    def _find_index(self, key: str, operation: str = "search") -> int:
        """
        Receives a key, applies the hash function, and returns the first index with a matching key or inactive element.
        If operation is 'add' will stop if tombstone encountered, if 'search' will continue past tombstones.

        :param key:         String representing key to be hashed / index found for.
        :param operation:   String representing whether operation is 'add' (put) or 'search' (get/remove).

        :return:            Integer representing first index with a matching key or inactive element.
        """
        # Init number receiving quadratic to 1, calculate initial index, and create pointer to element at that index
        exp_base = 1
        orig_ind = self._hash_function(key) % self._capacity
        ind = orig_ind                  # Inits ind for 'no collision' case
        cur_entry = self._buckets[orig_ind]

        # Loop until we find empty element, inactive element, or an element with a matching key (add)
        if operation == "add":
            while cur_entry and not cur_entry.is_tombstone and cur_entry.key != key:
                ind = orig_ind              # resetting to original index calc each pass
                # Apply quadratic probing with each loop - modulo to wrap around if new ind exceeds table
                ind = ind + (exp_base ** 2)
                exp_base += 1

                if ind >= self._capacity:
                    ind = ind % self._capacity

                cur_entry = self._buckets[ind]

        # Loop until reach empty element or active entry with matching key is found (get or remove)
        else:
            while cur_entry:
                if cur_entry.key == key and not cur_entry.is_tombstone:
                    return ind

                ind = orig_ind
                ind = ind + (exp_base ** 2)
                exp_base += 1

                if ind >= self._capacity:
                    ind = ind % self._capacity

                cur_entry = self._buckets[ind]

        return ind


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
