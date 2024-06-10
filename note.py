import json
import argparse
from datetime import datetime

FILENAME = 'notes.json'

print("Список дооступных команд для работы в заметках: add, list, edit, delete, exit.")


def load_notes():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notes(notes):
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)


def add_note(title, message):
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "Название": title,
        "Текст заметки": message,
        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(note)
    save_notes(notes)
    print("Заметка успешно сохранена.")


def list_notes():
    notes = load_notes()
    for note in notes:
        print(f'{note["id"]}: {note["title"]
                               } - {note["message"]} (Дата: {note["date"]})')


def edit_note(note_id, title, message):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["message"] = message
            note["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print("Заметка обновлена.")
            return
    print("Заметка не найдена.")


def delete_note(note_id):
    notes = load_notes()
    notes = [note for note in notes if note["id"] != note_id]
    save_notes(notes)
    print("Заметка удалена.")


def interactive_mode():
    while True:
        command = input("Введите команду: ")
        if command == "add":
            title = input("Введите заголовок заметки: ")
            message = input("Введите тело заметки: ")
            add_note(title, message)
        elif command == "list":
            list_notes()
        elif command == "edit":
            note_id = int(input("Введите ID заметки: "))
            title = input("Введите новый заголовок заметки: ")
            message = input("Введите новое тело заметки: ")
            edit_note(note_id, title, message)
        elif command == "delete":
            note_id = int(
                input("Введите ID заметки, которую хотите удалить: "))
            delete_note(note_id)
        elif command == "exit":
            print("Выход из программы.")
            break
        else:
            print(
                "Неизвестная команда. Доступные команды: add, list, edit, delete, exit.")


def main():
    parser = argparse.ArgumentParser(
        description="Консольное приложение для управления заметками.")
    parser.add_argument("command", nargs='?', help="Команда для выполнения")
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--msg", help="Текст заметки")
    parser.add_argument("--id", type=int, help="Идентификатор заметки")
    args = parser.parse_args()

    if args.command:
        if args.command == "add" and args.title and args.msg:
            add_note(args.title, args.msg)
        elif args.command == "list":
            list_notes()
        elif args.command == "edit" and args.id and args.title and args.msg:
            edit_note(args.id, args.title, args.msg)
        elif args.command == "delete" and args.id:
            delete_note(args.id)
        else:
            print("Некорректные аргументы команды.")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
