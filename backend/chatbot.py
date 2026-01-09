from langgraph.graph import StateGraph, START,END
from schemas.ChatResponseState import ChatState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from llm.Model import get_llm
import aiosqlite
from tools.StockPriceTool import get_stock_price
from tools.SerachTool import search_tool
from utility.ToolHelper import load_mcp_tools,create_chat_node
from mcpclient.McpLocalClient import get_mcp_client
import os
from dotenv import load_dotenv


#load env
load_dotenv()

#get model and mcp client
llm = get_llm()
client = get_mcp_client()


DB_PATH = "chatbot.db"

async def get_saver():
    conn = await aiosqlite.connect(DB_PATH)
    return AsyncSqliteSaver(conn)

# ---------- Graph Builder ----------
async def build_chatbot():

    mcp_tools = await load_mcp_tools(client)
    tools = [search_tool, get_stock_price, *mcp_tools]
    llm_with_tools = llm.bind_tools(tools)
    chat_node = create_chat_node(llm_with_tools)


    graph = StateGraph(ChatState)
    graph.add_node("chat", chat_node)
    graph.add_node("tools", ToolNode(tools))
    

    graph.add_edge(START, "chat")
    # If tool is needed → tools
    # If tool is NOT needed → END
    graph.add_conditional_edges(
        "chat",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        }
    )
    # After tools run → back to chat
    graph.add_edge("tools", "chat")


    conn = await aiosqlite.connect("chatbot.db")
    saver = AsyncSqliteSaver(conn)

    return graph.compile(
        checkpointer=saver
    )



