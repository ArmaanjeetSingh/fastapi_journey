from models import create_tables
from services import create_user, get_user_by_id, get_all_users, create_post, get_posts_by_user, user_update_email


create_tables()

# create_user("Armaan","ar1234@Gmail.com")
# create_post("hello c++ video","brief intro about programming",1)

get_user_by_id(1)

get_all_users()

print(get_posts_by_user(1))

update_user_email()