from typing import Callable, Any


class LRUCache:
    class _CachedInstance:
        def __init__(self, args: tuple, return_value: Any) -> None:
            self.args = args
            self.return_value = return_value

        def __repr__(self) -> str:
            return str( self.return_value )

    def __init__(self, max_: int) -> None:
        self._cache_list: list[self._CachedInstance] = []
        self._max: int = max_

    def _is_cached(self, args: tuple) -> tuple[Any, Any]:
        for position, instance in enumerate(self._cache_list):
            if args == instance.args:
                return instance.return_value, position
        return False, False

    def __call__(self, func: Callable, *_) -> Any:
        def wrapper(*args):
            cached_return_value, position = self._is_cached(args)
            if not cached_return_value is False:
                # Move this value to the first position in the list
                self._cache_list[0], self._cache_list[position] = (
                    self._cache_list[position],
                    self._cache_list[0],
                )

                print(self._cache_list)

                # Is cached, so return cached value
                return cached_return_value

            return_value = func(*args)

            # Insert at first index
            self._cache_list.insert(0, self._CachedInstance(args, return_value))
            if len(self._cache_list) > self._max:
                self._cache_list.pop() # Remove last element if cache it too large

            print(self._cache_list)

            return return_value
        return wrapper


if __name__ == "__main__":
    import time

    @LRUCache(3)
    def expensive_operation(a, b):
        time.sleep(2)
        return a * b

    expensive_operation(3, 3)
    expensive_operation(3, 3)
    expensive_operation(5, 3)
    expensive_operation(4, 7)
    expensive_operation(6, 1)
    expensive_operation(3, 3)
