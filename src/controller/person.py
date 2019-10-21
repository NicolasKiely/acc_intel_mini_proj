from typing import List

from src.controller import fields
import src.model.person


class AddPersons(fields.AddMovieFieldBaseClass):
    """ Action to add list of persons

    Kludgy to use fields controller as base class, but given
    time constraints it'll do.
    """
    def execute(self, person_names: List[str]):
        self.execute_add(person_names, src.model.person.Person, 'person')
