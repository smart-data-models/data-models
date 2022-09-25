from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

from pysmartdatamodels import queries


def test_list_all_datamodels():
    assert len(queries.list_all_datamodels()) > 0
