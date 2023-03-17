import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

import aiohttp_cors
import strawberry
from aiohttp import web
from graphql import GraphQLError
from strawberry.aiohttp.views import GraphQLView
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from strawberry.types import ExecutionContext

import coniql.strawberry_schema as schema

from . import __version__

module_logger = logging.getLogger(__name__)


def create_schema(debug: bool):
    # Create the schema
    return strawberry.Schema(
        query=schema.Query,
        subscription=schema.Subscription,
        mutation=schema.Mutation,
    )


def create_app(use_cors: bool, debug: bool, graphiql: bool):

    # Create the schema
    strawberry_schema = create_schema(debug)

    # Create the GraphQL view to attach to the app
    view = GraphQLView(
        schema=strawberry_schema,
        subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL],
        graphiql=graphiql,
    )

    # Create app
    app = web.Application()
    # Add routes
    app.router.add_route("GET", "/ws", view)
    app.router.add_route("POST", "/ws", view)
    app.router.add_route("POST", "/graphql", view)
    # Enable CORS for all origins on all routes (if applicable)
    if use_cors:
        cors = aiohttp_cors.setup(app)
        for route in app.router.routes():
            allow_all = {
                "*": aiohttp_cors.ResourceOptions(
                    allow_headers=("*"), max_age=3600, allow_credentials=True
                )
            }
            cors.add(route, allow_all)
    module_logger.debug("Example")
    return app


def set_up_logging(debug: bool = False) -> None:
    class OptionalTraceFormatter(logging.Formatter):
        def __init__(self, debug: bool = False) -> None:
            self.debug = debug
            # Can also set or pass through the other args like format
            super().__init__()

        def formatStack(self, stack_info: str) -> str:
            """Optionally suppress stack trace output"""
            if self.debug:
                return ""
            return super().formatStack(stack_info)

    # Handler to print to stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if debug else logging.ERROR)
    console.setFormatter(OptionalTraceFormatter(debug))

    # Attach it to coniql and strawberry logger
    strawberry_logger = logging.getLogger("strawberry")
    strawberry_logger.addHandler(console)
    coniql_logger = logging.getLogger("coniql")
    coniql_logger.addHandler(console)


def main(args=None) -> None:
    """
    Entry point of the application.
    """
    parser = ArgumentParser(description="CONtrol system Interface over graphQL")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "config_paths",
        metavar="PATH",
        type=Path,
        nargs="*",
        help="Paths to .coniql.yaml files describing Channels and Devices",
    )
    parser.add_argument(
        "--cors",
        action="store_true",
        default=False,
        help="Allow CORS for all origins and routes",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Print stack trace on errors",
    )
    parser.add_argument(
        "--graphiql",
        action="store_true",
        default=False,
        help="Enable GraphiQL for testing at localhost:8080/ws",
    )
    parsed_args = parser.parse_args(args)

    set_up_logging(parsed_args.debug)

    app = create_app(parsed_args.cors, parsed_args.debug, parsed_args.graphiql)
    web.run_app(app)
