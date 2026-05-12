from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base

class PrDetails(Base):
    __tablename__ = "pr_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    commit_message: Mapped[str] = mapped_column(Text, default="")
    committed_by: Mapped[str] = mapped_column(String(255), default="")
    committed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    changed_files: Mapped[list] = mapped_column(JSON, default=list)

    # PR metadata columns
    pr_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    pr_title: Mapped[str] = mapped_column(String(512), default="")
    pr_body: Mapped[str] = mapped_column(Text, default="")
    pr_state: Mapped[str] = mapped_column(String(32), default="")
    pr_locked: Mapped[bool] = mapped_column(Integer, default=0)  # 0=False, 1=True
    pr_comments_url: Mapped[str] = mapped_column(String(512), default="")

    user_login: Mapped[str] = mapped_column(String(255), default="")
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_type: Mapped[str] = mapped_column(String(64), default="")
    user_site_admin: Mapped[bool] = mapped_column(Integer, default=0)  # 0=False, 1=True

    head_ref: Mapped[str] = mapped_column(String(255), default="")
    base_ref: Mapped[str] = mapped_column(String(255), default="")

    # Config parsed from config.py in the repo
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    diff_details: Mapped[str] = mapped_column(Text, default="")
    pr_review_comments: Mapped[list] = mapped_column(JSON, default=list)

    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[str] = mapped_column(String(255), default="")