#!/bin/sh

TEXT=$1

curl -k "https://tts.voicetech.yandex.net/tts?format=mp3&quality=hi&platform=web&application=slovari&lang=en_GB" --data-urlencode text="$TEXT" -H 'accept-encoding: identity;q=1, *;q=0' -H 'accept-language: ru,en-US;q=0.8,en;q=0.6,nl;q=0.4' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36' -H 'accept: */*' -H 'referer: https://slovari.yandex.ru/hectic/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/' -H 'cookie: yandexuid=42181751378747851' --compressed -k > $TEXT.mp3

