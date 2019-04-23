from VKinder import VKinderVkontakte, VKinderSearch, VKinderData, VKinderDatabase


def run():
    id = int(input('Введите ID: '))
    token = input('Введите токен: ')

    vkinder_vk = VKinderVkontakte.VKinderVK(age_from=18, age_to=23, id=id, token=token)
    vkinder_vk.authorize_by_token()
    vkinder_vk.get_city_and_sex()

    all_users = vkinder_vk.search_users()
    my_account = vkinder_vk.get_my_profile()

    vkinder_db = VKinderDatabase.VKinderDatabase()

    vkinder_data = VKinderData.VKinderData(id=id, token=token, all_user=all_users)
    vkinder_data.users_with_groups()
    formated_users = vkinder_data.format_users()
    my_account = vkinder_data.format_my_profile(my_account)

    vkinder_search = VKinderSearch.VKinderSearch(my_account, formated_users)

    vkinder_db.insert_many_people(formated_users)
    vkinder_db.insert_one(my_account)

    result = list()
    res = list()
    reccomended_g = vkinder_search.find_with_groups()
    result += reccomended_g
    reccomended_b = vkinder_search.find_with_books()
    result += reccomended_b
    reccomended_m = vkinder_search.find_with_music()
    result += reccomended_m
    reccomended_i = vkinder_search.find_with_interests()
    result += reccomended_i

    for i in result:
        if i not in res:
            res.append(i)

    vkinder_db.insert_many_partners(res)
