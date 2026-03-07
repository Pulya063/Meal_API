# 🍳 Meal API

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=sqlalchemy&logoColor=white)

**Meal API** — це веб-додаток, який допомагає знайти ідеальний рецепт на основі наявних у вас інгредієнтів. Система використовує **Google Gemini AI** для аналізу продуктів та **TheMealDB API** для отримання детальних інструкцій приготування.

---

## ✨ Можливості

*   🥗 **Розумний пошук**: Введіть список інгредієнтів, а AI запропонує відповідну страву.
*   🔗 **Інтеграція API**: Автоматичний пошук фото, інструкцій та калорійності через зовнішні сервіси.
*   🔐 **Автентифікація**: Безпечна реєстрація та вхід (JWT, хешування паролів).
*   👤 **Особистий кабінет**: Перегляд профілю та історії знайдених рецептів.
*   💾 **Історія**: Всі знайдені страви автоматично зберігаються у вашій базі даних.
*   📱 **Адаптивність**: Зручний інтерфейс для десктопів та мобільних пристроїв.

---

## 🛠️ Технологічний стек

| Категорія | Технології |
| :--- | :--- |
| **Backend** | Python, Flask, Werkzeug |
| **Database** | SQLite, SQLAlchemy, Alembic (міграції) |
| **AI & API** | Google Gemini (google-genai), TheMealDB |
| **Forms & Auth** | Flask-WTF, WTForms, Python-Jose, Passlib |
| **Frontend** | Jinja2 Templates, CSS3 (Custom styles) |

---

## 📂 Структура проекту

```text
Meal_API/
├── alembic/             # 🗄️ Міграції бази даних
├── app/
│   ├── db/              # Моделі (ORM) та конфігурація БД
│   ├── other/           # Сервіси (AI, OAuth) та декоратори
│   ├── router/          # Логіка маршрутів та CRUD операції
│   ├── static/          # 🎨 CSS стилі та зображення
│   ├── templates/       # 📄 HTML шаблони
│   └── main.py          # Точка входу в додаток
├── requirements.txt     # Залежності
├── alembic.ini          # Конфіг Alembic
└── README.md            # Документація
```

---

## 🚀 Встановлення та запуск

### 1. Клонування репозиторію
```bash
git clone <repository_url>
cd Meal_API
```

### 2. Налаштування оточення
Створіть та активуйте віртуальне середовище:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Змінні оточення
Створіть файл `.env` у папці `app/` (або в корені) та додайте ваш ключ:
```env
GEMINI_API_KEY=your_google_api_key_here
```

### 5. База даних
Застосуйте міграції для створення структури БД:
```bash
alembic upgrade head
```

### 6. Запуск
```bash
python app/main.py
```

🎉 **Готово!** Відкрийте браузер за адресою: `http://127.0.0.1:8000`
