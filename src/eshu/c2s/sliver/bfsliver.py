import os
import asyncio
import logging
from typing import List, Dict, Optional, Union

from sliver import SliverClient, SliverClientConfig
from sliver.beacon import InteractiveBeacon
from sliver.session import InteractiveSession  
from eshu.base_C2 import BaseC2

logger = logging.getLogger(__name__)


class Sliver(BaseC2):
    NAME = "sliver"

    def __init__(self, config_path: str):
        # Resolve absolute path, parse config, then connect
        config_file = os.path.abspath(config_path)
        self._config: SliverClientConfig = SliverClientConfig.parse_config_file(config_file)
        self._client: SliverClient = SliverClient(self._config)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._client.connect())
        logger.info("Connected to Sliver C2")

    def _run(self, coro):
        try:
            return self._loop.run_until_complete(coro)
        except RuntimeError:
            # in case loop was closed elsewhere, recreate it
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            return self._loop.run_until_complete(coro)

    @property
    def CLIENT(self) -> SliverClient:
        return self._client

    def list_sessions(self, timeout: int = 60) -> List[Dict[str,Union[str,int]]]:
        """Return a list of sessions as plain dicts."""
        try:
            raw = self._run(self._client.sessions(timeout=timeout))
        except Exception as e:
            logger.error("Error listing sessions: %s", e)
            return []

        sessions: List[Dict[str,Union[str,int]]] = []
        for s in raw:
            # pull out the attributes we care about
            sess = {
                "session_id":   getattr(s, "ID", None),
                "target_host":  getattr(s, "RemoteAddress", None),
                "platform":     getattr(s, "OS", None),
            }
            sessions.append(sess)

        return sessions

    def list_beacons(self, timeout: int = 60) -> List[Dict[str, str]]:
        """Return a list of active beacons as plain dicts."""
        try:
            raw = self._run(self._client.beacons(timeout=timeout))
        except Exception as e:
            logger.error("Error retrieving beacons: %s", e)
            return []

        if not raw:
            logger.warning("No Sliver beacons found.")
            return []

        beacons: List[Dict[str, str]] = []
        for b in raw:
            beacon = {
                "beacon_id":   getattr(b, "ID", None),
                "target_host": getattr(b, "RemoteAddress", None),
                "platform":    getattr(b, "OS", None),
            }
            beacons.append(beacon)
            logger.info(
                "Beacon %s — Host: %s, Platform: %s",
                beacon["beacon_id"], beacon["target_host"], beacon["platform"]
            )

        return beacons

    def send_beacon_cmd(
        self,
        beacon_id: str,
        commands: List[str]
    ) -> List[str]:
        """
        Execute a list of shell commands on the specified beacon.
        Returns a list of outputs (stdout or stderr).
        """
        if not commands:
            logger.debug("No commands provided for beacon %s", beacon_id)
            return []

        # Interact with the beacon
        try:
            beacon: InteractiveBeacon = self._run(
                self._client.interact_beacon(beacon_id)
            )
        except Exception as e:
            raise ValueError(f"Beacon with ID '{beacon_id}' not found. {e}")

        outputs: List[str] = []
        for cmd in commands:
            # split into program + args
            parts = cmd.split()
            logger.debug("Sending to %s: %s", beacon_id, parts)

            try:
                # execute returns a coroutine that yields a Response
                response = self._run(beacon.execute(parts[0], parts[1:]))
                stdout = response.Stdout.decode("utf-8", errors="ignore").strip()
                stderr = response.Stderr.decode("utf-8", errors="ignore").strip()

                if stdout:
                    outputs.append(stdout)
                elif stderr:
                    outputs.append(stderr)
                else:
                    outputs.append("")  # empty but successful
            except Exception as e:
                err = f"Error on beacon {beacon_id} cmd '{cmd}': {e}"
                logger.error(err)
                outputs.append(err)

        return outputs

    def send_session_cmd(
        self,
        session_id: str,
        commands: List[str]
    ) -> List[str]:
        """
        Execute a list of commands on the given Sliver session.
        :param session_id: the unique ID of the session to target
        :param commands:    a list of shell commands (strings)
        :returns:           list of stdout/stderr outputs
        """
        if not commands:
            logger.debug("No commands provided for session %s", session_id)
            return []

        # get an interactive session handle
        try:
            session: InteractiveSession = self._run(
                self._client.interact_session(session_id)
            )
        except Exception as e:
            raise ValueError(f"Session with ID '{session_id}' not found. {e}")

        outputs: List[str] = []
        for cmd in commands:
            parts = cmd.split()
            logger.debug("Sending to session %s: %s", session_id, parts)

            try:
                # assume `.execute` returns a coroutine that yields a Response-like object
                resp = self._run(session.execute(parts[0], parts[1:]))
                out = resp.Stdout.decode("utf-8", errors="ignore").strip()
                err = resp.Stderr.decode("utf-8", errors="ignore").strip()

                if out:
                    outputs.append(out)
                elif err:
                    outputs.append(err)
                else:
                    outputs.append("")  # no output, but no error
            except Exception as e:
                msg = f"Error on session {session_id} cmd '{cmd}': {e}"
                logger.error(msg)
                outputs.append(msg)

        return outputs