Date and Time generators
========================

Perjury provides both low and high level tools for generating date based
values.

.. autofunction:: perjury.generators
    :members: datetime_in_range


.. autoclass:: perjury.generators.datetime_generators.DatetimeGenerator


Perjery also provides two ready to use generator functions.


current_datetime

Returns a datetime within 30 days of today.

datetime_generator

Returns a datetime between ``datetime.datetime.min`` and ``datetime.datetime.max``.
