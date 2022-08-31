from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case

    SET_AIRLINE = ListItem()
    GET_RESULT = ListItem()


if __name__ == '__main__':
    print(f'States list: {States.all()}')