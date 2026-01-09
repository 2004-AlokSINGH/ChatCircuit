from langchain_core.tools import tool, BaseTool
from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode, tools_condition
from schemas.ChatResponseState import ChatState


async def load_mcp_tools(client) -> list[BaseTool]:
    return await client.get_tools()

# ---------- Chat Node ----------
def create_chat_node(llm_with_tools):
    async def chat_node(state: ChatState):
        response = await llm_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}
    return chat_node







