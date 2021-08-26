import asyncio

import aioboto3
import httpx

PENNSIEVE_URL = "https://api.pennsieve.io"
api_key = "..."
api_secret = "..."


async def the_function():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{PENNSIEVE_URL}/authentication/cognito-config")
        r.raise_for_status()

        cognito_app_client_id = r.json()["tokenPool"]["appClientId"]
        cognito_region = r.json()["region"]

        session = aioboto3.Session()
        async with session.resource("cognito-idp", region_name=cognito_region, aws_access_key_id="", aws_secret_access_key="") as cognito_idp_client:
            login_response = cognito_idp_client.initiate_auth(AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": api_token, "PASSWORD": api_secret},
                ClientId=cognito_app_client_id,
                )



if __name__ == "__main__":
    asyncio.run(the_function())
