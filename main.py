import asyncio
from dotenv import load_dotenv
from apps.main import main


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
