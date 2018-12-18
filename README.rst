Rabbit
====================================================================================================

A tool for making and calibrating short-term predictions.

Motivation
----------------------------------------------------------------------------------------------------

I often find myself failing to predict things, particularly things like my personal productivity or
goals I set for myself. While it would be nice to perfectly be able to meet every goal I set all the
the time, this is unrealistic and in practice is far from the case. At the very least, I would like 
to be able to anticipate my future behavior and make reliable predictions about what I am likely to
actually do so that I can better plan long-term projects.

This is why I am designing *Rabbit*. I want to be able to make predictions about things that are
likely to resolve within a few days, check to see how my predictions did, and then score myself over
a long period of time. The hope is that this will turn 'predicting the future' from a nebulous thing
I am able to do with varying-but-generally-poor success to a skill that I can train over time.

Design
----------------------------------------------------------------------------------------------------

This is the first project I have worked on where I have some real conception of the 'right way' to
do this sort of thing. I am using `Sphinx <https://http://www.sphinx-doc.org>`_ to generate
documentation, `Pytest <https://docs.pytest.org/en/latest/>`_ to test the code (with mostly dev-ops
inspired test-driven development), and `Pylint <https://www.pylint.org/>`_ to ensure my code stays
in spec with my coding standard (very close, though not precisely, `PEP 8 
<https://www.python.org/dev/peps/pep-0008/>`_).

Further, in order to aid in doing things the 'right way' I am writing out the requirements of this
project *very explicitly* and separating them into minimum-viable-product (MVP), expected product,
and a catch-all list of other cool features I'd like to add at some point.

Minimum:

    * Collects *predictions* of discrete events (events that can happen in one of a few distinct
      ways) where a 'prediction' is a vector, :math:`v`, made of probabilities, :math:`p`, such
      that :math:`p\in[0,1)\land\sum{v}=1`. [Done]
    * Associates predictions with *outcomes*, a one-hot vector of the same length as the associated
      prediction. [Done]
    * Records the timestamp of both the predictions and the outcomes. [Done]
    * Scores the predictions with outcomes in an arbitrary time interval using the `Brier score
      <https://en.wikipedia.org/wiki/Brier_score>`_. [Done]
    * Exposes these features through a command-line and web API (either RESTful or GraphQL,
      haven't decided yet).

Expected:
    
    * Associates predictions and outcomes with *users* such that multiple users may interact with a
      given instance of Rabbit without being exposed to each-others predictions or scores.
    * Enforces users with an authentication system for API access, ideally one which supports pubkey
      authentication.
    * Provides a human-friendly web interface for user account creation and prediction management.
    * Provides a template system for reccuring or common predictions.

Additional:

    * Email interface, possibly with regular reminders.
