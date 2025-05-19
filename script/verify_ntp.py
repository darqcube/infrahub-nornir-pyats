from pyats import aetest
from pyats.topology import loader
from genie.testbed import load
from genie.utils.diff import Diff


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_devices(self):
        # Load testbed file
        testbed = load("testbed/ntp-testbed.yaml")
        device = testbed.devices["FT-RC-CloudCore-R1"]
        device.connect()
        self.parent.parameters.update(device=device)


class VerifyNTP(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.device = self.parent.parameters["device"]

    @aetest.test
    def verify_ntp_config(self):
        # Get NTP configuration
        ntp_config = self.device.parse("show running-config | include ntp")

        # Expected configuration
        expected_config = {
            "ntp server 216.239.35.12": True,
            "ntp source loopback0": True,
            "ntp master 3": True,
        }

        # Verify each NTP command
        for command, _ in expected_config.items():
            if command not in ntp_config:
                self.failed(f"NTP configuration missing: {command}")

    @aetest.test
    def verify_ntp_status(self):
        # Verify NTP is synchronized
        ntp_status = self.device.parse("show ntp status")
        if (
            not ntp_status["clock_state"].get("system_status", {}).get("status")
            == "synchronized"
        ):
            self.failed("NTP is not synchronized")


if __name__ == "__main__":
    aetest.main()
