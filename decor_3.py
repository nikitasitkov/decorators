import os
from datetime import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(
                    f'{datetime.now()} | '
                    f'function: {old_function.__name__} | '
                    f'args: {args} | '
                    f'kwargs: {kwargs} | '
                    f'result: {result}\n'
                )

            return result

        return new_function

    return __logger


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    @logger('iterator.log')
    def __iter__(self):
        self.outer = 0
        self.inner = 0
        return self

    @logger('iterator.log')
    def __next__(self):
        while self.outer < len(self.list_of_list) and self.inner >= len(self.list_of_list[self.outer]):
            self.outer += 1
            self.inner = 0

        if self.outer >= len(self.list_of_list):
            raise StopIteration

        item = self.list_of_list[self.outer][self.inner]
        self.inner += 1
        return item


def test_1():

    path = 'iterator.log'
    if os.path.exists(path):
        os.remove(path)

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert os.path.exists(path), 'файл iterator.log должен существовать'

    with open(path, encoding='utf-8') as log_file:
        log_file_content = log_file.read()

    assert '__iter__' in log_file_content
    assert '__next__' in log_file_content
    assert 'a' in log_file_content
    assert 'False' in log_file_content
    assert 'None' in log_file_content


if __name__ == '__main__':
    test_1()