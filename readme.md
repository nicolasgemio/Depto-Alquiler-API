# 🏘️ Depto Alquiler API

API desarrollada en **FastAPI** para obtener y administrar publicaciones de alquiler de departamentos de plataformas como **MercadoLibre** y **Argenprop**.

## 🧱 Tecnologías utilizadas

- ⚙️ **API**: [FastAPI](https://fastapi.tiangolo.com/)
- 🛢️ **Base de datos**: SQL Server (Azure)
- 🗄️ **ORM**: SQLAlchemy
- 🧰 **Arquitectura**: MVC (Modelo - Vista - Controlador)

## 📚 Funcionalidades

- 🔎 Búsqueda de departamentos por usuarios autenticados con Google
- 🏷️ Asociaciones de búsquedas con múltiples departamentos (evita duplicados)
- 💬 Reacciones de los participantes (favoritos, rechazos, comentarios)
- 👥 Gestión de participantes dentro de cada búsqueda
- 🧾 Renderizado HTML para vistas web básicas (con Jinja2)

## 🔐 Autenticación

- Inicio de sesión mediante **Google OAuth2**
- Asociación de usuarios a sus búsquedas de manera segura

## 🗄️ Estructura de la base de datos

Modelo relacional basado en SQL Server. Algunas tablas clave:

- `users`
- `searches`
- `departments`
- `search_participants`
- `search_departments` ← tabla intermedia (PK compuesta)
- `participant_reactions`
- `participant_comments`

## 🚀 Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/nicolas-gemio/depto-alquiler-api.git
   cd depto-alquiler-api

Deployar:
docker build -t myapp:latest .
docker tag myapp:latest gemionicolas/scarpdepto:v28
docker push gemionicolas/scarpdepto:v1
