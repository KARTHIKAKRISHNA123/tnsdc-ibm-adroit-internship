# =============================================================
# MCP SERVER — Real-Time Tools (no mock data, no API keys needed)
# Exposes 3 live external APIs as MCP tools over stdio transport.
#
# Test standalone with MCP Inspector:
#   npx @modelcontextprotocol/inspector python mcp_server.py
# =============================================================

from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("realtime-tools")

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm",
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current, real-time weather for a given city name."""
    try:
        # Step 1: turn the city name into coordinates (free geocoding API)
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        ).json()

        results = geo.get("results")
        if not results:
            return f"Could not find a location named '{city}'."

        place = results[0]
        lat, lon = place["latitude"], place["longitude"]
        display_name = f"{place['name']}, {place.get('country', '')}"

        # Step 2: fetch the live current weather for those coordinates
        wx = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=10,
        ).json()

        current = wx.get("current_weather", {})
        code = current.get("weathercode")
        condition = WEATHER_CODES.get(code, "Unknown conditions")

        return (
            f"Weather in {display_name}: {condition}, "
            f"{current.get('temperature')}°C, "
            f"wind {current.get('windspeed')} km/h "
            f"(live data, fetched just now)"
        )
    except Exception as ex:
        return f"Weather lookup failed: {ex}"


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount of money from one currency to another using live, current exchange rates."""
    try:
        resp = requests.get(
            "https://api.frankfurter.app/latest",
            params={
                "amount": amount,
                "from": from_currency.upper(),
                "to": to_currency.upper(),
            },
            timeout=10,
        ).json()

        rate_result = resp.get("rates", {}).get(to_currency.upper())
        if rate_result is None:
            return f"Could not convert {from_currency} to {to_currency}. Check the currency codes."

        return (
            f"{amount} {from_currency.upper()} = {rate_result} {to_currency.upper()} "
            f"(live rate, date: {resp.get('date')})"
        )
    except Exception as ex:
        return f"Currency conversion failed: {ex}"



if __name__ == "__main__":
    # stdio transport = the server talks to its client over stdin/stdout,
    # exactly like the pattern used in the MCP Insurance labs.
    mcp.run(transport="stdio")