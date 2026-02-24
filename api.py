# from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from fastapi import FastAPI, UploadFile, File
import base64
# from mcp.client.sse import sse_client
app = FastAPI()

MCP_URL = "http://localhost:8050/mcp"

@app.get("/add")
async def add_numbers(a: int, b: int):
    async with streamablehttp_client(MCP_URL) as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("add", arguments={"a": a, "b": b})
            return {"result": result.content[0].text}
        

@app.get("/sub")
async def sub_numbers(a: int, b: int):
    async with streamablehttp_client(MCP_URL) as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("sub", arguments={"a": a, "b": b})
            return {"result": result.content[0].text}
        



@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    # 1️⃣ Read uploaded file
    file_bytes = await file.read()

    # 2️⃣ Convert to base64
    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    # 3️⃣ Get filename automatically
    file_name = file.filename

    async with streamablehttp_client(MCP_URL) as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "extract_text_from_document",
                arguments={
                    "file_name": file_name,
                    "file_base64": file_base64
                },
            )

            return {
                "filename": file_name,
                "extracted_text": result.content[0].text
            }