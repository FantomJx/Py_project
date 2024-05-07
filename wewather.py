"""
import python_weather
import asyncio
import os

async def getweather():
  async with python_weather.Client(format=python_weather.IMPERIAL, locale="bg-BG") as client:
    weather = await client.get("Stara Zagora")
    celsius= (weather.current.temperature - 32) *5/9
    print(str(round(celsius)) + "°")
    print(weather.current)
    print(weather.location.index)
if __name__ == "__main__":
  if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(getweather())
"""
# import the module
import asyncio
import os
import python_weather
async def getweather():
  async with python_weather.Client(format=python_weather.IMPERIAL) as client:

    weather = await client.get("Sofia")
  
    celsius= (weather.current.temperature - 32) *5/9
    print(str(round(celsius)) + "°")
  
    for forecast in weather.forecasts:
      print(forecast.date, forecast.astronomy)
  
      # hourly forecasts
      #for hourly in forecast.hourly:
       #print(f' --> {hourly!r}')

if __name__ == "__main__":
  if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(getweather())