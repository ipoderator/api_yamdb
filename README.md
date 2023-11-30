
### :writing_hand: YaMDb- Командный проект  YandexPracticum:


### Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### :hammer_and_wrench:  Стэк технологий:
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- Django - 3.2.16 
- Djangorestframework - 3.12.4
-  Djangorestframework-simplejwt - 4.7.2
- Django-import-export -3.3.3
- Python - 3.11

	[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=ipoderator&layout=compact&theme=vision-friendly-dark)](https://github.com/anuraghazra/github-readme-stats)

### :woman_technologist: Авторы:
<div id="header" align="center">  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>  </div>

- [Алексей Мелентьев](https://github.com/alexeymelentev) - отвечал за систему регистрации и аутентификации, права доступа, работу с токенами и систему подтверждения через e-mail.
- [Константин Пархоц](https://github.com/parchoc) - работал над отзывами, комментариями и рейтингом произведений. 
- [Чуркин Глеб](https://github.com/ipoderator) - реализововал импорт данных из csv файла. Делал модели, view фукнции и эндпоинты для произведений, категорий и жанров.

### Как запустить проект:
<div align="center">  <img src="https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif" width="700" height="400"/>  </div>
Cоздать и активировать виртуальное окружение:

```
git clone git@github.com:ipoderator/api_yamdb.git
```
```
python3.11 -m venv venv 
```
```
. ./venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3.11 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3.11 manage.py migrate
```
Запустить проект:
```
python3.11 manage.py runserver
```
____
Документация будет доступна после запуска проекта по адресу ```/redoc/```
