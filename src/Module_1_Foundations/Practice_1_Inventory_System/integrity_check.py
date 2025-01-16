from utils import console
from Session import Session

session = Session()

credentials_list = session.shared.credentials_list
users = session.shared.users
add_requests = session.shared.add_requests
delete_requests = session.shared.delete_requests
pending_requests = session.shared.pending_requests
approved_requests = session.shared.approved_requests
rejected_requests = session.shared.rejected_requests
non_pending_requests = session.shared.non_pending_requests
requests = session.shared.requests
saved_inventory = session.shared.saved_inventory
deleted_inventory = session.shared.deleted_inventory
inventory = session.shared.inventory
saved_equipment = session.shared.saved_equipment
deleted_equipment = session.shared.deleted_equipment
approved_changelog = session.shared.approved_changelog
rejected_changelog = session.shared.rejected_changelog
changelog = session.shared.changelog

credentials_list__user_ids = list(
    user_id
    for user_id in credentials_list.apply(lambda credentials: credentials.get_user_id())
)
credentials_list__unique_user_ids = set(credentials_list__user_ids)

users__user_ids = list(user_id for user_id in users.apply(lambda user: user.get_id()))
users__unique_user_ids = set(users__user_ids)

if len(credentials_list__unique_user_ids) != len(credentials_list__user_ids):
    console.print(
        "[yellow]Hay IDs de usuario duplicados en la lista de credenciales.[/]"
    )

if len(users__unique_user_ids) != len(users__user_ids):
    console.print("[yellow]Hay IDs de usuario duplicados en la lista de usuarios.[/]")

if len(credentials_list__user_ids) != len(users__user_ids):
    console.print(
        "[yellow]El número de IDs de usuario en la lista de credenciales no coincide con el número en la lista de usuarios.[/]"
    )