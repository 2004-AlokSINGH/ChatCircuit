from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calculator-server")


def as_number(value) -> float:
    """
    Safely convert input to float.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid number: {value}")


@mcp.tool()
async def add(first_num: float, second_num: float) -> dict:
    a = as_number(first_num)
    b = as_number(second_num)
    return {
        "operation": "add",
        "first_num": a,
        "second_num": b,
        "result": a + b,
    }


@mcp.tool()
async def subtract(first_num: float, second_num: float) -> dict:
    a = as_number(first_num)
    b = as_number(second_num)
    return {
        "operation": "subtract",
        "first_num": a,
        "second_num": b,
        "result": a - b,
    }


@mcp.tool()
async def multiply(first_num: float, second_num: float) -> dict:
    a = as_number(first_num)
    b = as_number(second_num)
    return {
        "operation": "multiply",
        "first_num": a,
        "second_num": b,
        "result": a * b,
    }


@mcp.tool()
async def divide(first_num: float, second_num: float) -> dict:
    a = as_number(first_num)
    b = as_number(second_num)

    if b == 0:
        return {"error": "Division by zero is not allowed"}

    return {
        "operation": "divide",
        "first_num": a,
        "second_num": b,
        "result": a / b,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
