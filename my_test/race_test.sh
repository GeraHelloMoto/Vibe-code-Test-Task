#!/bin/bash
# Проверка гонки при взятии заявки
# Предполагается, что сервер запущен и заявка с id=2 назначена на мастера с id=2 (из сидов)

echo "Проверка гонки: отправляем два параллельных запроса на взятие заявки 2 мастером 2"

do_curl() {
    curl -s -X PATCH "http://localhost:8000/api/master/requests/2/take?master_id=2" -w " %{http_code}\n"
}

do_curl &
do_curl &
wait