from VKinder import VKinderVkontakte, VKinderSearch, VKinderData, VKinderDatabase, VKinderFind
import config
import logging
import vk_api
import datetime
import pymongo


def run():
    try:
        logging.basicConfig(filename="sample.log", level=logging.INFO)
        log = logging.getLogger(' (' + str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + ') '))
        log.info('')
        log.info('\t === Начали работу === \t')
        try:
            token = config.AUTH_PARAMS['TOKEN'] if config.AUTH_PARAMS['TOKEN'] else input('Введите токен: ')
            id = config.AUTH_PARAMS['ID'] if config.AUTH_PARAMS['ID'] else input('Введите ID: ')
            vkinder_vk = VKinderVkontakte.VKinderVK(age_from=config.AUTH_PARAMS['AGE_FROM'],
                                                    age_to=config.AUTH_PARAMS['AGE_TO'], id=id, token=token)
            vkinder_vk.authorize_by_token()
            log.info('Авторизовались в ВК')
        except vk_api.exceptions.ApiError:
            log.warning('Не удалось авторизоваться в ВК!')
            raise vk_api.exceptions.ApiError

        vkinder_vk.get_city_and_sex()
        my_account = vkinder_vk.get_my_profile()
        log.info('Спарсили свой аккаунт')

        all_users = vkinder_vk.search_users()
        log.info('Произвели поиск пользователей')

        vkinder_data = VKinderData.VKinderData(id=id, token=token, all_user=all_users)
        vkinder_data.users_with_groups()
        my_account = vkinder_data.format_my_profile(my_account)
        formated_users = vkinder_data.format_users()
        log.info('Отформатировали данные и получили пользователей с общими группами')

        vkinder_search = VKinderSearch.VKinderSearch(my_account, formated_users)
        vk_find = VKinderFind.VKinderFind()
        result = list()
        res = list()
        log.info('Начали поиск подходящей пары')

        reccomended_g = vkinder_search.find_with_groups()
        counter = 0
        for i in reccomended_g:
            if i not in result:
                result.append(i)
                counter += 1
                if counter == vk_find.groups_percent:
                    break
        log.info('Нашли пользователей с общими группами')

        reccomended_b = vkinder_search.find_with_books()
        counter = 0
        for i in reccomended_b:
            if i not in result:
                result.append(i)
                counter += 1
                if counter == vk_find.books_percent:
                    break
        log.info('Нашли пользователей с общими книгами')

        reccomended_m = vkinder_search.find_with_music()
        counter = 0
        for i in reccomended_m:
            if i not in result:
                result.append(i)
                counter += 1
                if counter == vk_find.music_percent:
                    break
        log.info('Нашли пользователей с общией музыкой')

        reccomended_i = vkinder_search.find_with_interests()
        counter = 0
        for i in reccomended_i:
            if i not in result:
                result.append(i)
                counter += 1
                if counter == vk_find.interests_percent:
                    break
        log.info('Нашли пользователей с общими интересами')

        for i in result:
            if i not in res:
                res.append(i)
        log.info('Избавились от повторов')

        for i in res:
            ph = vkinder_vk.get_top_photo(i['id'])
            i['photos'] = ph
        log.info('Нашли для каждого аккаунта ТОП3 фото')

        try:
            vkinder_db = VKinderDatabase.VKinderDatabase()
            if vkinder_db.vkinder_db.own_account.count_documents({}) == 0:
                vkinder_db.insert_one(my_account)
            if vkinder_db.vkinder_db.all_people.count_documents({}) == 0:
                vkinder_db.insert_many_people(formated_users)
            else:
                alredy_writed_users = vkinder_db.find_all_people()
                new_formated_users = list(filter(lambda x: x not in alredy_writed_users, formated_users))
                if len(new_formated_users) > 0: vkinder_db.insert_many_people(new_formated_users)
            if vkinder_db.vkinder_db.partners.count_documents({}) == 0:
                vkinder_db.insert_many_partners(res)
            else:
                alredy_writed_partners = vkinder_db.find_many_partners()
                new_partners = list(filter(lambda x: x not in alredy_writed_partners, res))
                if len(new_partners) > 0: vkinder_db.insert_many_partners(new_partners)
            log.info('Подключились к БД')
        except pymongo.errors.ServerSelectionTimeoutError:
            log.warning('Ошибка при подключении к БД')
            raise pymongo.errors.ServerSelectionTimeoutError
        vk_find.get_json(result)
        log.info('Записали всё, создали JSON файл')
        log.info('\t === Закончили работу === \t')
    except KeyboardInterrupt:
        log.warning('\t === Прервали досрочно! === \t')
        raise KeyboardInterrupt
