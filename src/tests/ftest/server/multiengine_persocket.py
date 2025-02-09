"""
  (C) Copyright 2020-2022 Intel Corporation.

  SPDX-License-Identifier: BSD-2-Clause-Patent
"""

import time
import random
import base64
import traceback

from general_utils import run_pcmd, get_random_bytes
from ior_test_base import IorTestBase
from mdtest_test_base import MdtestBase
from pydaos.raw import DaosApiError
from server_utils_base import DaosServerCommand


class MultiEnginesPerSocketTest(IorTestBase, MdtestBase):
    # pylint: disable=too-many-ancestors
    """Daos server configuration tests.

    Test Class Description:
        Tests to verify that the multiple engines per socket on daos_server.

    :avocado: recursive
    """

    def __init__(self, *args, **kwargs):
        """Initialize a MultiEnginesPerSocketTest object."""
        super().__init__(*args, **kwargs)
        self.start_agents_once = False
        self.start_servers_once = False
        self.setup_start_agents = False
        self.setup_start_servers = False

    @staticmethod
    def create_data_set(num_attributes):
        """Create the large attribute dictionary.

        Args:
            num_attributes (int): number of attributes to be created on container.

        Returns:
            dict: a large attribute dictionary

        """
        data_set = {}
        for index in range(num_attributes):
            size = random.randint(1, 10)  # nosec
            key = str(index).encode("utf-8")
            data_set[key] = get_random_bytes(size)
        return data_set

    def verify_list_attr(self, indata, attributes_list):
        """Verify the length of the Attribute names.

        Args:
            indata (dict): Dict used to set attr
            attributes_list (list): List obtained from list attr
        """
        length = sum(map(len, indata.keys()))
        size = sum(map(len, attributes_list))

        self.log.info("Verifying list_attr output:")
        self.log.info("  set_attr names:  %s", list(indata.keys()))
        self.log.info("  set_attr size:   %s", length)
        self.log.info("  list_attr names: %s", attributes_list)
        self.log.info("  list_attr size:  %s", size)

        if length != size:
            self.fail(
                "FAIL: Size does not match for Names in list attr, Expected "
                "len={} and received len={}".format(length, size))
        # verify the Attributes names in list_attr retrieve
        for key in indata.keys():
            if key.decode() not in attributes_list:
                self.fail(
                    "FAIL: Name does not match after list attr, Expected "
                    "buf={} and received buf={}".format(key, attributes_list))

    def verify_get_attr(self, indata, outdata):
        """verify the Attributes value after get_attr.

        Args:
             indata (dict): In data item of container get_attr.
             outdata (dict): Out data from container get_attr.
        """
        decoded = {}
        for key, val in outdata.items():
            if isinstance(val, bytes):
                decoded[key.decode()] = val
            else:
                decoded[key] = base64.b64decode(val)

        self.log.info("Verifying get_attr output:")
        self.log.info("  get_attr data: %s", indata)
        self.log.info("  set_attr data: %s", decoded)

        for attr, value in indata.items():
            if value != decoded.get(attr.decode(), None):
                self.fail(
                    "FAIL: Value does not match after get({}), Expected "
                    "val={} and received val={}".format(attr, value,
                                                        decoded.get(attr.decode(), None)))

    def daos_server_storage_prepare_reset(self, step):
        """Perform daos_server storage prepare.

        Args:
             step (str): test step.
        """
        cmd = DaosServerCommand()
        cmd.sudo = False
        cmd.debug.value = False
        cmd.set_sub_command("scm")
        cmd.sub_command_class.set_sub_command("reset")
        cmd.sub_command_class.sub_command_class.force.value = True
        self.log.info(
            "===(%s.A)Starting daos_server scm reset: %s", step, str(cmd))
        results = run_pcmd(self.hostlist_servers, str(cmd), timeout=180)
        if results[0]['exit_status']:
            self.fail(
                "#({0}.A){1} failed, "
                "please make sure the server equipped with PMem modules".format(step, cmd))

    def daos_server_storage_prepare_ns(self, step, engines_per_socket=1):
        """Perform daos_server storage prepare --scm-ns-per-socket and reboot.

        Args:
             step (str): test step.
             engines_per_socket (int): number of engines per socket.
        """
        cmd = DaosServerCommand()
        cmd.sudo = False
        cmd.debug.value = False
        cmd.set_sub_command("scm")
        cmd.sub_command_class.set_sub_command("reset")
        cmd.sub_command_class.sub_command_class.scm_ns_per_socket.value = engines_per_socket
        cmd.sub_command_class.sub_command_class.force.value = True
        cmd.sub_command_class.sub_command_class.scm_only.value = True

        self.log.info(
            "===(%s.B)Starting daos_server storage prepare -S: %s", step, str(cmd))
        results = run_pcmd(self.hostlist_servers, str(cmd), timeout=180)
        if results[0]['exit_status']:
            self.fail(
                "#({0}.B){1} failed, "
                "please make sure the server equipped with {2} PMem "
                "modules.".format(step, cmd, engines_per_socket))
        time.sleep(15)
        self.host_reboot(self.hostlist_servers)

    def host_reboot(self, hosts):
        """To reboot the hosts.

        Args:
             hosts (NodeSet): hosts set to be rebooted.
        """
        reboot_waittime = self.params.get("reboot_waittime", "/run/server_config/*", default=210)
        cmd = "sudo shutdown -r now"
        run_pcmd(hosts, cmd, timeout=210)
        self.log.info("===Server %s rebooting... \n", hosts)
        time.sleep(reboot_waittime)

    def cleanup(self):
        """Servers clean up after test complete."""
        self.pool.destroy(recursive=1, force=1)
        cleanup_cmds = [
            "sudo systemctl stop daos_server.service",
            "sudo umount /mnt/daos*",
            "sudo wipefs -a /dev/pmem*",
            "/usr/bin/ls -l /dev/pmem*",
            'lsblk|grep -E "NAME|pmem"']
        for cmd in cleanup_cmds:
            run_pcmd(self.hostlist_servers, cmd, timeout=90)

    def test_multiengines_per_socket(self):
        """Test ID: DAOS-12076.

        Test description: Test multiple engines/sockets.
            (1) Storage prepare --scm-ns-per-socket
            (2) Start server
            (3) Start agent
            (4) Dmg system query
            (5) Pool create
            (6) Container create and attributes test
            (7) IOR test
            (8) MDTEST
            (9) Cleanup
        To launch test:
            (1) Make sure server is equipped with PMem
            (2) ./launch.py test_multiengines_per_socket -ts <servers> -tc <agent>

        :avocado: tags=manual
        :avocado: tags=server
        :avocado: tags=test_multiengines_per_socket
        """
        # (1) Storage prepare --scm-ns-per-socket
        step = 1
        self.log.info("===(%s)===Storage prepare --scm-ns-per-socket", step)
        self.daos_server_storage_prepare_reset(step)
        engines_per_socket = self.params.get(
            "engines_per_socket", "/run/server_config/*", default=1)
        self.daos_server_storage_prepare_ns(step, engines_per_socket)
        cmd = "/usr/bin/ls -l /dev/pmem*"
        results = run_pcmd(self.hostlist_servers, cmd, timeout=90)
        retry = 0
        max_retry = 3
        while results[0]['exit_status'] != 0 and retry < max_retry:
            retry += 1
            self.log.info("===(%s.%s retry)sleep 15 sec, retry server configure "
                          "daos_server_storage_prepare_ns", step, retry)
            time.sleep(15)
            results = run_pcmd(self.hostlist_servers, cmd, timeout=90)

        if retry > max_retry:
            self.cleanup()
            self.fail(
                "#PMem did not show after storage prepare --scm-ns-per-socket and {0} "
                "retries".format(max_retry))

        # (2) Start server
        step += 1
        self.log.info("===(%s)===Start server", step)
        start_server_cmds = [
            'lsblk|grep -E "NAME|pmem"',
            "sudo cp /etc/daos/daos_server.yml_4 /etc/daos/daos_server.yml",
            "sudo systemctl start daos_server.service"]
        for cmd in start_server_cmds:
            results = run_pcmd(self.hostlist_servers, cmd, timeout=90)
        # Check for server start status
        if results[0]['exit_status']:
            self.fail("#Fail on {0}".format(cmd))

        # (3) Start agent
        step += 1
        self.log.info("===(%s)===Start agent", step)
        start_agent_cmds = [
            "sudo systemctl start daos_agent.service",
            "dmg storage scan",
            "dmg network scan",
            "dmg storage format"]
        for cmd in start_agent_cmds:
            results = run_pcmd(self.hostlist_clients, cmd, timeout=90)
            # Check for agent start status
            if results[0]['exit_status'] and "sudo systemctl" in cmd:
                self.fail("#Fail on {0}".format(cmd))

        # (4) Dmg system query
        step += 1
        self.log.info("===(%s)===Dmg system query", step)
        # Delay is needed for multi ranks to show
        time.sleep(5)
        query_cmds = [
            "dmg system query",
            "dmg system query -v"]
        for cmd in query_cmds:
            results = run_pcmd(self.hostlist_clients, cmd, timeout=90)

        # (5) Pool create
        step += 1
        self.log.info("===(%s)===Pool create", step)
        self.add_pool(connect=False)

        # (6) Container create and attributes test
        step += 1
        self.log.info("===(%s)===Container create and attributes test", step)
        self.add_container(self.pool)
        self.container.open()
        daos_cmd = self.get_daos_command()
        num_attributes = self.params.get("num_attributes", '/run/attrtests/*')
        attr_dict = self.create_data_set(num_attributes)
        try:
            self.container.container.set_attr(data=attr_dict)
            data = daos_cmd.container_list_attrs(
                pool=self.pool.uuid,
                cont=self.container.uuid,
                verbose=False)
            self.verify_list_attr(attr_dict, data['response'])

            data = daos_cmd.container_list_attrs(
                pool=self.pool.uuid,
                cont=self.container.uuid,
                verbose=True)
            self.verify_get_attr(attr_dict, data['response'])
        except DaosApiError as excep:
            self.log.info(excep)
            self.log.info(traceback.format_exc())
            self.fail("#Test was expected to pass but it failed.\n")
        self.container.close()
        self.pool.disconnect()

        # (7) IOR test
        step += 1
        self.log.info("===(%s)===IOR test", step)
        ior_timeout = self.params.get("ior_timeout", '/run/ior/*')
        self.run_ior_with_pool(
            timeout=ior_timeout, create_pool=True, create_cont=True, stop_dfuse=True)

        # (8) MDTEST
        step += 1
        self.log.info("===(%s)===MDTEST", step)
        mdtest_params = self.params.get("mdtest_params", "/run/mdtest/*")
        self.run_mdtest_multiple_variants(mdtest_params)

        # (9) Cleanup
        step += 1
        self.log.info("===(%s)===Cleanup", step)
        cmd = "dmg system query -v"
        results = run_pcmd(self.hostlist_clients, cmd, timeout=90)
        self.cleanup()
