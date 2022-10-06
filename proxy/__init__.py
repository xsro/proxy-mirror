import imp
from .git import Git, GitSsh

proxies={
    'git':Git(),
    'git-ssh':GitSsh()
}