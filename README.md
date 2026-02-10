# 🎬 Filseries — Movie & Series Tracker

A **full-stack web application** that lets users track movies and TV shows they've watched, maintain a watchlist, and discover new titles through a recommendation system powered by the **TMDB API**.

> **Note:** A valid [TMDB API key](https://www.themoviedb.org/settings/api) is required for search, title details, and recommendations to work.

---

## 📌 About the Project

Filseries started as a learning project to build a large-scale application with a database. It has since been reorganized and refactored into a clean, modular codebase with a well-defined architecture. The core functionality is complete, with room for future enhancements such as a notification system.

---

## 🚀 Features

### Authentication & User Management
- User **registration and login** with secure password hashing (`bcrypt`)
- **Session management** via `flask-login`
- **Password change** from user profile
- **Username update** with availability check
- **Profile picture** upload and display (stored in database)

### Title Discovery
- **TMDB-powered search** with filters by media type (movies, series, or both)
- **Advanced search filters** — genre, sort order (popularity, rating, title, release date)
- **Title detail page** with poster, backdrop, overview, genres, runtime, seasons (for TV), and IMDB link
- **Home page** showcasing trending, popular, and top-rated movies and TV shows

### Watched & Watchlist
- **Mark movies as watched** with an optional personal rating (0–10)
- **Track series progress** — current season, status (watching, completed, on-hold, dropped), and rating
- **Watchlist** — save titles to watch later; adding a title to watched auto-removes it from the watchlist
- **Infinite scroll** (cursor-based pagination) on both watched and watchlist pages
- **Client-side filtering** by media type (all, movies, series) and multiple sort options
- **Similar titles** and **personalized recommendations** carousels based on watched history

### Other
- **Responsive design** — works on desktop and mobile with an off-canvas navigation menu
- **Custom error handling** for HTTP errors and application-specific exceptions
- **About** and **Privacy Policy** pages

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | HTML, CSS, JavaScript, Bootstrap 5.3, Bootstrap Icons, Font Awesome 6 |
| **Backend** | Python, Flask, Jinja2 |
| **Database** | MySQL via PyMySQL + SQLAlchemy |
| **API** | [TMDB API v3](https://developer.themoviedb.org/docs) (async requests with `aiohttp`) |
| **Auth** | Flask-Login, Flask-Bcrypt |

---

## 📁 Project Structure

```
Filseries/
├── app.py                          # Application entry point
├── config.py                       # Configuration (env vars, DB URI, API key)
├── requirements.txt                # Python dependencies
├── keys.env                        # Environment variables (not committed)
├── keys_example.env                # Example environment variables
├── db_script.sql                   # Database schema reference
│
└── app/
    ├── __init__.py                 # App factory (create_app)
    ├── extensions.py               # Flask extensions (SQLAlchemy, Bcrypt, LoginManager)
    │
    ├── constants/                  # Application-wide constants
    │   ├── app_constants.py        # General constants (current year)
    │   ├── search_constants.py     # Allowed fields for API responses
    │   ├── title_constants.py      # Title validation limits, genres, sort options
    │   ├── user_constants.py       # Username/password rules and patterns
    │   └── watchlist_constants.py  # Watchlist status values
    │
    ├── exceptions/                 # Custom exception hierarchy
    │   ├── base_exceptions.py      # Base MediaError class
    │   ├── auth_exceptions.py      # Register, Login, Auth errors
    │   ├── db_exceptions.py        # Database and table errors
    │   ├── http_exceptions.py      # HTTP access errors
    │   ├── search_exceptions.py    # Search validation errors
    │   ├── titles_exceptions.py    # Title, rating, and type errors
    │   └── watchlist_exceptions.py # Status change errors
    │
    ├── models/                     # SQLAlchemy models
    │   ├── user.py                 # User model with profile picture
    │   ├── titles_seen.py          # Watched movies & series progress
    │   ├── titles_watchlist.py     # Watchlist movies & series
    │   └── notifications.py       # Notification model (future feature)
    │
    ├── routes/                     # Flask Blueprints
    │   ├── auth.py                 # Login, register, profile, password change
    │   ├── main.py                 # Home, about, privacy pages
    │   ├── titles.py               # Search and title detail pages
    │   ├── watched.py              # Watched page and API endpoints
    │   ├── watchlist.py            # Watchlist page and API endpoints
    │   ├── movies.py               # Movie CRUD (seen/watchlist add/remove/update)
    │   ├── series.py               # Series CRUD (progress/watchlist management)
    │   ├── notifications.py        # Notification endpoints (future feature)
    │   └── error_handler.py        # HTTP and custom error handlers
    │
    ├── services/                   # Business logic layer
    │   ├── search_info.py          # TMDB search, title info, batch fetching
    │   ├── api/
    │   │   └── api_info.py         # TMDB API client (async with aiohttp)
    │   └── db/                     # Database queries (raw SQL via SQLAlchemy)
    │       ├── movies.py           # Movie seen/watchlist queries
    │       ├── series.py           # Series progress/watchlist queries
    │       ├── users.py            # User CRUD and profile queries
    │       ├── user_titles.py      # User marks (seen/watchlist status checks)
    │       ├── user_stats.py       # User statistics and recent activity
    │       └── notifications.py    # Notification CRUD queries
    │
    ├── utils/                      # Utility modules
    │   ├── converters.py           # MediaType URL converter (movie/tv)
    │   ├── title_helpers.py        # Shared helpers for watched/watchlist pages
    │   └── valid_next_page.py      # Safe redirect validation
    │
    ├── validations/                # Input validation
    │   ├── auth_validations.py     # Username, password, registration validation
    │   ├── pagination_validations.py # Cursor-based pagination params
    │   ├── title_validations.py    # Title search input validation
    │   └── watchlist_validations.py  # Title ID, rating, status validation
    │
    ├── static/
    │   ├── css/                    # Stylesheets
    │   │   ├── styles.css          # Global styles
    │   │   ├── title-grid.css      # Shared grid layout (watched/watchlist)
    │   │   ├── home.css            # Home page
    │   │   ├── search.css          # Search results page
    │   │   ├── title.css           # Title detail page
    │   │   ├── watched.css         # Watched page overrides
    │   │   ├── watchlist.css       # Watchlist page overrides
    │   │   ├── auth.css            # Login/register forms
    │   │   └── error.css           # Error pages
    │   ├── js/                     # Client-side scripts
    │   │   ├── script.js           # Global JS (navbar, search, notifications)
    │   │   ├── title-grid.js       # Shared infinite scroll and grid logic
    │   │   ├── home.js             # Home page sliders and hero
    │   │   ├── search.js           # Search filtering and sorting
    │   │   ├── title.js            # Title detail page interactions
    │   │   ├── watched.js          # Watched page config
    │   │   ├── watchlist.js        # Watchlist page config
    │   │   ├── auth.js             # Auth form handling
    │   │   └── user.js             # Profile page interactions
    │   ├── icons/                  # Favicon and web manifest
    │   └── img/                    # Images and logo
    │
    └── templates/                  # Jinja2 templates
        ├── base.html               # Base layout (navbar, footer, flash messages)
        ├── auth/                   # Login, register, profile, change password
        ├── main/                   # Home, about, privacy
        ├── titles/                 # Search results, title detail
        ├── watched/                # Watched page
        ├── watchlist/              # Watchlist page
        └── error-handler/          # Error pages
```

---

## ⚡ Requirements

- **Python** 3.9+
- **MySQL** server with a database created
- **TMDB API key** — [get one here](https://www.themoviedb.org/settings/api)
- **requirements.txt**

---

## ▶️ Running the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/huger6/Filseries.git
   cd Filseries
   ```

2. **Create a MySQL database:**
   ```sql
   CREATE DATABASE filseries;
   ```

3. **Set up environment variables** — copy `keys_example.env` to `keys.env` and fill in your values:
   ```env
   SECRET_KEY=your-secret-key
   DATABASE_URI=mysql+pymysql://root:your-password@localhost:3306/filseries
   TMDB_API_KEY=your-tmdb-api-key
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in your browser:**
   ```
   http://127.0.0.1:5000/
   ```

   Database tables are created automatically on first run.

---

## � Building a Standalone Executable

You can package Filseries into a single-file executable (`.exe` on Windows, binary on Linux/macOS) using [PyInstaller](https://pyinstaller.org/). This allows running the app without a separate Python installation.

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the executable

> **Important:** The `--add-data` flag uses a different separator depending on the OS:
> - **Windows** → semicolon `;`
> - **Linux / macOS** → colon `:`

**Windows:**

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "app/static;app/static" --add-data "app/templates;app/templates" --add-data "keys.env;." app.py
```

**Linux / macOS:**

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "app/static:app/static" --add-data "app/templates:app/templates" --add-data "keys.env:." app.py
```

| Flag | Purpose |
|------|---------|
| `--noconfirm` | Overwrite the output directory without asking |
| `--onefile` | Bundle everything into a single executable |
| `--windowed` | Suppress the console window on launch (Windows) |
| `--add-data` | Include non-Python files (templates, static assets, env) |

### 3. Run the executable

After the build completes, the executable will be located in the `dist/` folder:

```
dist/
└── app.exe        # Windows
└── app             # Linux / macOS
```

Simply run the executable — it behaves the same as `python app.py`. Make sure a MySQL server is accessible with the connection details specified in your `keys.env`.

> **Note:** The `keys.env` file is bundled inside the executable. If you need to change environment variables, you must rebuild the executable.

---

## �🔮 Future Enhancements

- **Notifications** — the data model and database layer are ready; route implementation and frontend integration are pending
- **Unit and integration tests**

---

## 📄 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.  

