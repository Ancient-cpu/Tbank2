import json
import os
DATA_FILE = "library_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []
    return []
def save_data(library):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(library, file, ensure_ascii=False, indent=4)
def print_book(book):
    status = "Прочитана" if book['is_read'] else "Не прочитана"
    fav = "★ Да" if book['is_favorite'] else "☆ Нет"
    print(f"ID: {book['id']} | Название: {book['title']} | Автор: {book['author']} | Год: {book['year']}")
    print(f"Жанр: {book['genre']} | Статус: {status} | В избранном: {fav}")
    print(f"Описание: {book['description']}")
    print("-" * 40)
def add_book(library):
    print("\n--- Добавление новой книги ---")
    title = input("Введите название: ").strip()
    author = input("Введите автора: ").strip()
    genre = input("Введите жанр: ").strip()
    while True:
        year = input("Введите год издания: ").strip()
        if year.isdigit():
            year = int(year)
            break
        print("Ошибка: год должен быть числом.")
    description = input("Введите краткое описание: ").strip()
    new_id = max([b['id'] for b in library], default=0) + 1
    book = {
        "id": new_id,
        "title": title,
        "author": author,
        "genre": genre,
        "year": year,
        "description": description,
        "is_read": False,
        "is_favorite": False
    }
    library.append(book)
    save_data(library)
    print("Книга успешно добавлена!")
def view_books(library):
    if not library:
        print("\nБиблиотека пуста.")
        return
    print("\n--- Просмотр книг ---")
    print("1. Показать все книги")
    print("2. Отсортировать по названию")
    print("3. Отсортировать по автору")
    print("4. Отсортировать по году издания")
    print("5. Фильтр по жанру")
    print("6. Фильтр по статусу (прочитана/не прочитана)")
    choice = input("Выберите действие (1-6): ").strip()
    books_to_show = library.copy()
    if choice == '2':
        books_to_show.sort(key=lambda x: x['title'].lower())
    elif choice == '3':
        books_to_show.sort(key=lambda x: x['author'].lower())
    elif choice == '4':
        books_to_show.sort(key=lambda x: x['year'])
    elif choice == '5':
        genre = input("Введите жанр для фильтрации: ").strip().lower()
        books_to_show = [b for b in books_to_show if b['genre'].lower() == genre]
    elif choice == '6':
        status = input("Показать прочитанные? (да/нет): ").strip().lower()
        is_read_filter = True if status == 'да' else False
        books_to_show = [b for b in books_to_show if b['is_read'] == is_read_filter]
    elif choice != '1':
        print("Неверный выбор. Показываем все книги.")
    print("\nСписок книг:")
    print("=" * 40)
    if not books_to_show:
        print("По вашему запросу книг не найдено.")
    for book in books_to_show:
        print_book(book)
def toggle_favorite(library):
    try:
        book_id = int(input("\nВведите ID книги: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for book in library:
        if book['id'] == book_id:
            book['is_favorite'] = not book['is_favorite']
            save_data(library)
            action = "добавлена в избранное" if book['is_favorite'] else "удалена из избранного"
            print(f"Книга '{book['title']}' {action}!")
            return
    print("Книга с таким ID не найдена.")
def change_status(library):
    try:
        book_id = int(input("\nВведите ID книги для изменения статуса чтения: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for book in library:
        if book['id'] == book_id:
            book['is_read'] = not book['is_read']
            save_data(library)
            status = "Прочитана" if book['is_read'] else "Не прочитана"
            print(f"Ста08тус книги '{book['title']}' изменен на '{status}'.")
            return
    print("Книга с таким ID не найдена.")
def view_favorites(library):
    favorites = [b for b in library if b['is_favorite']]
    print("\n--- Избранные книги ---")
    if not favorites:
        print("У вас пока нет избранных книг.")
        return
    for book in favorites:
        print_book(book)
def delete_book(library):
    try:
        book_id = int(input("\nВведите ID книги для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    for i, book in enumerate(library):
        if book['id'] == book_id:
            deleted_title = book['title']
            del library[i]
            save_data(library)
            print(f"Книга '{deleted_title}' успешно удалена из библиотеки.")
            return
    print("Книга с таким ID не найдена.")
def search_books(library):
    keyword = input("\nВведите ключевое слово для поиска: ").strip().lower()
    found_books = []
    for book in library:
        if (keyword in book['title'].lower() or 
            keyword in book['author'].lower() or 
            keyword in book['description'].lower()):
            found_books.append(book)
    print(f"\n--- Результаты поиска по запросу '{keyword}' ---")
    if not found_books:
        print("Книги не найдены.")
    for book in found_books:
        print_book(book)
def main():
    library = load_data()
    print("Добро пожаловать в приложение 'T-Библиотека'!")
    while True:
        print("\n=== ГЛАВНОЕ МЕНЮ ===")
        print("1. Добавить книгу")
        print("2. Просмотр книг (с фильтрами и сортировкой)")
        print("3. Поиск книги")
        print("4. Изменить статус (Прочитана / Не прочитана)")
        print("5. Добавить/Удалить из избранного")
        print("6. Показать избранные книги")
        print("7. Удалить книгу")
        print("0. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == '1':
            add_book(library)
        elif choice == '2':
            view_books(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            change_status(library)
        elif choice == '5':
            toggle_favorite(library)
        elif choice == '6':
            view_favorites(library)
        elif choice == '7':
            delete_book(library)
        elif choice == '0':
            print("Сохранение данных... До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")
if __name__ == "__main__":
    main()
