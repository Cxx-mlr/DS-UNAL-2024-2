from Session import Session

from utils import console

session = Session()

console.rule("Empleados")
for user in session.shared.users:
    console.print(user.to_csv())

print()
console.rule("Credenciales")
for credentials in session.shared.credentials_list:
    console.print(credentials)