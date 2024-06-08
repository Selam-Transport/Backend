
---

# Selam Transport - Backend

Welcome to Selam Transport's backend repository! This repository contains the backend codebase for the Selam Transport web application, which is a platform designed to streamline bus transport management.

## Overview

Selam Transport is a comprehensive solution for managing bus transport operations. The backend is responsible for handling the server-side logic, API endpoints, database interactions, and other core functionalities. This backend repository focuses on providing a robust and scalable API using FastAPI.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **MongoDB**: A NoSQL database for storing and managing application data.
- **Motor**: An async MongoDB driver for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: A lightning-fast ASGI server implementation, using `uvloop` and `httptools`.
- **Git**: Git is used for version control, allowing collaborative development and code management.
- **GitHub**: GitHub is utilized as the hosting platform for the codebase and for collaboration among team members.

## Setup Instructions

### Prerequisites

- **Python 3.7+**: Ensure that you have Python installed on your machine.
- **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies.
- **MongoDB**: Ensure that you have MongoDB installed and running on your machine or have access to a MongoDB instance.

### Steps

1. **Clone the Repository**: Clone this repository to your local machine using the following command:
   ```sh
   git clone https://github.com/Selam-Transport/Backend.git
   ```

2. **Navigate to the Project Directory**: Change directory to the project folder:
   ```sh
   cd Backend
   ```

3. **Create and Activate Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

4. **Install Dependencies**: Install the necessary dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```

5. **Configure MongoDB Connection**: Update the MongoDB connection settings in `app/core/config.py` or set the environment variables for MongoDB URI.

6. **Run the Application**: Start the FastAPI server with:
   ```sh
   uvicorn app.main:app --reload
   ```

7. **Access the API Documentation**: Once the server is running, you can access the automatically generated API documentation by visiting:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure

```plaintext
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # Entry point of the application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic models (schemas)
│   ├── crud.py            # CRUD operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py      # API route definitions
│   └── core/
│       ├── config.py      # Configuration settings
│       └── database.py    # Database connection and session
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_main.py
├── .gitignore
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Contributing

We welcome contributions from the community! If you would like to contribute to the development of Selam Transport's backend, please follow these steps:

1. Fork the Repository
2. Create Your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit Your Changes (`git commit -m 'Add some feature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please ensure that your contributions adhere to the project's coding standards and guidelines.

## License

This project is licensed under the [MIT License](LICENSE).

---

