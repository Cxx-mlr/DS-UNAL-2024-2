from __future__ import annotations


from SorterAgenda import SorterAgenda
from Agenda import Agenda

def main():
    sorter_agenda = SorterAgenda()

    agenda = Agenda(capacity=6)
    agenda.load_from_file()

    for user in agenda.get_users():
        sorter_agenda.add_user(user)

    sorter_agenda.sort()
    sorter_agenda.display()

if __name__ == "__main__":
    main()