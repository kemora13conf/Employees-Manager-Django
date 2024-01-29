# Project Title

This is a Django-based web application with a JavaScript frontend. The project is structured into three main Django apps: [`Api`](command:_github.copilot.openRelativePath?%5B%22Api%22%5D "Api"), [`Auth`](command:_github.copilot.openRelativePath?%5B%22Auth%22%5D "Auth"), and [`Dashboard`](command:_github.copilot.openRelativePath?%5B%22Dashboard%22%5D "Dashboard").

## Api

The [`Api`](Api) app handles the main functionality of the project. It includes models, views, and templates for the application's core features. The [`models.py`](command:_github.copilot.openSymbolInFile?%5B%22Api%2Fmodels.py%22%2C%22models.py%22%5D "Api/models.py") file contains the database models used in the app. The [`views.py`](command:_github.copilot.openSymbolInFile?%5B%22Api%2Fviews.py%22%2C%22views.py%22%5D "Api/views.py") file contains the views that handle requests and responses. The [`dashboard.html`](command:_github.copilot.openSymbolInFile?%5B%22Api%2Ftemplates%2Fdashboard.html%22%2C%22dashboard.html%22%5D "Api/templates/dashboard.html") is the main template file for the application.

The [`dashboard.js`](command:_github.copilot.openSymbolInFile?%5B%22Api%2Fstatic%2Fdashboard.js%22%2C%22dashboard.js%22%5D "Api/static/dashboard.js") and [`dashboard.css`](command:_github.copilot.openSymbolInFile?%5B%22Api%2Fstatic%2Fdashboard.css%22%2C%22dashboard.css%22%5D "Api/static/dashboard.css") files in the `static` directory are responsible for the frontend functionality and styling of the dashboard.

## Auth

The [`Auth`](Auth) app handles user authentication. It includes models, views, and templates for user registration, login, and logout. The [`models.py`](command:_github.copilot.openSymbolInFile?%5B%22Auth%2Fmodels.py%22%2C%22models.py%22%5D "Auth/models.py") file contains the User model, and the [`views.py`](command:_github.copilot.openSymbolInFile?%5B%22Auth%2Fviews.py%22%2C%22views.py%22%5D "Auth/views.py") file contains the views for authentication.

## Dashboard

The [`Dashboard`](Dashboard) app is responsible for displaying user data on a dashboard. The [`models.py`](command:_github.copilot.openSymbolInFile?%5B%22Dashboard%2Fmodels.py%22%2C%22models.py%22%5D "Dashboard/models.py") file contains the models for the dashboard, and the [`views.py`](command:_github.copilot.openSymbolInFile?%5B%22Dashboard%2Fviews.py%22%2C%22views.py%22%5D "Dashboard/views.py") file contains the views for the dashboard.

## Setup

To set up the project, you need to have Python. Then you can run the virtual environment by running:

```sh
venv\Scripts\activate
```

To run the project, use the Django manage.py script:

```sh
cd Employees_Manager
python manage.py runserver
```

## Database

The project uses SQLite as its database. The database file is [`db.sqlite3`](command:_github.copilot.openSymbolInFile?%5B%22db.sqlite3%22%2C%22db.sqlite3%22%5D "db.sqlite3").

## Styling

The project uses Tailwind CSS for styling. The configuration for Tailwind can be found in the [`tailwind.config.js`](command:_github.copilot.openSymbolInFile?%5B%22tailwind.config.js%22%2C%22tailwind.config.js%22%5D "tailwind.config.js") file.

## Version Control

The project uses Git for version control. The [`.gitignore`](command:_github.copilot.openRelativePath?%5B%22.gitignore%22%5D ".gitignore") file is used to exclude certain files from the repository.

Please note that this is a basic overview of the project. For more detailed information, please refer to the individual files and code comments.
