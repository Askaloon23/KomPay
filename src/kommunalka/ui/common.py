from services.app_service import REPOSITORIES


def read_int(message):
    try:
        return int(input(message))
    except ValueError:
        print("Введите целое число.")
        return None


def show_records(repo_name):
    repo = REPOSITORIES[repo_name]
    records = repo.get_all()

    if not records:
        print("Записей нет.")
        return

    for record in records:
        print(dict(record))


def show_records_for_user(repo_name, user_id):
    repo = REPOSITORIES[repo_name]
    records = repo.get_all()
    found = False

    for record in records:
        data = dict(record)

        if data.get("user_id") == user_id:
            print(data)
            found = True

    if not found:
        print("Записей не найдено.")
