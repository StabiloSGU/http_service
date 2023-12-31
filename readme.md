<h1>Http_service csv processing app</h1>

Это простое приложение, позволяющее загружать, просматривать и удалять csv файлы.
Написано на django + drf, так как это прототип, применение стилей и js минимальные.
Js самый простой, без использования сторонних библиотек.

Инструкции по установке и использованию:

Проект состоит из приложения django http_service И нескольких модулей:
Состав:
user_service - отвечает за управление пользователями
csv_import - отвечает за загрузку и взаимодействие с csv файлами, а также их отображение в браузере
csv_import_api - выход на основной CRUD функционал

Установка:
В корне проекта находится файл Dockerfile
При установленном docker достаточно из папки проекта выполнить команду build . -t "desired_name"
Затем запустить контейнер, указав желаемый порт.
При условии, что выбран порт 8000, в адресной строке браузера следует перейти на 127.0.0.1:8000/csv_import

Если docker не установлен, достаточно запустить в корне проекта команду python manage.py runserver (или python3...)

Обзор:
По адресу 127.0.0.1:8000/admin находится админка django с созданным суперюзером admin/admin
Создание пользователей оставлено на админа, а их авторизация и выход выведены на точки
127.0.0.1:8000/user_service/login/ и 127.0.0.1:8000/user_service/logout

Пользовательская подсистема минимальная, добавлена как заготовка для расширения. Сейчас она только препятствует загрузке
нового файла через браузер.

По адресу 127.0.0.1:8000/csv_import/uploads/add доступна форма загрузки csv файла.
При загрузке необходимо указать способ загрузки: в базу данных или в хранилище на сервер.

Тестовые файлы доступны в каталоге http_service\csv_import\test_csv_files
При запуске Python manage.py test тест проверит успешную загрузку каждого файла из этого каталога и валидацию формы.

После загрузки файла, записи добавляются на страницу-список 127.0.0.1:8000/csv_import/
При переходе по ссылке загруженного файла
127.0.0.1:8000/csv_import/uploads/edit/"id" отображается информация о файле: заголовки, возможные типы данных и первая
строка данных для ознакомления. Здесь же возможно удаление файла.

Детальный просмотр файла доступен на странице 127.0.0.1:8000/csv_import/uploads/detail/"id"
На странице реализована сортировка по нажатию на заголовок (включая вложенную сортировку сразу по нескольким столбцам) и
поиск, через ввод подстроки в поле ввода над заголовками и нажатия enter.

Применение поиска не сбрасывает предыдущего отбора и сортировки.

API:
По адресам
127.0.0.1:8000/csv_import_api/v1/uploads_list/
127.0.0.1:8000/csv_import_api/v1/uploads_list/view/"id"
127.0.0.1:8000/csv_import_api/v1/uploads_list/delete/"id"
127.0.0.1:8000/csv_import_api/v1/uploads_list/create/

Доступны эндпоинты для просмотра всего списка файлов, конкретного файла, удаления конкретного файла и загрузки нового.
Просмотр файла также выводит информацию по колонкам по аналогии с 127.0.0.1:8000/csv_import/uploads/edit/"id"
