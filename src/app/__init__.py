from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.openpi_examples import examples as component_examples
from app.routers import ROUTERS


def _register_routers(app: FastAPI) -> None:
    for router in ROUTERS:
        app.include_router(router)


def _init_python_dependency_injector(app: FastAPI) -> None:
    from app.di_container import ServiceDIContainer  # pylint: disable=import-outside-toplevel

    container = ServiceDIContainer()
    app.container = container


def _custom_openapi(app: FastAPI) -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    openapi_schema.setdefault('components', {})
    openapi_schema['components'].setdefault('examples', {})
    openapi_schema['components']['examples'].update(component_examples)

    app.openapi_schema = openapi_schema
    return openapi_schema


def create_app() -> FastAPI:
    app = FastAPI(
        title='Transaction HUB API',
    )

    _init_python_dependency_injector(app)
    _register_routers(app)
    # NOTE: `FastAPI` expects `app.openapi` to be a callable (a function/method)
    app.openapi = lambda: _custom_openapi(app)

    return app
