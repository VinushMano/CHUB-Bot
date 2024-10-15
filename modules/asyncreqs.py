import aiohttp


async def get(*args, **kwargs) -> aiohttp.ClientResponse:
    session = kwargs.pop('session') if 'session' in kwargs else None
    if session is None:
        # this api request has to be done with no session because of how disnake
        # autocomplete works
        if not args[0].startswith('https://api.ragingenby.dev/stem'):
            print('WARNING: Request to', args[0], 'is being made with no session,'
                  'this will slow the bot down. Ensure this is intentional.')
        async with aiohttp.ClientSession() as session:
            return await get(*args, session=session, **kwargs)
    async with session.get(*args, **kwargs) as response:
        await response.text()  # wait for response to go through (async can be buggy so this is somewhat needed)
        return response
        