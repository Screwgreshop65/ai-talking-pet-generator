"""Command-line entry point for the pet generator."""

from __future__ import annotations

import argparse
import asyncio
import sys

from petgen.core.pipeline import PetPipeline
from petgen.core.registry import StageRegistry
from petgen.config.loader import load_config


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="petgen", description="Generate a talking pet.")
    parser.add_argument("--profile", default="default_cat", help="Pet profile name.")
    parser.add_argument("--config", default=None, help="Path to a config override YAML.")
    parser.add_argument("--once", action="store_true", help="Single turn, then exit.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    config = load_config(profile=args.profile, override_path=args.config)
    registry = StageRegistry.default()
    pipeline = PetPipeline(config=config, registry=registry)
    try:
        asyncio.run(pipeline.run(once=args.once))
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())