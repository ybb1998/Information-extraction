from ontology import URI_PATH


def get_question_type(question):
    question = question[:len(question) - 1]
    first_word = question.split(' ')[0]
    second_word = question.split(' ')[1]
    if first_word == 'Who':
        second_word = question.split(' ')[1]
        if second_word == 'directed' or second_word == 'produced':
            return 1, query_for_1_2(question)
        elif second_word == 'starred':
            return 6, query_for_6(question)
        else:
            print("not a valid question")
            exit(1)

    elif first_word == 'Is':
        return 3, query_for_3(question)

    elif first_word == 'When':
        relation = question.split(' ')[-1]
        if relation == 'released':
            return 4, query_for_4(question)
        else:
            return 8, query_for_8(question)

    elif first_word == 'How' and second_word == 'long':
        return 5, query_for_5(question)

    elif first_word == 'Did':
        return 7, query_for_7(question)

    elif first_word == 'What':
        return 9, query_for_9(question)

    elif first_word == 'How':
        if 'based on' in question:
            return 10, query_for_10(question)
        elif 'academy award' in question:
            return 11, query_for_11(question)
        else:
            return 12, query_for_12(question)
    else:  # added question
        return 13, query_for_13(question)


def query_for_1_2(question):
    relation = question.split(" ")[1]
    film_with_spaces = question.split(" ", 2)[2]
    film = film_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{film}> <{URI_PATH}{relation}_by> ?e. }}"
    return query


def query_for_3(question):
    film_with_spaces = question.split(" based on a book")[0]
    film_with_spaces = film_with_spaces.split("Is ", 1)[1]
    film = film_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{film}> <{URI_PATH}based_on> ?e. }}"
    return query


def query_for_4(question):
    entity_with_spaces = question.split("When was ")[1]
    entity_with_spaces = entity_with_spaces.split(" released")[0]
    entity = entity_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{entity}> <{URI_PATH}released_on> ?e. }}"
    return query


def query_for_5(question):
    film_with_spaces = question.split(" ", 3)[3]
    film = film_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{film}> <{URI_PATH}running_time> ?e. }}"
    return query


def query_for_6(question):
    film_with_spaces = question.split(" ", 3)[3]
    film = film_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{film}> <{URI_PATH}starring> ?e. }}"
    return query


def query_for_7(question):
    film_with_spaces = question.split(" star in ")[1]
    film = film_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    entity_with_spaces = question.split(" star in ")[0]
    entity_with_spaces = entity_with_spaces.split(" ", 1)[1]
    entity = entity_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"ASK WHERE {{ <{URI_PATH}{film}> <{URI_PATH}starring> <{URI_PATH}{entity}>. }}"
    return query


def query_for_8(question):
    entity_with_spaces = question.split("When was ", 1)[1]
    entity_with_spaces = entity_with_spaces.split(" born")[0]
    entity = entity_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{entity}> <{URI_PATH}born> ?e. }}"
    return query


def query_for_9(question):
    entity_with_spaces = question.split("of ", 1)[1]
    entity = entity_with_spaces.replace(" ", "_") # keep if URI is with underscore
    query = f"SELECT * WHERE {{ <{URI_PATH}{entity}> <{URI_PATH}occupation> ?e. }}"
    return query


def query_for_10(question):
    query = f"SELECT ?e WHERE {{ ?e <{URI_PATH}based_on> ?book. }}"
    return query


def query_for_11(question):
    entity_with_spaces = question.split("starring ", 1)[1]
    entity_with_spaces = entity_with_spaces.split(" won an")[0]
    entity = entity_with_spaces.replace(" ", "_")  # keep if URI is with underscore
    query = f"SELECT ?e WHERE {{ ?e <{URI_PATH}starring> <{URI_PATH}{entity}>. }}"
    return query


def query_for_12(question):
    occupations = question.split("many ", 1)[1]
    occ1_with_spaces = occupations.split(" are also ")[0]
    occ2_with_spaces = occupations.split(" are also ")[1]
    occ1 = occ1_with_spaces.replace(" ", "_")
    occ2 = occ2_with_spaces.replace(" ", "_")
    query = f"SELECT * WHERE {{ ?person <{URI_PATH}occupation> <{URI_PATH}{occ1}>." \
            f" ?person <{URI_PATH}occupation> <{URI_PATH}{occ2}>. }}"
    return query


def query_for_13(question):
    temp = question.split("In which movies did ")[1]  # result: <entity1> and <entity2> star in together
    star1_with_spaces = temp.split(" and ")[0]  # result: entity1 with spaces
    star2_with_spaces = temp.split(" and ")[1]  # result: <entity2> star in together
    star2_with_spaces = star2_with_spaces.split(" star in")[0]  # result: entity2 with spaces
    star1 = star1_with_spaces.replace(" ", "_")  # result: entity1
    star2 = star2_with_spaces.replace(" ", "_")  # result: entity2
    query = f"SELECT * WHERE {{ ?movie <{URI_PATH}starring> <{URI_PATH}{star1}>." \
            f" ?movie <{URI_PATH}starring> <{URI_PATH}{star2}>. }}"
    return query
