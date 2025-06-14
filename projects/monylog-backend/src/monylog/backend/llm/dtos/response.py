from monylog.shared_kernel.infra.fastapi.dtos.response import ResponseDto
from .schemas import MessageAnalyzedSchema


MessageAnalyzedResponse = ResponseDto[MessageAnalyzedSchema]
