import os
import toml
import logging
from typing import List, Dict, Optional, Union

from eshu.c2s.sliver.bfsliver import Sliver
from eshu.c2s.msf.metasploit import Metasploit
from eshu.base_C2 import BaseC2

logger = logging.getLogger(__name__)

C2_CLASS_MAP = {
    'sliver': Sliver,
    'metasploit': Metasploit,
}

class C2Orchestrator:
    """
    Orchestrates multiple C2 frameworks based on a TOML config.
    """
    def __init__(self, config_file: str):
        logger.debug("Initializing C2Orchestrator with config: %s", config_file)
        if not os.path.isfile(config_file):
            logger.error("Config file not found: %s", config_file)
            raise FileNotFoundError(f"Config file not found: {config_file}")

        self.config = toml.load(config_file)
        self.c2_instances: List[BaseC2] = []
        self._load_c2s()

        loaded = [inst.NAME for inst in self.c2_instances]
        logger.info("Loaded frameworks: %s", loaded)

    def _load_c2s(self):
        entries = self.config.get('c2', {})
        logger.debug("Config sections found for C2: %s", list(entries.keys()))

        for c2_type, configs in entries.items():
            cls = C2_CLASS_MAP.get(c2_type)
            if not cls:
                logger.warning("Unknown C2 type in config: %s", c2_type)
                continue

            for entry in configs:
                alias = entry.pop("name", None)
                logger.debug("Instantiating %s with params: %s", c2_type, entry)
                try:
                    inst = cls(**entry)
                except Exception as e:
                    logger.error("Failed to initialize %s: %s", c2_type, e, exc_info=True)
                    continue

                inst.alias = alias
                self.c2_instances.append(inst)
                logger.info("Initialized C2 instance: %s (alias=%s)", c2_type, alias)

    def get_all_sessions(
        self,
        c2_names: Optional[List[str]] = None
    ) -> List[Dict[str, Union[str, int]]]:
        sessions = []
        for inst in self.c2_instances:
            if c2_names and inst.NAME not in c2_names:
                logger.debug("Skipping %s (not in filter %s)", inst.NAME, c2_names)
                continue

            logger.debug("Fetching sessions from %s", inst.NAME)
            raw = inst.list_sessions()
            logger.debug("%s.list_sessions() returned %r", inst.NAME, raw)

            for s in raw:
                if isinstance(s, dict):
                    sess = s.copy()
                else:
                    sess = {
                        "session_id": getattr(s, "session_id", None) or getattr(s, "ID", None),
                        "type":       getattr(s, "type", None)       or getattr(s, "Type", None),
                        "via_exploit":getattr(s, "via_exploit", None),
                        "tunnel_peer":getattr(s, "tunnel_peer", None),
                    }
                sess["c2"] = inst.NAME
                sessions.append(sess)
                logger.info("Discovered session: %s", sess)
        return sessions

    def get_all_beacons(
        self,
        c2_names: Optional[List[str]] = None
    ) -> List[Dict[str, Union[str, int]]]:
        beacons = []
        for inst in self.c2_instances:
            if c2_names and inst.NAME not in c2_names:
                logger.debug("Skipping %s for beacons (filter %s)", inst.NAME, c2_names)
                continue

            logger.debug("Fetching beacons from %s", inst.NAME)
            raw = inst.list_beacons()
            logger.debug("%s.list_beacons() returned %r", inst.NAME, raw)

            for b in raw:
                beacon = b.copy() if isinstance(b, dict) else {
                    "beacon_id":   getattr(b, "beacon_id", None) or getattr(b, "ID", None),
                    "target_host": getattr(b, "target_host", None) or getattr(b, "RemoteAddress", None),
                    "platform":    getattr(b, "platform", None)    or getattr(b, "OS", None),
                }
                beacon["c2"] = inst.NAME
                beacons.append(beacon)
                logger.info("Discovered beacon: %s", beacon)
        return beacons

    def run_on_sessions(
        self,
        commands: List[str],
        c2_names: Optional[List[str]] = None,
        os_types: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        results = {}
        for inst in self.c2_instances:
            if c2_names and inst.NAME not in c2_names:
                logger.debug("Skipping %s for run_on_sessions (filter %s)", inst.NAME, c2_names)
                continue

            for sess in inst.list_sessions():
                target_os = sess.get('platform') or sess.get('type')
                if os_types and target_os not in os_types:
                    logger.debug("Skipping session %s (OS filter %s)", sess, os_types)
                    continue

                sid = sess.get('session_id') or sess.get('beacon_id')
                key = f"{inst.NAME}:{sid}"
                logger.info("Running commands on session %s: %s", key, commands)
                results[key] = inst.send_session_cmd(sid, commands)
        return results

    def run_on_beacons(
        self,
        commands: List[str],
        c2_names: Optional[List[str]] = None,
        os_types: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        results = {}
        for inst in self.c2_instances:
            if c2_names and inst.NAME not in c2_names:
                logger.debug("Skipping %s for run_on_beacons (filter %s)", inst.NAME, c2_names)
                continue

            for beacon in inst.list_beacons():
                target_os = beacon.get('platform')
                if os_types and target_os not in os_types:
                    logger.debug("Skipping beacon %s (OS filter %s)", beacon, os_types)
                    continue

                bid = beacon.get('beacon_id')
                key = f"{inst.NAME}:{bid}"
                logger.info("Running commands on beacon %s: %s", key, commands)
                results[key] = inst.send_beacon_cmd(bid, commands)
        return results

def main():
    import argparse
    import logging as _logging

    parser = argparse.ArgumentParser(
        description="Run commands across all configured C2 frameworks"
    )
    parser.add_argument("config", help="path to your config.toml")
    parser.add_argument(
        "--list-sessions", action="store_true", help="List all sessions"
    )
    parser.add_argument(
        "--list-beacons", action="store_true", help="List all beacons"
    )
    parser.add_argument(
        "--cmd", nargs="+", help="Command(s) to run on all sessions"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level"
    )
    args = parser.parse_args()

    _logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=getattr(_logging, args.log_level),
    )

    orch = C2Orchestrator(args.config)

    if args.list_sessions:
        for s in orch.get_all_sessions():
            print(s)
    elif args.list_beacons:
        for b in orch.get_all_beacons():
            print(b)
    elif args.cmd:
        res = orch.run_on_sessions(args.cmd)
        for k, out in res.items():
            print(f"== {k} ==")
            for line in out:
                print(line)
    else:
        parser.print_help()
