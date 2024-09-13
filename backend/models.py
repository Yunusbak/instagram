from database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Boolean, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    post = relationship('Post', back_populates='user')
    comments = relationship('Comments', back_populates='user')
    likes = relationship('Likes', back_populates='user')
    follower_user = relationship('Followers', foreign_keys='[Followers.follower_id]', back_populates='follower')
    following_user = relationship('Followers', foreign_keys='[Followers.following_id]', back_populates='following')
    sent_messages = relationship('Messages', foreign_keys='[Messages.sender_id]', back_populates='sender')
    received_messages = relationship('Messages', foreign_keys='[Messages.receiver_id]', back_populates='receiver')

class Post(Base):
    __tablename__ = 'post'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    image_path = Column(String(255), nullable=True)
    caption = Column(String(255), nullable=True)
    review = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='post')
    comments = relationship('Comments', back_populates='post', cascade="all, delete-orphan")
    like = relationship('Likes', back_populates='post', cascade="all, delete-orphan")
    post_tags = relationship('PostTags', back_populates='post')

class Comments(Base):
    __tablename__ = 'comment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id'), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Likes(Base):
    __tablename__ = 'like'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='like')

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    follower_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    following_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    follower = relationship('User', foreign_keys=[follower_id], back_populates='follower_user')
    following = relationship('User', foreign_keys=[following_id], back_populates='following_user')

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    post_tags = relationship('PostTags', back_populates='tags')

class PostTags(Base):
    __tablename__ = 'post_tags'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id'), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    post = relationship('Post', back_populates='post_tags')
    tags = relationship('Tags', back_populates='post_tags')

class Messages(Base):
    __tablename__ = 'messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    is_read = Column(Boolean, default=False)

    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')