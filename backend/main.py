from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
from schemas.ChatRequestState import ChatRequest
from chatbot import build_chatbot,get_saver
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LangGraph MCP Chat API")



@app.get("/threads")
async def list_threads():
    saver = await get_saver()

    all_threads = set()
    async for checkpoint in saver.alist(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)



@app.get("/conversation/{thread_id}")
async def get_conversation(thread_id: str):
    chatbot = app.state.chatbot
    chat_state = await chatbot.aget_state(config={"configurable": {"thread_id": thread_id}})
    if not chat_state:
        return []
    state = chat_state.values  
    messages = state.get("messages", [])
    formatted = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted.append({
                "role": "user",
                "content": msg.content
            })
        elif isinstance(msg, AIMessage):
            formatted.append({
                "role": "assistant",
                "content": msg.content
            })
    return formatted




@app.on_event("startup")
async def startup_event():
    app.state.chatbot = await build_chatbot()


@app.post("/chat")
async def chat(req: ChatRequest):
    chatbot = app.state.chatbot
    thread_id = req.thread_id or str(uuid.uuid4())
    tools_used = []
    
    try:
        result = await chatbot.ainvoke(
            {"messages": [HumanMessage(content=req.message)]},
            config={
                "configurable": {"thread_id": thread_id},
                "metadata": {"thread_id": thread_id},
                "recursion_limit": 20,   # MAX tool ↔ chat loops
            },
        )
        
        # Extract tools used from messages
        messages = result.get("messages", [])
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name", "")
                    # Map tool names to friendly server names
                    if tool_name not in tools_used:
                        tools_used.append(tool_name)
        
        # Map tool names to friendly display names
        tool_display_names = []
        for tool in tools_used:
            if tool == "create_jira_ticket":
                tool_display_names.append("🎫 Jira MCP Server")
            elif tool in ["add", "subtract", "multiply", "divide"]:
                tool_display_names.append("🧮 Calculator MCP Server")
            elif tool == "search_tool":
                tool_display_names.append("🔍 DuckDuckGo Search")
            elif tool == "get_stock_price":
                tool_display_names.append("📈 Stock Price Tool")
            else:
                tool_display_names.append(f"🔧 {tool}")
        
        return {
            "thread_id": thread_id,
            "response": result["messages"][-1].content,
            "tools_used": list(set(tool_display_names)),  
        }
    except Exception as e:
        print(e)
        return {
            "thread_id": thread_id,
            "response": "Stopped due to excessive tool calls. Please rephrase or try again later",
            "tools_used": tools_used,
        }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
