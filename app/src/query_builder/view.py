from fastapi import APIRouter, Request
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from src.query_builder.service import Service
# class InputDataItem(BaseModel):
#     question: Union[str, None]
#     response: Union[str, None]

class InputData(BaseModel):
    table_name: str
    input_data: Union[Dict[str, str], List[Dict[str, str]]]

router = APIRouter(
    tags=["query_builder"],
    responses={404: {"description": "Not found"}},
)

query_builder_service = Service()

def start_query_builder(request: Request, input_data: InputData):
    print(input_data)

    if True:#'cookie' in request.headers:

        if True: #validate auth token.
            sql_response = query_builder_service.run_sql_query_builder(input_data=input_data)

            return sql_response
        else:
            track.info(msg = "Unable to authenticate")
            return {"status": 401, "message": "Invalid access token", "success": False}, 401
    else:
        track.info(msg = "Cookie not found in request")
        return {"status": 400, "message": "Invalid cookie request", "success": False}, 400




@router.post("/organization/{organizationId}/query-builder")
async def upload(request: Request, input_data: InputData):
# async def upload(request: Request, chat: Union[Dict[str, str], List[Dict[str, str]]], table_name: str):
    response = start_query_builder(request=request,
                                   input_data=input_data)
    return response

