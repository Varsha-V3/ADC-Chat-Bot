#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "6552af1b-2f8f-44be-af69-0469067df59e")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "a6958ce9-5d0c-4cf8-8f3a-d2700ef08568")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://qnaadcbot.azurewebsites.net/qnamaker")
