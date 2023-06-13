import utils


def main():
    """Задает алгоритм выполнения программы"""
    data = {}

    user_request = input('Введите, интересующий Вас, товар\n')
    formatted_user_request = user_request.replace(' ', '+')
    sort_type = input('Введите тип сортировки. Доступные варианты:'
                      ' по умолчанию, сначала дешевле, сначала дороже, по дате\n')

    sort_type_code = utils.get_sorting_type(sort_type)

    for page in range(1, 999):
        soup = utils.get_soup_data(page, formatted_user_request, sort_type_code)

        if utils.check_last_page(soup) is False:
            break

        ads = soup.find_all('div',
                            class_='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH '
                                   'iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih '
                                   'items-listItem-Gd1jN js-catalog-item-enum')

        for i in range(len(ads)):
            utils.get_data_from_ad(data, i, ads[i], page)

    ads_data = utils.get_processed_data(data)

    utils.save_to_csv(ads_data)


if __name__ == "__main__":
    main()
