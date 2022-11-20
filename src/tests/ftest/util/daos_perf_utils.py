#!/usr/bin/python
"""
  (C) Copyright 2019-2022 Intel Corporation.

  SPDX-License-Identifier: BSD-2-Clause-Patent
"""
from command_utils_base import FormattedParameter
from command_utils import ExecutableCommand


class DaosPerfCommand(ExecutableCommand):
    """Defines a object representing the daos_perf command.

    The daos_perf utility benchmarks point-to-point I/O performance of different
    layers of the DAOS stack.
    """

    def __init__(self, path):
        """Create a daos_perf command object.

        Args:
            path (str): path to the daos_perf command
        """
        super().__init__(
            "/run/daos_perf/*", "daos_perf", path)

        # daos_perf command line options:
        #
        #   -P <number/string>
        #       Pool SCM partition size, which can have M(megabytes) or
        #       G(gigabytes) as postfix of number. E.g. -P 512M, -P 8G.
        self.pool_scm_size = FormattedParameter("-P {}")

        #   -N <number/string>
        #       Pool NVMe partition size.
        self.pool_nvme_size = FormattedParameter("-N {}")

        #   -T <echo|daos>
        #       Type of test, it can be 'daos' or 'echo'.
        #           echo : I/O traffic generated by the utility only goes
        #               through the network stack and never lands to storage.
        #           daos : I/O traffic goes through the full DAOS stack,
        #               including both network and storage.
        #       The default value is 'daos'.
        self.test_type = FormattedParameter("-T {}", "daos")

        #   -C <number>
        #       Credits for concurrently asynchronous I/O. It can be value
        #       between 1 and 64. The utility runs in synchronous mode if
        #       credits is set to 0.
        self.credits = FormattedParameter("-C {}")

        #   -c TINY|LARGE|R2S|R3S|R4S|EC2P1|EC2P2|EC4P2|EC8P2
        #       Object class for DAOS full stack test.
        self.object_class = FormattedParameter("-c {}")

        #   -o <number>
        #       Number of objects are used by the utility.
        self.objects = FormattedParameter("-o {}")

        #   -d <number/string>
        #       Number of dkeys per object. The number can have 'k' or 'm' as
        #       postfix which stands for kilo or million.
        self.dkeys = FormattedParameter("-d {}")

        #   -a <number/string>
        #       Number of akeys per dkey. The number can have 'k' or 'm' as
        #       postfix which stands for kilo or million.
        self.akeys = FormattedParameter("-a {}")

        #   -A [R]
        #       Use array value of akey, single value is selected by default.
        #       optional parameter 'R' indicates random writes
        self.akey_use_array = FormattedParameter("-A", False)

        #   -s <number/string>
        #       Stride size, it is the offset distance between two array writes,
        #       it is also the default size for write if 'U' has no size
        #       parameter. The number can have 'K' or 'M' as postfix which
        #       stands for kilobyte or megabytes.
        self.stride_size = FormattedParameter("-s {}")

        #   -R <string>
        #       Execute a series of test commands:
        #       'U'    : Update test
        #       'F'    : Fetch test
        #       'V'    : Verify data consistency
        #       'O'    : OID table test (daos_perf only)
        #       'Q'    : Query test (vos_perf only)
        #       'I'    : VOS iteration test (vos_perf only)
        #       'P'    : Punch test (vos_perf only)
        #       'p'    : Output performance numbers
        #       'i=$N' : Iterate test $N times
        #       'k'    : Don't reset key for each iteration
        #       'o=$N' : Offset for update or fetch
        #       's=$N' : IO size for update or fetch
        #       'd'    : Dkey punch (for Punch test)
        #       'v'    : Verbose mode
        #       Test commands are in format of: "C;p=x;q D;a;b" The upper-case
        #       character is command, e.g. U=update, F=fetch, anything after
        #       semicolon is parameter of the command. Space or tab is the
        #       separator between commands.
        self.test_command = FormattedParameter("-R \"{}\"")

        #   -n <number/string>
        #       Number of strides per akey. The number can have 'k' or 'm' as
        #       postfix which stands for kilo or million.
        self.number_strides_per_akey = FormattedParameter("-n {}")

        #   -G <number/string>
        #       Random seed
        self.random_seed = FormattedParameter("-G {}")

        #   -w
        #       Pause after initialization for attaching debugger or analysis
        #       tool.
        self.pause_after_init = FormattedParameter("-w", False)

        #   -u <string>
        #       Specify an existing pool uuid
        self.pool_uuid = FormattedParameter("-u {}")

        #   -X <string>
        #       Specify an existing cont uuid
        self.cont_uuid = FormattedParameter("-X {}")

        #   -g <string>
        #       dmg configuration file
        self.dmg_config_file = FormattedParameter("-g {}")
