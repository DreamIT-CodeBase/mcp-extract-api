from mcp.server.fastmcp import FastMCP
import requests
import os

AZURE_ENDPOINT = "https://ditcs-ai-func-app-f7h8bbe0badyd3et.canadacentral-01.azurewebsites.net/api/extract-text"

# Create an MCP server
mcp = FastMCP(
    name="Extract tool",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    # port=8050,  # only used for SSE transport (set this to any port)
    port=int(os.getenv("PORT", 8050)),
    stateless_http=True,
)


@mcp.tool()
def extract_text_from_document(file_name: str, file_base64: str) -> str:
    """
    Extract text from PDF or DOCX using Azure OCR.
    file_name: name of file (example: sample.pdf)
    file_base64: base64 encoded file content
    """

    ext = os.path.splitext(file_name)[1].lower()

    if ext == ".pdf":
        content_type = "application/pdf"
    elif ext == ".docx":
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        return "Unsupported file type"

    payload = {
        "$content-type": content_type,
        "$content": file_base64
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(AZURE_ENDPOINT, headers=headers, json=payload)

    # Safe handling
    try:
        result = response.json()
        return str(result)
    except Exception:
        return f"Error: {response.status_code} - {response.text}"



# Run the server
if __name__ == "__main__":
     print("Running server with Streamable HTTP transport")
     mcp.run(transport="streamable-http")