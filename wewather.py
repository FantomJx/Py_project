import python_weather


async def getweather(town):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get('town')

        celsius = (weather.current.temperature - 32) * 5 / 9
        round(celsius)

        for daily in weather.daily_forecasts:
            print(daily)

