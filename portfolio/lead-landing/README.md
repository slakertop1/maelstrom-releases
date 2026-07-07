# 🌐 Лендинг с приёмом заявок в Telegram

Демо-проект: продуктовый лендинг (вымышленный сервис онлайн-записи «TimeSlot»)
с рабочей формой заявки. Каждый лид сохраняется в базу и **мгновенно приходит
владельцу в Telegram** — без CRM, почтовых серверов и платных сервисов.

Стек: **FastAPI · SQLite · чистые HTML/CSS/JS** (без фреймворков и сборки).
Разворачивается на любом VPS одной командой.

## Что внутри

- **Лендинг**: адаптивная вёрстка (десктоп/планшет/телефон), секции
  «возможности / как работает / тарифы / FAQ / форма» — без единой картинки,
  быстрая загрузка, чистый CSS без фреймворков.
- **Форма заявки**: валидация на клиенте и сервере (Pydantic), отправка без
  перезагрузки страницы, понятные сообщения об ошибках.
- **Анти-спам**: honeypot-поле против ботов + ограничение частоты заявок с
  одного IP (5 за 10 минут).
- **Уведомления**: заявка прилетает в ваш Telegram через Bot API за секунду.
- **База**: все лиды в SQLite (`data/leads.db`) — ничего не теряется, даже
  если Telegram недоступен.

## Быстрый старт

1. Создайте бота у [@BotFather](https://t.me/BotFather) (`/newbot`) — получите токен.
2. Напишите своему боту `/start` и узнайте свой chat ID у [@userinfobot](https://t.me/userinfobot).
3. Настройте окружение:

```bash
cp .env.example .env   # впишите BOT_TOKEN и ADMIN_CHAT_ID
```

### Вариант А — Docker

```bash
docker compose up -d --build
# сайт на http://localhost:8000
```

### Вариант Б — вручную

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Настройка

| Переменная | Описание |
|---|---|
| `BOT_TOKEN` | токен бота от @BotFather |
| `ADMIN_CHAT_ID` | ваш Telegram ID — куда слать заявки |
| `DB_PATH` | путь к базе SQLite (по умолчанию `data/leads.db`) |

Если `BOT_TOKEN` не задан, форма всё равно работает — лиды просто копятся в базе.

## Продакшен

За реверс-прокси (nginx/Caddy) с HTTPS:

```caddy
# Caddyfile — HTTPS автоматически
yourdomain.ru {
    reverse_proxy localhost:8000
}
```

Посмотреть накопленные лиды:

```bash
sqlite3 data/leads.db "SELECT created_at, name, contact, message FROM leads ORDER BY id DESC LIMIT 20;"
```

## Структура

```
app/main.py        # FastAPI: статика + POST /api/lead + Telegram-уведомления
static/index.html  # лендинг
static/style.css   # стили (чистый CSS, адаптив)
static/script.js   # отправка формы без перезагрузки
```

## Под вашу задачу

Контент лендинга — вымышленный продукт для демонстрации. Под ваш бизнес
меняются тексты, цвета и услуги; форма и доставка лидов в Telegram уже готовы.
Нужен такой сайт? Пишите: [github.com/slakertop1](https://github.com/slakertop1)

## Лицензия

MIT — см. [LICENSE](LICENSE).
