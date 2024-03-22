"""Main module executed by the Dockerfile."""

import asyncio
import logging

from uvicorn import Config, Server

from back.config import ApplicationConfig

log = logging.getLogger(__name__)

servers: list["MultiServer"] = []


def cancel_all_tasks(exclude_current=False) -> None:
    """Cancel all asyncio tasks to force exiting on Ctrl+C.
    Necessary only because of the game infinite loop.
    TODO: find cleaner solution.
    """
    all_tasks = asyncio.all_tasks()
    if exclude_current and (current_task := asyncio.current_task()):
        all_tasks.remove(current_task)
    for task in all_tasks:
        task.cancel()


class MultiServer(Server):
    """Server listening on one port and accepting other servers in parallel."""

    def __init__(self, on_shutdown, *args, **kwargs) -> None:
        self.on_shutdown = on_shutdown
        super().__init__(*args, **kwargs)

    async def async_run(self, sockets=None) -> None:
        """Same implementation as :meth:`~Server.run` but in async."""
        self.config.setup_event_loop()
        await self.serve(sockets=sockets)

    async def shutdown(
        self,
        *args,
        **kwargs,
    ) -> None:  # pragma: no cover (can only be called in prod)
        """Shutdown the server and notify the others."""
        self.on_shutdown()
        cancel_all_tasks()
        return await super().shutdown(*args, **kwargs)


def exit_application() -> None:
    """Exit the application."""
    log.info("exiting the backend")
    for server in servers:
        server.should_exit = True


async def main() -> None:
    """Main function executed by the Dockerfile."""
    app_config: ApplicationConfig = ApplicationConfig()

    for app, port in (
        ("back.api.routes:app", api_port := app_config.api.port),
        (
            "back.api.monitoring:app",
            monitoring_port := app_config.api.monitoring_port,
        ),
    ):
        # WARNING: when providing the default log_config, it disabled all existing loggers, and we loose some logs.
        config = Config(app, host="0.0.0.0", port=port, log_config=None)
        servers.append(MultiServer(config=config, on_shutdown=exit_application))

    log.info(
        f"the backend is ready and listen on {api_port} (API) and {monitoring_port} (monitoring)",
    )
    # By using a dedicated port for monitoring features (healthcheck, metrics, changing log level, etc.),
    # and not exposing it, the front can't have access to these features. It's more risky to expect
    # an API Gateway blocking the access to /monitoring path.
    await asyncio.gather(*(server.async_run() for server in servers))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
