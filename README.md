# Bcommune AI Assistant

Enterprise internal AI assistant for Bcommune employees.

## Stack

- Frontend: React + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI
- Database: Supabase PostgreSQL + pgvector
- AI Engine: Google Colab + Mistral-7B-Instruct-v0.3
- Authentication: JWT
- Authorization: RBAC

## Architecture

User -> React Frontend -> FastAPI Backend -> Internal API Key -> Google Colab AI Engine -> Supabase pgvector