# 🎬 Filseries - Movie & Series Tracker (Work in Progress)

This project is a **web application** with an integrated **database** that allows users to keep track of which movies and TV shows they have already watched.  
It also includes a **recommendation system** based on the user's viewing history and preferences.

> ⚠️ **Note:** This application is still under development.  
Some features require a valid **API key** to work properly.

---

## 📌 About the Project

Originally, this project started as a first attempt to build a **large-scale application with a database**. The initial version was developed with little planning and served as a foundation for experimentation.  
The current repository represents a **reorganized and refactored version**, where the database structure, code organization, and overall architecture are being reworked for scalability and maintainability.

---

## 🚀 Features (Planned & Implemented)

- ✅ User **registration, login, and logout** (via `flask-login`)  
- ✅ Track movies and series watched by the user  
- ✅ **Asynchronous search** handled in the backend  
- ✅ Database **title search with pagination** (React-based frontend component)  
- ❌ Initial **Flask-WTF forms** (to be deprecated)  
- ⏳ Improved **recommendation system** based on user preferences  
- ⏳ Full **CSS redesign** (first version was experimental)  
- ⏳ Database refactoring to **MySQL** using **SQLAlchemy ORM**

---

## 🛠️ Tech Stack

**Frontend:**  
- HTML, CSS, JavaScript  
- React (for dynamic components, e.g., search pagination)  
- Bootstrap 5 

**Backend:**  
- Python  
- Flask + Jinja2  
- Flask-Login (authentication)  
- Flask-WTF (to be replaced in future versions)  

**Database:**  
- SQLAlchemy ORM  
- Currently being migrated to **MySQL**  

---

## ⚡ Requirements

To run this project locally, you will need:  
- Python 3.9+  
- Flask  
- SQLAlchemy  
- MySQL (configured with user and database)  
- API key (for full feature support)  

You can install dependencies with:  

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

1. Clone this repository:
   ```bash
   git clone https://github.com/huger6/Filseries.git
   cd Filseries
   ```

2. Set up your environment variables (e.g., .env file) with your API key and database configuration.

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask Application:
    ```bash
    python app.py
    ```

5. Acess the app locally at:
    ```bash
    http://127.0.0.1:5000/
    ```

--- 

## 📅 Roadmap

- [ ] Redesign frontend styles with a modern approach (CSS/React)  
- [ ] Improve recommendation system 
- [ ] Migrate fully to MySQL  
- [ ] Replace Flask-WTF with modern solutions  
- [ ] Add unit and integration tests  

---

## 📖 Notes

- This repository is an **intermediate refactor** of the original project.  
- The aim is to turn a quick first prototype into a **scalable, maintainable application**.  
- Contributions and feedback are welcome as the project evolves.  

