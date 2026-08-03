from datetime import datetime

from app.extensions import db


# =====================================================
# TEAM CHAT CHANNELS
# =====================================================

class ChatChannel(db.Model):
    __tablename__ = "chat_channels"

    id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    is_private = db.Column(
        db.Boolean,
        default=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    team = db.relationship(
        "Team",
        back_populates="channels"
    )

    creator = db.relationship(
        "User",
        foreign_keys=[created_by]
    )

    messages = db.relationship(
        "ChatMessage",
        back_populates="channel",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<ChatChannel {self.name}>"



# =====================================================
# CHAT MESSAGES
# =====================================================

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    channel_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_channels.id"),
        nullable=False
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    edited = db.Column(
        db.Boolean,
        default=False
    )

    deleted = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    channel = db.relationship(
        "ChatChannel",
        back_populates="messages"
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id]
    )

    reads = db.relationship(
        "MessageRead",
        back_populates="message",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<ChatMessage {self.id}>"



# =====================================================
# READ RECEIPTS
# =====================================================

class MessageRead(db.Model):
    __tablename__ = "message_reads"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_messages.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    read_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    message = db.relationship(
        "ChatMessage",
        back_populates="reads"
    )

    user = db.relationship(
        "User"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "message_id",
            "user_id",
            name="uq_message_reader"
        ),
    )

    def __repr__(self):
        return f"<MessageRead {self.id}>"