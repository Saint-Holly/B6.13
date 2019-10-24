"""
Модуль запуска web-сервера
с обработкой пути /albums/<artist>

"""
from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        result = "В базе данных {} альбомов {}<br>".format(len(albums_list), artist)
        album_names = [album.album for album in albums_list]
        result += "Список альбомов {}: <br>".format(artist)
        result += ", <br>".join(album_names)
    return result

@route("/albums", method="POST")
@route("/albums/", method="POST")
def new_album():
    if request.forms.get("year") is None or request.forms.get("artist") is None or request.forms.get("genre") is None or request.forms.get("album") is None:
        return HTTPError(400, "Некорректные параметры")
    try: 
        year = int(request.forms.get("year"))
    except:
        result = HTTPError(400, "Некорректные параметр - год записи")
    else:

    #Считаем год валидным, если это целое между 1000 и 3000
        if year > 1000 and year < 3000:
            album_data = {
                "artist": request.forms.get("artist"),
                "genre": request.forms.get("genre"),
                "album": request.forms.get("album"),
                "year": int(request.forms.get("year"))
            }
            result = album.save(album_data)
        if result == "Этот альбом уже есть в базе данных":
            return HTTPError(409, result)

    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
