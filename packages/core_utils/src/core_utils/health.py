"""
core_utils.health – health-check routes for FastAPI services.

Provides attach_health_routes() to wire /healthz and /readyz with
custom liveness and readiness checks.
"""

import asyncio
from typing import Awaitable, Callable, Mapping, Union

from fastapi import APIRouter, FastAPI, Request
from core_config import get_settings

# A health check can return:
#  - bool
#  - dict (arbitrary JSON body)
#  - Awaitable of either
HealthCheck = Callable[[], Union[bool, dict, Awaitable[Union[bool, dict]]]]
HealthChecks = Mapping[str, HealthCheck]


def attach_health_routes(app: FastAPI, *, checks: HealthChecks) -> None:
    """
    Register health-check endpoints on the app.

    Args:
        app: FastAPI application
        checks: mapping with keys "liveness" and/or "readiness" to callables.
            Liveness check should return bool or dict.
            Readiness check should return bool or dict.

    Endpoints:
<<<<<<< HEAD
        GET /healthz -> { "status": "ok" | "fail" } or custom dict.
=======
        GET /healthz -> { "ok": <bool> } or custom dict.
>>>>>>> origin/main
        GET /readyz -> readiness check result directly if dict, or
                       { "ready": <bool> }.
    """
    router = APIRouter()

    async def _run_check(fn: HealthCheck) -> Union[bool, dict]:
        try:
            res = fn()
            if asyncio.iscoroutine(res):
                res = await res
            return res
        except Exception:
            return False

<<<<<<< HEAD
    # Optional rate limiter (e.g., slowapi); no-op if absent.
    limiter = getattr(app.state, "limiter", None)
    _default_limit = get_settings().api_rate_limit_default

    def _limit(fn):
        return limiter.limit(_default_limit)(fn) if limiter else fn

    # ── Liveness ────────────────────────────────────────────────────────────
    if "liveness" in checks:
        @_limit
        @router.get("/healthz")
        async def _healthz(request: Request):
=======
    limiter = getattr(app.state, "limiter", None)
    _default_limit = get_settings().api_rate_limit_default
    def _limit(fn):             # no-op when limiter is absent
        return limiter.limit(_default_limit)(fn) if limiter else fn

    # Liveness endpoint
    if "liveness" in checks:
        @_limit
        @router.get("/healthz")
        async def _healthz(request: Request):         # ← accept request
>>>>>>> origin/main
            res = await _run_check(checks["liveness"])
            if isinstance(res, dict):
                return res
            return {"status": "ok" if bool(res) else "fail"}
<<<<<<< HEAD

        # Back-compat alias some stacks probe
        @_limit
        @router.get("/health")
        async def _health_alias(request: Request):
            return await _healthz(request)
    else:
        @router.get("/healthz")
        async def _healthz_default(request: Request):
            return {"status": "ok"}

        @router.get("/health")
        async def _health_alias_default(request: Request):
            return await _healthz_default(request)

    # ── Readiness ───────────────────────────────────────────────────────────
    if "readiness" in checks:
        @_limit
        @router.get("/readyz")
        async def _readyz(request: Request):
=======
    else:
        @router.get("/healthz")
        async def _healthz_default(request: Request): # ← accept request
            return {"status": "ok"}

    # Readiness endpoint
    if "readiness" in checks:
        @_limit
        @router.get("/readyz")
        async def _readyz(request: Request): 
>>>>>>> origin/main
            res = await _run_check(checks["readiness"])
            if isinstance(res, dict):
                return res
            return {"ready": bool(res)}
<<<<<<< HEAD

        # Typo/back-compat alias (some probes use /rdyz by mistake)
        @_limit
        @router.get("/rdyz")
        async def _rdyz_alias(request: Request):
            return await _readyz(request)
    else:
        @router.get("/readyz")
        async def _readyz_default(request: Request):
            return {"ready": True}

        @router.get("/rdyz")
        async def _rdyz_alias_default(request: Request):
            return await _readyz_default(request)

=======
    else:
        @router.get("/readyz")
        async def _readyz_default(request: Request):  # ← accept request
            return {"ready": True}

>>>>>>> origin/main
    app.include_router(router)
