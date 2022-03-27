#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os
# from dotenv import load_dotenv
# load_dotenv()

class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "914d56ad-325a-4577-8a40-928094a54de9")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "BbT7Q~yoCuJzQM44zSHAu5kCqjNR3RfqQ13ha")
    LUIS_APP_ID = os.environ.get("LuisAppId", "02e79a1d-9047-45ba-84ca-941a5500c455")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "0efb9c55e110407fa0468f94f15de1dc")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "0b563d44-bb61-4324-ab47-cf614cfe96fb"
    )
