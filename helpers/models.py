from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class User(BaseModel):
    login: str
    id: int
    type: str
    user_view_type: Optional[str]
    site_admin: bool


class RepoOwner(BaseModel):
    login: str


class Repository(BaseModel):
    id: int
    name: str
    private: bool
    compare_url: str
    owner: RepoOwner


class Branch(BaseModel):
    ref: str
    sha: str


class PullRequest(BaseModel):
    id: int
    state: str
    title: str
    body: Optional[str]
    locked: bool
    comments_url: str
    diff_url: Optional[str]
    user: User
    head: Branch
    base: Branch


class WebhookPayload(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repository

###############################################################################

class Comment(BaseModel):
    body: str
    path: str
    line: int
    side: Optional[str] = "RIGHT"
    start_line: Optional[int] = None
    start_side: Optional[str] = None


class LLMResponse(BaseModel):
    comments: List[Comment]

####################################################################################