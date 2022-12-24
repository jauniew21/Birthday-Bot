import asyncio
from datetime import date, datetime

today = datetime.now()
print(today)

async def change_today(today):
    # Changes today based on the time shift at midnight
    await asyncio.sleep(5)
    today = datetime.today()
    return today

def main():
    today = asyncio.run(change_today(today))
    print(today)

main()