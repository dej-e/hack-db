import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Mark, Chastisement, Lesson, Commendation, Schoolkid

COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!,',
    'Теперь у тебя точно все получится!',
]


def get_schoolkid(kid_name):
    try:
        return Schoolkid.objects.filter(full_name__contains=kid_name).get()
    except ObjectDoesNotExist:
        print(f'Школьника {kid_name} не найдено в базе')
        exit(2)
    except MultipleObjectsReturned:
        print(f'Неточный запрос, школьников {kid_name} больше одного')
        exit(2)


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    marks.update(points=5)


def remove_chastisements(schoolkid):
    chastisments = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisments.delete()


def get_lesson(year, letter, subject_title):
    return Lesson.objects.filter(
        year_of_study=year,
        group_letter=letter,
        subject__title=subject_title
    ).order_by('date').first()


def create_commendation(schoolkid, subject):
    commendation_text = random.choice(COMMENDATIONS)

    lesson = get_lesson(
        schoolkid.year_of_study,
        schoolkid.group_letter,
        subject
    )
    if lesson:
        Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher,
        )
