from datacenter.models import Schoolkid, Lesson, Subject, Chastisement, Commendation, Mark
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import random


def get_kid(name):
    return Schoolkid.objects.get(full_name__contains=name)


def get_marks(kid):
    return Mark.objects.filter(schoolkid=kid)


def get_bad_marks(kid):
    return get_marks(kid).filter(points__lt=4)


def fix_marks(marks):
    for mark in marks:
        mark.points = random.choice([4,5])
        mark.save()


def get_chastisements(kid):
    return Chastisement.objects.filter(schoolkid=kid)


def remove_chastisements(chastisements):
    chastisements.delete()


def get_lessons(title, year=6, letter="А"):
    return Lesson.objects.filter(
        subject__title__contains=title, 
        subject__year_of_study=year,
        group_letter=letter
    ).order_by("date")


def create_commendation(kid_name, lesson_title):
    kid = get_kid(kid_name)
    lesson = random.choice(get_lessons(lesson_title))
    Commendation.objects.create(
        text = random.choice(commendations),
        created = lesson.date,
        schoolkid = kid,
        subject = lesson.subject,
        teacher = lesson.teacher,
    )


commendations = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!"
]


def main():
    try:
        name = input("Введите имя: ")
        kid = get_kid(name)
        badmarks = get_bad_marks(kid)
        fix_marks(badmarks)
        remove_chastisements(get_chastisements(kid))
        lesson_title = input("Введите имя предмета: ")
        create_commendation(name, lesson_title)

    except MultipleObjectsReturned as e:
        print("Найдено несколько учеников, уточните запрос")
    except ObjectDoesNotExist as e:
        print("Имя не найдено")


if __name__ == "__main__":
    main()