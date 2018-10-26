"""
INTERFACES
====================================================================================================

Interfaces to the database for managing rows as objects.

----------------------------------------------------------------------------------------------------

**Created**
    10.22.18
**Updated**
    10.24.18 by Darkar
**Author**
    Darkar
"""

from datetime import datetime

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
        self.resolved = None
        self.probabilities = {}
        self.outcome = None

    def get_vectors(self, pad=0):
        """
        Returns vectors for the predicted probabilites and, if it exist, a one-hot vector that
        encodes the outcome.
        """
        preds = []
        outs = []
        for event in self.probabilities:
            preds.append(self.probabilities[event])
            if event == self.outcome:
                outs.append(1)
            else:
                outs.append(0)
        delta = pad - len(preds)
        if delta > 0:
            preds += [0]*delta
            outs += [0]*delta
        return preds, outs if self.outcome else None

    def load(self):
        find_predictions_query = """ select created, description from predictions
                                     where id = ?"""
        self._cursor.execute(find_predictions_query, self._rid)
        timestamp, full_description = self._cursor.fetchone()
        if not timestamp: return False
        self.created = datetime.utcfromtimestamp(timestamp)
        desc_lines = full_description.split("\n")
        self.name, self.description = desc_lines[0], "\n".join(full_description[1:])

        find_probabilities_query = """ select probability, event from probabilities
                                     where pid = ? """
        self._cursor.execute(find_probabilities_query, self._rid)
        for row in self._cursor.fetchall():
            probability, event = row
            self.probabilities[event] = probability
        if not self.probabilities:
            raise KeyError("No row matching the id {} was found".format(self._rid))

        find_outcome_query = """ select probabilities.event, outcomes.created
                                 from probabilites, outcomes
                                 where probabilities.pid = ?
                                 and probabilities.id = outcomes.oid """
        self._cursor.execute(find_outcome_query, self._rid)
        outcome, resolved = self._cursor.fetchone()
        if outcome and resolved:
            self.outcome = outcome
            self.resolved = datetime.utcfromtimestamp(resolved)

        return True

    def save(self):
        check_existing_query = """ select * from predictions where id = ? """
        self._cursor.execute(check_existing_query, self._rid)

        if self._cursor.fetchone():
            #UPDATE
            update_predictions_query = """ update predictions
                                           set created = ?, desciption = ?
                                           where id = ? """
            timestamp = self.created.timestamp()
            full_description = self.name + "\n" + self.description
            self._cursor.execute(update_predictions_query, timestamp, full_description, self._rid)
            self._cursor.commit()

            for event in self.probabilities:
                update_probabilities_query = """ update probabilities
                                                 set probability = ?
                                                 where event = ? and pid = ? """
                probability = self.probabilities[event]
                self._cursor.execute(update_probabilities_query, probability, event, self._rid)
                self._cursor.commit()

        else:
            #INSERT
            insert_predictions_query = """ insert into predictions (created, decription)
                                           values (?, ?) """
            timestamp = self.created.timestamp()
            full_description = self.name + "\n" + self.description
            self._cursor.execute(insert_predictions_query, timestamp, full_description)
            self._cursor.commit()

            for event in self.probabilities:
                insert_probabilities_query = """ insert into probabilities (pid, probability, event)
                                                 values (?, ?, ?) """
                probability = self.probabilities[event]
                self._cursor.execute(insert_probabilities_query, self._rid, probability, event)
                self._cursor.commit()

        find_outcome_id_query = """ select id from probabilities where event = ? and pid = ? """
        self._cursor.execute(find_outcome_id_query, self.outcome, self._rid)
        oid = self._cursor.fetcheone()

        check_existing_outcome_query = """ select * from outcomes where pid = ? """
        self._cursor.execute(check_existing_outcome_query, self._rid)
        if self._cursor.fetchone():
            update_outcomes_query = """ update outcomes
                                        set created = ?, oid = ?
                                        where pid = ? """
            timestamp = self.resolved.timestamp()
            self._cursor.execute(update_outcomes_query, timestamp, oid, self._rid)
            self._cursor.commit()
        else:
            insert_outcomes_query = """ insert into outcomes (pid, oid, created)
                                        values (?, ?, ?) """
            timestamp = self.resolved.timestamp()
            self._cursor.execute(insert_outcomes_query, self._rid, oid, timestamp)

        return True
