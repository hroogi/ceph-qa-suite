"""
Set fs.aio-max-nr to 128M for Async I/O using sysctl. 

Reset back to default value of 65K after test.
"""

import argparse
import contextlib
import logging

from teuthology import misc as teuthology
from teuthology import contextutil
from teuthology.orchestra import run

log = logging.getLogger(__name__)


@contextlib.contextmanager
def task(ctx, config):
    """
    Set fs.aio-max-nr in order to test async read tests.
    :param ctx: Context
    :param config: Configuration
    """

    log.info('Setting fs.aio-max-nr parameter using sysctl...')
    run.wait(
        ctx.cluster.run(
            args=['sudo', 'sysctl', '-w', 'fs.aio-max-nr=134217728'],
            wait=False,
        )
    )
    try:
        yield
    finally:
        log.info('Resetting the default fs.aio-max-nr parameter...')
        run.wait(
            ctx.cluster.run(
                args=['sudo', 'sysctl', '-w', 'fs.aio-max-nr=65536'],
                wait=False,
            ),
        )

