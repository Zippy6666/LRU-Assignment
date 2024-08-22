from typing import Callable, Any


class LRUCache:
    class _CachedInstance:
        def __init__(self, args: tuple, return_value: Any) -> None:
            self.args = args
            self.return_value = return_value

    def __init__(self, func: Callable, max_: int) -> None:
        self._func: Callable = func
        self._cache_list: list[self._CachedInstance] = []
        self._max: int = max_

    def _is_cached(self, args: tuple) -> tuple[Any, int] | bool:
        for position, instance in enumerate(self._cache_list):
            if set(args) == set(instance.args): # Sets eliminate the order of the args
                return instance.return_value, position
        return False

    def __call__(self, *args) -> Any:
        cached_return_value, position = self._is_cached(self, args)

        return_value = self._func(*args)

        # Insert at first index
        self._cache_list.insert(0, self._CachedInstance(args, return_value))

        return return_value


if __name__ == "__main__":
    import time

    @LRUCache(3)
    def expensive_operation(a, b):
        time.sleep(1)
        return a * b

    expensive_operation(3, 3)
    expensive_operation(3, 3)
    expensive_operation(5, 3)
    expensive_operation(4, 7)
    expensive_operation(6, 1)
    expensive_operation(3, 3)
