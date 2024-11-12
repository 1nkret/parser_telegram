def read_category_prompt():
    with open("prompts/test_get_category.txt", "r") as file:
        get_category_prompt = file.read()
        return get_category_prompt


def read_title_prompt():
    with open("prompts/get_title.txt", "r") as file:
        get_title_prompt = file.read()
        return get_title_prompt
