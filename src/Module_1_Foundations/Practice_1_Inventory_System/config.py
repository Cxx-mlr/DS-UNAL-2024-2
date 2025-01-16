from pathlib import Path

THIS_PATH = Path(__file__).parent
DATA_PATH = THIS_PATH / "data" / "prod"

DELETE_REQUESTS_PATH = DATA_PATH / "delete_requests.txt"
ADD_REQUESTS_PATH = DATA_PATH / "add_requests.txt"
PASSWORDS_PATH = DATA_PATH / "passwords.txt"
SAVED_INVENTORY_PATH = DATA_PATH / "saved_inventory.txt"
DELETED_INVENTORY_PATH = DATA_PATH / "deleted_inventory.txt"
EMPLOYEES_PATH = DATA_PATH / "employees.txt"
APPROVED_CHANGE_CONTROL_PATH = DATA_PATH / "approved_change_control.txt"
REJECTED_CHANGE_CONTROL_PATH = DATA_PATH / "rejected_change_control.txt"
REQUESTS_STATUS_FILENAME = "requests_status {} {}.txt"
