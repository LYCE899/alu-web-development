class BaseCaching:
    """ Base caching class """
    def __init__(self):
        self.cache_data = {}

    def print_cache(self):
        """ Prints the cache """
        print("Current cache:")
        for key in self.cache_data.keys():
            print("{}: {}".format(key, self.cache_data.get(key)))


class BasicCache(BaseCaching):
    """ Basic cache class inheriting from BaseCaching """

    def put(self, key, item):
        """ Add an item to the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is not None:
            return self.cache_data.get(key)
        return None


# Example usage:
basic_cache = BasicCache()
basic_cache.put(1, 'A')
basic_cache.put(2, 'B')
basic_cache.put(3, 'C')

print(basic_cache.get(1))  # Output: A
print(basic_cache.get(4))  # Output: None
