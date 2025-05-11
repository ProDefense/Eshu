#!/usr/bin/env python3
import argparse
import logging
from eshu import C2Orchestrator

def main():
    parser = argparse.ArgumentParser(
        description="Example: connect to all configured C2s and run commands"
    )
    parser.add_argument(
        "config",
        help="Path to your config.toml"
    )
    parser.add_argument(
        "--sessions",
        action="store_true",
        help="List all sessions"
    )
    parser.add_argument(
        "--beacons",
        action="store_true",
        help="List all beacons"
    )
    parser.add_argument(
        "--cmd",
        nargs="+",
        help="Command(s) to run on all sessions"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"],
        help="Logging verbosity"
    )
    args = parser.parse_args()

    # configure logging
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=getattr(logging, args.log_level),
    )

    # load orchestrator
    orch = C2Orchestrator(args.config)

    if args.sessions:
        print("=== Sessions ===")
        for s in orch.get_all_sessions():
            print(f"{s['c2']} | {s['session_id']} | {s.get('platform','')}")

    if args.beacons:
        print("=== Beacons ===")
        for b in orch.get_all_beacons():
            print(f"{b['c2']} | {b['beacon_id']} | {b.get('platform','')}")

    if args.cmd:
        print(f"=== Running {args.cmd} on all sessions ===")
        results = orch.run_on_sessions(args.cmd)
        for key, out_lines in results.items():
            print(f"\n-- {key} --")
            for line in out_lines:
                print(line)

if __name__ == "__main__":
    main()
