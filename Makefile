.PHONY: help install build up down logs clean test lint format

# Default target
help:
	@echo "AI Local RAG System - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  install          Install all dependencies (backend + frontend)"
	@echo "  install-backend  Install Python dependencies"
	@echo "  install-frontend Install Node.js dependencies"
	@echo ""
	@echo "Development:"
	@echo "  up               Start all services with Docker Compose"
	@echo "  down             Stop all services"
	@echo "  logs             Show logs from all services"
	@echo "  logs-api         Show API service logs"
	@echo "  logs-web         Show frontend service logs"
	@echo ""
	@echo "Building:"
	@echo "  build            Build all Docker images"
	@echo "  build-api        Build API Docker image"
	@echo "  build-web        Build frontend Docker image"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-backend     Run backend tests"
	@echo "  test-frontend    Run frontend tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting on all code"
	@echo "  lint-backend     Run backend linting"
	@echo "  lint-frontend    Run frontend linting"
	@echo "  format           Format all code"
	@echo "  format-backend   Format backend code"
	@echo "  format-frontend  Format frontend code"
	@echo ""
	@echo "Database:"
	@echo "  db-migrate       Run database migrations"
	@echo "  db-reset         Reset database (WARNING: destroys data)"
	@echo ""
	@echo "Utilities:"
	@echo "  clean            Clean all build artifacts and containers"
	@echo "  shell-api        Open shell in API container"
	@echo "  shell-web        Open shell in frontend container"

# Installation
install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	cd services/api && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd apps/web && npm install

# Development
up:
	@echo "Starting AI Local RAG System..."
	docker-compose up -d

down:
	@echo "Stopping AI Local RAG System..."
	docker-compose down

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-web:
	docker-compose logs -f web

# Building
build:
	@echo "Building all Docker images..."
	docker-compose build

build-api:
	docker-compose build api

build-web:
	docker-compose build web

# Testing
test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	cd services/api && python -m pytest

test-frontend:
	@echo "Running frontend tests..."
	cd apps/web && npm test

# Code Quality
lint: lint-backend lint-frontend

lint-backend:
	@echo "Running backend linting..."
	cd services/api && flake8 app/ && black --check app/ && isort --check-only app/

lint-frontend:
	@echo "Running frontend linting..."
	cd apps/web && npm run lint

format: format-backend format-frontend

format-backend:
	@echo "Formatting backend code..."
	cd services/api && black app/ && isort app/

format-frontend:
	@echo "Formatting frontend code..."
	cd apps/web && npm run format

# Database
db-migrate:
	@echo "Running database migrations..."
	cd services/api && alembic upgrade head

db-reset:
	@echo "WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 5; \
		cd services/api && alembic upgrade head; \
	fi

# Utilities
clean:
	@echo "Cleaning build artifacts..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	cd apps/web && rm -rf .next node_modules
	cd services/api && find . -type d -name __pycache__ -delete

shell-api:
	docker-compose exec api bash

shell-web:
	docker-compose exec web sh

# Health checks
health:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/health || echo "API not healthy"
	@curl -f http://localhost:3000 || echo "Frontend not healthy"
	@curl -f http://localhost:9000/minio/health/live || echo "MinIO not healthy"

# Development with hot reload
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
