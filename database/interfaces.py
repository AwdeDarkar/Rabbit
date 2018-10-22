"""
INTERFACES
====================================================================================================

Interfaces to the database for managing rows as objects.

----------------------------------------------------------------------------------------------------

**Created**
    10.22.18
**Updated**
    10.22.18 by Ben Croisdale
**Author**
    Ben Croisdale
**Copyright**
    This code is property of HEAT LLC Copyright HEAT LLC 2018 (c)
"""

class DatabaseInterface:
    """ Abstract class with serialization tools for interfacing with the database """

    def __init__(self, rid, cursor):
        self._cursor = cursor
        self._rid = rid

    def __del__(self):
        self.save()

    def load(self): #pylint: disable=no-self-use
        """ Loads the object from the database, returns True if successful """
        return False

    def save(self): #pylint: disable=no-self-use
        """ Saves the object to the database, returns True if successful """
        return False


    @classmethod
    def create_all(cls, conn, test=lambda x: True):
        """
        Generator to create all of the interfaces accessible over the connection which pass an
        optional test.
        """
        i = 0
        obj = cls(i, conn.cursor())
        while obj.load():
            if test(obj): yield obj
            i += 1
            obj = cls(i, conn.cursor())

class PredictionInterface(DatabaseInterface):
    """ Manage predictions and outcomes """

    def __init__(self, rid, cursor):
        super(PredictionInterface, self).__init__(rid, cursor)

        self.name = "Unnamed"
        self.description = "No description"
        self.created = None
        self.determined = None
        self.probabilities = {}
        self.outcome = ""

    def get_vector(self):
        """
        Returns a vector where the first half are the probabilities and the second half is a one-hot
        outcome vector.
        """
        preds = []
        outs = []
        for event in self.probabilities:
            preds.append(self.probabilities[event])
            if event == self.outcome:
                outs.append(1)
            else:
                outs.append(0)
        return preds + outs

    def load(self):
        find_row_query = """ select created, description from predictions
                             where id = {}""".format(self._rid)
        #bahh...
