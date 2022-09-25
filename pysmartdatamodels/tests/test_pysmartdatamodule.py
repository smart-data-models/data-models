from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

from pysmartdatamodels import commands


def test_list_all_datamodels():
    assert len(commands.list_all_datamodels()) > 0
