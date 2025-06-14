from fastapi import Request
from fastapi.responses import JSONResponse
from monylog.shared_kernel.domain.exception import BaseMsgException


async def custom_exception_handler(request: Request, exe: BaseMsgException):
    return JSONResponse(
        status_code=exe.code,
        content={
            "method": request.method,
            "path": request.url.path,
            "request_id": request.state.correlation_id,
            "detail": exe.message,
            "error": exe.error,
            "status_code": exe.code,
        },
    )
