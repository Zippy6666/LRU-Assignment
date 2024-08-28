from typing import Callable, Any


class LRUCache:
    max = 50

    class _CachedReturnValue:
        def __init__(self, args: tuple, return_value: Any) -> None:
            self.args = args
            self.return_value = return_value

        def __repr__(self) -> str:
            return str(self.return_value)

    def __init__(self, func: Callable) -> None:
        """My half-decent LRU-cache. Only caches return-values by functions that have the same positional arguments (in the same order). The cache is limited to 50 return-values."""
        self._func = func
        self._cache_list: list[self._CachedReturnValue] = []

    def _is_cached(self, args: tuple) -> tuple[Any, Any]:
        for position, instance in enumerate(self._cache_list):
            if args == instance.args:
                return instance.return_value, position
        return False, False

    def __call__(self, *args, **_) -> Any:
        cached_return_value, position = self._is_cached(args)

        if not cached_return_value is False:
            # Move this value to the first position in the list
            self._cache_list[0], self._cache_list[position] = (
                self._cache_list[position],
                self._cache_list[0],
            )

            print(self)
            return cached_return_value  # Is cached, so return cached value

        return_value = self._func(*args)

        # Insert at first index
        self._cache_list.insert(0, self._CachedReturnValue(args, return_value))
        if len(self._cache_list) > self.max:
            self._cache_list.pop()  # Remove last element if cache is larger than max

        print(self)
        return return_value

    def __repr__(self) -> str:
        return "LRU CACHE: " + str(self._cache_list)
