from git import Repo


class GitClient(object):

    @classmethod
    def pull(cls, repo_path):
        repo = Repo(repo_path)
        # current = repo.head.commit
        remote = repo.remote()
        remote.pull()
        # return current != repo.head.commit
        # diff = repo.index.diff(None)
        # return [d.a_path for d in diff]

    @classmethod
    def clone(cls, git_url, base_path):
        Repo.clone_from(git_url, base_path)

