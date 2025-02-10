from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import GitRepository
from pathlib import Path
import pygit2
import subprocess

# Base directory for repositories
REPO_BASE_DIR = Path("git_repos")

@csrf_exempt
def create_repository(request, repo_name):
    """Create a new Git repository."""
    if request.method == "POST":
        try:
            repo, created = GitRepository.objects.get_or_create(name=repo_name)
            if created:
                repo.create_repo()
                return JsonResponse({"message": f"Repository '{repo_name}' created successfully."})
            return JsonResponse({"message": "Repository already exists."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def list_repositories(request):
    """List all Git repositories."""
    repos = GitRepository.objects.all().values("name", "created_at")
    return JsonResponse({"repositories": list(repos)})

def get_repo_commit_details(request,repo_name, branch="master"):
    """List all Git repositories."""
    repo_path = REPO_BASE_DIR / repo_name
    if not repo_path.exists():
        return HttpResponse("Repository not found", status=404)
    repo = pygit2.Repository(str(repo_path))
    branch = repo.lookup_branch(branch)
    if branch is None:
        return HttpResponse("Branch not found", status=404)
    commit = repo[branch.target]
    commits = []
    for commit in repo.walk(branch.target, pygit2.GIT_SORT_TIME):
        commits.append({
            "commit_id": commit.short_id,
            "message": commit.message,
            "author": commit.author.name,
            "email": commit.author.email,
            "time": commit.commit_time,
        })

    return JsonResponse({"branch": branch.name, "commits": commits})


@csrf_exempt
def git_info_refs(request, repo_name):
    """Handles `git clone` by advertising repository references."""
    repo_path = REPO_BASE_DIR / repo_name
    if not repo_path.exists():
        return HttpResponse("Repository not found", status=404)

    service = request.GET.get("service")
    if service not in ["git-upload-pack", "git-receive-pack"]:
        return HttpResponse("Invalid service", status=400)

    # Create the pkt-line header Git expects
    header = f"# service={service}\n".encode()
    pkt_line = f"{len(header) + 4:04x}".encode() + header + b"0000"

    # Run `git-upload-pack --advertise-refs`
    result = subprocess.run(
        ["git", 'upload-pack', "--stateless-rpc", "--advertise-refs", str(repo_path)],
        capture_output=True
    )

    if result.returncode != 0:
        return HttpResponse(f"Error running git {service}", status=500)
    return HttpResponse(pkt_line + result.stdout, content_type=f"application/x-{service}-advertisement")

@csrf_exempt
def git_upload_pack(request, repo_name):
    """Handles `git fetch` requests."""    
    repo = get_object_or_404(GitRepository, name=repo_name)
    repo_path = REPO_BASE_DIR / repo_name

    response = subprocess.run(
        ["git", "upload-pack", "--stateless-rpc", str(repo_path)],
        input=request.body,
        capture_output=True,
    )
    return HttpResponse(response.stdout, content_type="application/x-git-upload-pack-result")

@csrf_exempt
def git_receive_pack(request, repo_name):
    """Handles `git push` requests."""
    repo = get_object_or_404(GitRepository, name=repo_name)
    repo_path = REPO_BASE_DIR / repo_name


    response = subprocess.run(
        ["git", "receive-pack", "--stateless-rpc", str(repo_path)],
        input=request.body,
        capture_output=True,
    )
    return HttpResponse(response.stdout, content_type="application/x-git-receive-pack-result")


