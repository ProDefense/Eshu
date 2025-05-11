import time
import logging
import asyncio
from typing import List, Dict

from pymetasploit3.msfrpc import MsfRpcClient
from eshu.base_C2 import BaseC2

logger = logging.getLogger(__name__)

class Metasploit(BaseC2):
    NAME = "metasploit"

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 55552,
        password: str = "changeme"
    ):
        """
        :param host:    msfrpcd host
        :param port:    msfrpcd port
        :param password: password you configured msfrpcd with
        """
        # connect synchronously; rpc client is thread-safe
        self._client = MsfRpcClient(password, server=host, port=port)
        logger.info("Connected to Metasploit RPC at %s:%d", host, port)

    @property
    def CLIENT(self) -> MsfRpcClient:
        return self._client
    
    def list_sessions(self) -> List[Dict[str, str]]:
        """
        Returns a list of active sessions with minimal info.
        """
        raw = self._client.sessions.list  # dict: { id: {...} }
        sessions = []
        for sid, info in raw.items():
            sessions.append({
                "session_id": str(sid),
                "type":       info.get("type", ""),
                "via_exploit": info.get("via_exploit", ""),
                "tunnel_peer": info.get("tunnel_peer", "")
            })
            logger.info(
                "Found session %s: type=%s, peer=%s",
                sid, info.get("type"), info.get("tunnel_peer")
            )
        return sessions

    def list_beacons(self) -> List[Dict]:
        """
        Metasploit has no beacons, so we return an empty list.
        """
        return []

    def send_beacon_cmd(self, beacon_id, commands):
        """
        No beacons in Metasploit.
        """
        raise NotImplementedError("Metasploit does not support beacons")

    def send_session_cmd(
        self,
        session_id: str,
        commands: List[str]
    ) -> List[str]:
        """
        Execute shell commands in a session. For Meterpreter sessions, drops into
        shell and uses run_shell_cmd_with_output; for others, falls back to runsingle
        or raw write/read.
        """
        if not commands:
            logger.debug("No commands to send to session %s", session_id)
            return []

        # lookup session (try as string ID then int)
        try:
            try:
                session = self._client.sessions.session(session_id)
            except KeyError:
                session = self._client.sessions.session(int(session_id))
        except Exception:
            raise ValueError(f"Session '{session_id}' not found")

        # figure out session type
        sess_type = None
        try:
            sess_type = session.info.get("type")  # e.g. "meterpreter" or "shell"
        except Exception:
            pass

        outputs: List[str] = []
        for cmd in commands:
            logger.debug("Sending to session %s: %s", session_id, cmd)
            try:
                # If it's a Meterpreter, drop into shell
                if sess_type == "meterpreter" and hasattr(session, "run_shell_cmd_with_output"):
                    # `end_strs` should match your shell prompt; adjust as needed
                    out = session.run_shell_cmd_with_output(cmd, end_strs=[session.sep], timeout=5, timeout_exception=False)
                    # optionally detach after each command, but run_shell_cmd_with_output does it for you

                # If it's already a raw shell session (type=="shell"), just runsingle
                elif sess_type == "shell" and hasattr(session, "runsingle"):
                    out = session.runsingle(cmd)

                # Otherwise, generic Meterpreter run_with_output
                elif hasattr(session, "run_with_output"):
                    out = session.run_with_output(cmd, end_strs=None)

                # Fallback: raw write/read
                else:
                    session.write(cmd)
                    time.sleep(0.5)
                    raw = session.read()
                    out = raw if isinstance(raw, str) else raw.decode("utf-8", errors="ignore")

                text = out.strip()
                outputs.append(text)
                logger.info("Session %s → %r", session_id, text)

            except Exception as e:
                err = f"Error on session {session_id} cmd '{cmd}': {e}"
                logger.error(err)
                outputs.append(err)

        return outputs


