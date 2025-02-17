"""
``/sys/module`` System Module Information
=========================================

A parser to parse the system module information.

Parsers included in this module are:

DMModUseBlkMq - file ``/sys/module/dm_mod/parameters/use_blk_mq``
------------------------------------------------------------------
LpfcMaxLUNs - file ``/sys/module/lpfc/parameters/lpfc_max_luns``
----------------------------------------------------------------
Ql2xMaxLUN - file ``/sys/module/qla2xxx/parameters/ql2xmaxlun``
---------------------------------------------------------------
SCSIModMaxReportLUNs - file ``/sys/module/scsi_mod/parameters/max_report_luns``
-------------------------------------------------------------------------------
SCSIModUseBlkMq - file ``/sys/module/scsi_mod/parameters/use_blk_mq``
---------------------------------------------------------------------
VHostNetZeroCopyTx - file ``/sys/module/vhost_net/parameters/experimental_zcopytx``
-----------------------------------------------------------------------------------
"""
from insights import parser, Parser
from insights.parsers import SkipException
from insights.specs import Specs


class XModUseBlkMq(Parser):
    """
    Parse for file `/sys/module/{dm_mod,scsi_mod}/parameters/use_blk_mq`.
    File content shows if use_blk_mq parameter is on.

    Sample Content::

        Y

    Raises:
        SkipException: When nothing need to parse.

    Attributes:
        val(str): Raw data of the content.
    """

    def parse_content(self, content):
        if not content or len(content) != 1:
            raise SkipException()
        self.val = content[0].strip()

    @property
    def is_on(self):
        """
        Returns:
            (bool): True for on, False for off.

        Raises:
            ValueError: When tell is_on for unknown cases.
        """
        if self.val in ['Y', '1']:
            return True
        if self.val in ['N', '0']:
            return False
        raise ValueError("Unexpected value {0}, please get raw data from attribute 'val' and tell is_on by yourself.".format(self.val))


class MaxLUNs(Parser):
    """
    Parse for file `/sys/module/{scsi_mod, lpfc, ...}/parameters/{max_report_luns, lpfc_max_luns, ...}`.
    File content shows the maximum LUN value currently supported.

    Sample Content::

        512

    Raises:
        SkipException: When content is empty or no parse-able content.

    Attributes:
        val(int): Convert the raw data of the content to int.
    """

    def parse_content(self, content):
        if not content or len(content) != 1:
            raise SkipException()
        if not content[0].strip('').isdigit():
            raise ValueError("Unexpected content: {0}".format(content[0]))
        self.val = int(content[0].strip())


@parser(Specs.dm_mod_use_blk_mq)
class DMModUseBlkMq(XModUseBlkMq):
    """
    This file `/sys/module/dm_mod/parameters/use_blk_mq` shows if use_blk_mq
    parameter is on.

    Examples::

        >>> dm_mod_use_blk_mq.val
        'Y'
        >>> dm_mod_use_blk_mq.is_on
        True
    """
    pass


@parser(Specs.scsi_mod_use_blk_mq)
class SCSIModUseBlkMq(XModUseBlkMq):
    """
    This file `/sys/module/scsi_mod/parameters/use_blk_mq` shows if use_blk_mq
    parameter is on.

    Examples::

        >>> scsi_mod_use_blk_mq.val
        'N'
        >>> scsi_mod_use_blk_mq.is_on
        False
    """
    pass


@parser(Specs.vhost_net_zero_copy_tx)
class VHostNetZeroCopyTx(XModUseBlkMq):
    """This file `/sys/module/vhost_net/parameters/experimental_zcopytx` shows if
    vhost_net's zero-copy tx parameter is enabled or not.

    Examples::

        >>> vhost_net_zero_copy_tx.val
        '0'
        >>> vhost_net_zero_copy_tx.is_on
        False

    """
    pass


@parser(Specs.lpfc_max_luns)
class LpfcMaxLUNs(MaxLUNs):
    """
    This file `/sys/module/lpfc/parameters/lpfc_max_luns` shows the max LUN number
    supported by lpfc driver.

    Examples:

        >>> lpfc_max_luns.val
        512
    """
    pass


@parser(Specs.ql2xmaxlun)
class Ql2xMaxLUN(MaxLUNs):
    """
    This file `/sys/module/qla2xxx/parameters/ql2xmaxlun` shows the max LUN number
    supported by qla2xxxx driver.

    Examples:

        >>> ql2xmaxlun.val
        512
    """
    pass


@parser(Specs.scsi_mod_max_report_luns)
class SCSIModMaxReportLUNs(MaxLUNs):
    """
    This file `/sys/module/scsi_mod/parameters/max_report_luns` shows the max LUN number
    supported by OS.

    Examples:

        >>> scsi_mod_max_report_luns.val
        512
    """
    pass
