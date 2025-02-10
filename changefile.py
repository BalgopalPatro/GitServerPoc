import pygit2

# Path to the bare repository
repo_path = "git_repos/my_repo"
repo = pygit2.Repository(repo_path)

# Get the reference for the branch (e.g., master)
branch_name = "master"
branch_ref = f"refs/heads/{branch_name}"
commit = repo.lookup_reference(branch_ref).peel(pygit2.Commit)

# Get the current tree
old_tree = commit.tree

# Create a new blob (file content)
file_path = "Hello/foo/bar/app.py"  # Path inside the repository
new_content = b"print('hello')"
blob_id = repo.create_blob(new_content)

# Function to recursively update trees for nested directories
def update_tree(repo, tree, path_parts, blob_id):
    builder = repo.TreeBuilder(tree) if tree else repo.TreeBuilder()

    if len(path_parts) == 1:  # Last part is the file
        builder.insert(path_parts[0], blob_id, pygit2.GIT_FILEMODE_BLOB)
    else:
        dir_name = path_parts[0]
        sub_tree = tree[dir_name] if tree and dir_name in tree else None
        sub_tree_obj = repo.get(sub_tree.id) if sub_tree else None
        new_sub_tree_id = update_tree(repo, sub_tree_obj, path_parts[1:], blob_id)
        builder.insert(dir_name, new_sub_tree_id, pygit2.GIT_FILEMODE_TREE)

    return builder.write()

# Create a new tree with the updated file
new_tree_id = update_tree(repo, old_tree, file_path.split("/"), blob_id)

if new_tree_id == old_tree.id:
    print("No changes detected. Exiting.")
    exit()

# Create a new commit
author = pygit2.Signature("Your Name", "your.email@example.com")
committer = pygit2.Signature("Your Name", "your.email@example.com")

new_commit_id = repo.create_commit(
    branch_ref,  # Update the branch reference
    author,
    committer,
    "Updated main.py",
    new_tree_id,  # Pass the tree OID
    [commit.id],  # Use `.id`
)

print(f"Updated {file_path} in bare repository. New commit: {new_commit_id}")
