# Registration Importer
Import osób z programów systemu USOS do rejestracji względem pliku selekcjonującego.
Aplikacja wysyła monity o powodzeniu oraz niepowodzeniu importu.

## Ważne pliki w strukturze:
| Plik | Opis |
| ------ | ------ |
| script.sql | Ten plik zawiera przygotowany wcześniej skrypt SQL, który tworzy importy osób z programu do rejestracji. |
| .env | Plik środowiskowy którego opis / jego poprawne zastosowane przedstawione jest poniżej. |
| mail_patterns.py | Służy do definicji szablonów wysyłania wiadomości, są trzy rodzaje: sukces, wyjątek, nic do roboty. |

## Plik środowiskowy .env
Stwórz plik .env w folderze projektu i uzupełnij poniższe klucze.
```sh
DATABASE_IP=
DATABASE_PORT=
DATABASE_NAME=
INSTANT_CLIENT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DEBUG=False
MAIL_LOGIN=
MAIL_PASSWORD=
MAIL_MONITS_TARGET=
```