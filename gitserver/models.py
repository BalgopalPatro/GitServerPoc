from django.db import models
from pathlib import Path
from pygit2 import init_repository

# Base directory for repositories
REPO_BASE_DIR = Path("git_repos")
REPO_BASE_DIR.mkdir(parents=True, exist_ok=True)

class GitRepository(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_repo_path(self) -> Path:
        """Returns the full path to the repository."""
        return REPO_BASE_DIR / self.name

    def create_repo(self):
        """Initializes a bare Git repository."""
        repo_path = self.get_repo_path()
        if repo_path.exists():
            raise ValueError("Repository already exists")
        init_repository(str(repo_path), bare=True)
