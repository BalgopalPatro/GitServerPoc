from django.urls import path
from .views import create_repository, list_repositories, git_info_refs, git_upload_pack, git_receive_pack,get_repo_commit_details

urlpatterns = [
    path('create_repo/<str:repo_name>/', create_repository, name="create_repo"),
    path('list_repos/', list_repositories, name="list_repos"),
    path('git/<str:repo_name>/commits/<str:branch>', get_repo_commit_details, name="git_info_refs"),
    path('git/<str:repo_name>/info/refs', git_info_refs, name="git_info_refs"),
    path('git/<str:repo_name>/git-upload-pack', git_upload_pack, name="git_upload_pack"),
    path('git/<str:repo_name>/git-receive-pack', git_receive_pack, name="git_receive_pack"),
]
