#!/usr/bin/env python3
"""
Verification script for AI Local RAG System
Checks that all core files exist and project structure is complete
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Define the project root
PROJECT_ROOT = Path(__file__).parent.parent

# Core files that must exist
CORE_FILES = [
    # Root level files
    "README.md",
    "PROJECT_BRIEF.md",
    "docker-compose.yml",
    "Makefile",
    ".gitignore",
    
    # Backend files
    "services/api/main.py",
    "services/api/requirements.txt",
    "services/api/Dockerfile",
    "services/api/env.example",
    "services/api/init.sql",
    
    # Backend app structure
    "services/api/app/__init__.py",
    "services/api/app/core/config.py",
    "services/api/app/core/database.py",
    "services/api/app/core/security.py",
    "services/api/app/core/celery.py",
    
    # Backend models
    "services/api/app/models/__init__.py",
    "services/api/app/models/user.py",
    "services/api/app/models/collection.py",
    "services/api/app/models/document.py",
    "services/api/app/models/chat.py",
    "services/api/app/models/connector.py",
    "services/api/app/models/evaluation.py",
    "services/api/app/models/audit.py",
    "services/api/app/models/system.py",
    
    # Backend schemas
    "services/api/app/schemas/__init__.py",
    "services/api/app/schemas/auth.py",
    "services/api/app/schemas/collection.py",
    "services/api/app/schemas/document.py",
    "services/api/app/schemas/chat.py",
    "services/api/app/schemas/connector.py",
    "services/api/app/schemas/evaluation.py",
    "services/api/app/schemas/common.py",
    
    # Backend services
    "services/api/app/services/__init__.py",
    "services/api/app/services/auth_service.py",
    "services/api/app/services/collection_service.py",
    "services/api/app/services/document_service.py",
    "services/api/app/services/chat_service.py",
    "services/api/app/services/connector_service.py",
    "services/api/app/services/evaluation_service.py",
    "services/api/app/services/rag_service.py",
    "services/api/app/services/file_service.py",
    "services/api/app/services/embedding_service.py",
    "services/api/app/services/system_service.py",
    
    # Backend API endpoints
    "services/api/app/api/__init__.py",
    "services/api/app/api/v1/__init__.py",
    "services/api/app/api/v1/auth.py",
    "services/api/app/api/v1/collections.py",
    "services/api/app/api/v1/documents.py",
    "services/api/app/api/v1/chat.py",
    "services/api/app/api/v1/connectors.py",
    "services/api/app/api/v1/admin.py",
    "services/api/app/api/v1/api.py",
    
    # Frontend files
    "apps/web/package.json",
    "apps/web/next.config.js",
    "apps/web/tailwind.config.js",
    "apps/web/tsconfig.json",
    "apps/web/Dockerfile",
    "apps/web/env.example",
    
    # Frontend app structure
    "apps/web/app/layout.tsx",
    "apps/web/app/page.tsx",
    "apps/web/app/globals.css",
    
    # Frontend components
    "apps/web/components/ui/button.tsx",
    "apps/web/components/ui/input.tsx",
    "apps/web/components/ui/card.tsx",
    "apps/web/components/ui/badge.tsx",
    
    # Frontend lib
    "apps/web/lib/utils.ts",
    "apps/web/lib/api.ts",
    "apps/web/lib/auth.ts",
    "apps/web/lib/store.ts",
    
    # Frontend types
    "apps/web/types/api.ts",
    "apps/web/types/auth.ts",
    "apps/web/types/common.ts",
    
    # Documentation
    "docs/CLAUDE.md",
    "README_BACKEND.md",
    "README_FRONTEND.md",
]

# Required directories
REQUIRED_DIRS = [
    "services/api/app",
    "services/api/app/core",
    "services/api/app/models",
    "services/api/app/schemas",
    "services/api/app/services",
    "services/api/app/api",
    "services/api/app/api/v1",
    "services/api/alembic",
    "services/api/tests",
    "apps/web/app",
    "apps/web/components",
    "apps/web/components/ui",
    "apps/web/lib",
    "apps/web/types",
    "docs",
    "scripts",
]

def check_file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    full_path = PROJECT_ROOT / file_path
    return full_path.exists()

def check_directory_exists(dir_path: str) -> bool:
    """Check if a directory exists."""
    full_path = PROJECT_ROOT / dir_path
    return full_path.exists() and full_path.is_dir()

def verify_project_structure() -> Tuple[bool, List[str], List[str]]:
    """Verify the complete project structure."""
    missing_files = []
    missing_dirs = []
    
    # Check core files
    for file_path in CORE_FILES:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
    
    # Check required directories
    for dir_path in REQUIRED_DIRS:
        if not check_directory_exists(dir_path):
            missing_dirs.append(dir_path)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0, missing_files, missing_dirs

def check_docker_compose() -> bool:
    """Check if Docker Compose file is properly configured."""
    docker_compose_path = PROJECT_ROOT / "docker-compose.yml"
    if not docker_compose_path.exists():
        return False
    
    try:
        with open(docker_compose_path, 'r') as f:
            content = f.read()
            # Check for essential services
            required_services = ['postgres', 'redis', 'minio', 'api', 'web']
            return all(service in content for service in required_services)
    except Exception:
        return False

def check_makefile() -> bool:
    """Check if Makefile has essential commands."""
    makefile_path = PROJECT_ROOT / "Makefile"
    if not makefile_path.exists():
        return False
    
    try:
        with open(makefile_path, 'r') as f:
            content = f.read()
            # Check for essential commands
            required_commands = ['up', 'down', 'build', 'test']
            return all(command in content for command in required_commands)
    except Exception:
        return False

def main():
    """Main verification function."""
    print("🔍 Verifying AI Local RAG System Project Structure")
    print("=" * 60)
    
    # Check project structure
    structure_ok, missing_files, missing_dirs = verify_project_structure()
    
    if not structure_ok:
        print("❌ Project structure verification failed!")
        print()
        
        if missing_files:
            print("Missing files:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            print()
        
        if missing_dirs:
            print("Missing directories:")
            for dir_path in missing_dirs:
                print(f"  - {dir_path}")
            print()
    else:
        print("✅ Project structure verification passed!")
        print()
    
    # Check Docker Compose
    docker_ok = check_docker_compose()
    if docker_ok:
        print("✅ Docker Compose configuration verified!")
    else:
        print("❌ Docker Compose configuration issues found!")
    print()
    
    # Check Makefile
    makefile_ok = check_makefile()
    if makefile_ok:
        print("✅ Makefile configuration verified!")
    else:
        print("❌ Makefile configuration issues found!")
    print()
    
    # Overall status
    overall_ok = structure_ok and docker_ok and makefile_ok
    
    if overall_ok:
        print("🎉 All verifications passed! The project is ready for development.")
        print()
        print("Next steps:")
        print("1. Run 'make install' to install dependencies")
        print("2. Run 'make up' to start the development environment")
        print("3. Access the application at http://localhost:3000")
        print("4. Access the API docs at http://localhost:8000/docs")
    else:
        print("⚠️  Some verifications failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
