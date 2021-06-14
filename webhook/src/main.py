from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field


# String format when returning date/time
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


app = FastAPI(
    title="Interview Chat Bot Webhook",
    description="Webhook integration with IBM Watson Assistant"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)


class TimeZoneRequest(BaseModel):
    '''
    Request model for the timezone webhook.
    '''
    timezone: str = Field(
        'America/Toronto',
        title='Time zone',
        description='The time zone (ex: America/Toronto)'
    )


class TimeZoneResponse(BaseModel):
    '''
    Response model for the timezone webhook.
    '''
    timezone: str = Field(
        title='Time zone',
        description='The time zone as reported by the chat bot'
    )

    utc: str = Field(
        title='UTC time',
        description='Current UTC time - formatted as a string'
    )

    local: str = Field(
        title='Local time',
        description='Current local time - formatted as a string'
    )

    offset: str = Field(
        title='Offset',
        description='Offset (in hours) between local and UTC time - formatted as a string'
    )


@app.post("/v1/timezone/webhook", response_model=TimeZoneResponse)
async def timezone_webhook(request: TimeZoneRequest):
    '''
    Given a user's time zone - calculate the offset in hours from the current UTC time.
    '''
    # The users time zone (as reported from the chat bot)
    user_tz = timezone(request.timezone)

    # Get the current UTC time with time zone information
    utc_with_tz = timezone('utc').localize(datetime.utcnow())

    # Strip out the time zone information from the UTC time
    utc_no_tz = utc_with_tz.replace(tzinfo=None)

    # Get the local time from the UTC time
    # Strip out the time zone information
    local_no_tz = utc_with_tz.astimezone(user_tz).replace(tzinfo=None)

    # Calculate the delta (in hours) between the two datetime objects
    offset_hours = relativedelta(utc_no_tz, local_no_tz).hours

    # Convert offset to a string prefixed with: +/-
    if offset_hours > 0:
        offset_hours_str = f'+{offset_hours}'
    elif offset_hours < 0:
        offset_hours_str = f'-{offset_hours}'
    else:
        offset_hours_str = '0'

    return TimeZoneResponse(
        timezone=request.timezone,
        utc=utc_no_tz.strftime(TIME_FORMAT),
        local=local_no_tz.strftime(TIME_FORMAT),
        offset=offset_hours_str)
