# User Management and Authorization API with FastAPI

## Description

This is a RESTful API developed with FastAPI for user management and authorization. It uses MySQL as the database and JWT (JSON Web Tokens) for authentication and authorization. The API provides endpoints for user management, including creating, retrieving, and deleting users, as well as endpoints for login, token verification, and logout.

## Endpoints

![image](https://github.com/user-attachments/assets/680a5350-0de0-41ff-87c1-d0d70ffb01f5)

### User

- **GET** `/api/v1/user/me` - Get current user details.
- **POST** `/api/v1/user/` - Create a new user.
- **DELETE** `/api/v1/user/` - Delete the current user.

### Auth

- **POST** `/api/v1/auth/login` - Login.
- **POST** `/api/v1/auth/verify-token` - Verify token.
- **POST** `/api/v1/auth/logout` - Logout.

### Default

- **GET** `/` - Welcome endpoint.

## Requirements

- Python 3.8+
- FastAPI
- MySQL
- PyJWT
- SQLAlchemy
- Alembic
