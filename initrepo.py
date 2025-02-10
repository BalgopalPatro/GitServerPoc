import os
import pygit2

# Path to the new bare repository
repo_path = "git_repos/my_repo"

# Initialize a bare repository
repo = pygit2.init_repository(repo_path, bare=True)
repo.config['init.defaultBranch'] = 'main'
repo.set_head('refs/heads/main')

# Create a new commit in the main branch with a README file
index = repo.index
blob_id = repo.create_blob(b"# MyRepo\nThis is a README file for my_repo3.")
index.add(pygit2.IndexEntry('README.md', blob_id, pygit2.GIT_FILEMODE_BLOB))


blob_id = repo.create_blob(b"# MyRepo\nThis is a README file for my_repo3.")
index.add(pygit2.IndexEntry('README1.md', blob_id, pygit2.GIT_FILEMODE_BLOB))


blob_id = repo.create_blob(b"# MyRepo\nThis is a README file for my_repo3.")
index.add(pygit2.IndexEntry('README2.md', blob_id, pygit2.GIT_FILEMODE_BLOB))

tree_id = index.write_tree()

author = pygit2.Signature('Author Name', 'author@example.com')
committer = pygit2.Signature('Committer Name', 'committer@example.com')
message = 'Initial commit with README'
repo.create_commit(
    'refs/heads/main',  # the name of the reference to update
    author,  # the author of the commit
    committer,  # the committer of the commit
    message,  # the commit message
    tree_id,  # the tree object this commit points to
    []  # parents of the new commit (none in this case)
)

print(f"Initialized bare repository at {repo_path}")