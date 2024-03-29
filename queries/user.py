from models import User
def get_user_by_discord_id(db, discord_user_id):
    user = db.query(User).filter(User.discord_user_id == discord_user_id).first()
    return user
            if user is None:
                if message.author.avatar:
                        avatar = message.author.avatar.url
                else:
                    avatar = ''
                user = User(discord_user_id=author_id, display_name=message.author.display_name, username=message.author.name, current_avatar_url=avatar)
                db.add(user)
                db.commit()
                db.refresh(user)