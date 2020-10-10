# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)

from data_models import WelcomeUserState
from flask import Config

from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
# def __init__(self, config: Config):
#    self.qna_maker = QnAMaker(
#       QnAMakerEndpoint(
#          knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
#          endpoint_key=config.QNA_ENDPOINT_KEY,
#          host=config.QNA_ENDPOINT_HOST,
#    )
# )

class WelcomeUserBot(ActivityHandler):
    def __init__(self, user_state: UserState,config: Config):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST,
            ))

        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")

        self.WELCOME_MESSAGE = """Type 'hello', 'hi','bye', 'docs' and 'intro' to explore more. Try it now, type 'hi'"""

        self.INFO_MESSAGE = """Welcome to ADC CHAT BOT"""

        self.LOCALE_MESSAGE = """" """

        self.PATTERN_MESSAGE = """Type 'hello', 'hi','bye', 'docs' and 'intro' to explore more. Try it now, type 'hi'"""

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(self.INFO_MESSAGE)

                await turn_context.send_activity(self.WELCOME_MESSAGE)



                # await turn_context.send_activity(
                #     f"{ self.LOCALE_MESSAGE } Current locale is { turn_context.activity.locale }."
                # )

                # await turn_context.send_activity(self.PATTERN_MESSAGE)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        # Get the state properties from the turn context.
        welcome_user_state = await self.user_state_accessor.get(
            turn_context, WelcomeUserState
        )

        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True

            await turn_context.send_activity(
                "Good day"
            )

            name = turn_context.activity.from_property.name
            await turn_context.send_activity(
                f"How can I help you {name}\n"
            )

        else:
            # This example hardcodes specific utterances. You should use LUIS or QnA for more advance language
            # understanding.
            text = turn_context.activity.text.lower().strip(" \n\r")
            # print(text)
            if str(text) == "hello":
                await turn_context.send_activity(f"Hello Smartone")
            elif str(text) == "hi":
                await turn_context.send_activity(f"Hi Smartone")
            elif str(text) == "bye":
                await turn_context.send_activity(f"Bye Bye..Have a great day!")
            elif str(text) == "docs":
                await self.__send_docs_card(turn_context)
            elif str(text) == "intro":
                await self.__send_intro_card(turn_context)
            else:
                # await turn_context.send_activity(self.WELCOME_MESSAGE)
                await self.__on_message_activity1(turn_context)

    async def __on_message_activity1(self, turn_context: TurnContext):
        # The actual call to the QnA Maker service.
        response = await self.qna_maker.get_answers(turn_context)
        if response and len(response) > 0:
            await turn_context.send_activity(MessageFactory.text(response[0].answer))
        else:
            await turn_context.send_activity(self.WELCOME_MESSAGE)

    async def __send_docs_card(self, turn_context: TurnContext):
            card = HeroCard(
            title="ADC DOCS!!",
            text="Click to browse the docs",
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Bot factory share point",
                    text="Browse to explore the sharepoint",
                    display_text="Browse to explore the sharepoint",
                    value="https://capgemini.sharepoint.com/sites/BOTfactory/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FBOTfactory%2FShared%20Documents&newTargetListUrl=%2Fsites%2FBOTfactory%2FShared%20Documents&viewpath=%2Fsites%2FBOTfactory%2FShared%20Documents%2FForms%2FAllItems%2Easpx",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Effort Tracker",
                    text="Browse to fill youe daily efforts",
                    display_text="Browse to fill youe daily efforts",
                    value="https://apps.powerapps.com/play/2ad7c8fa-550e-44c5-af65-d6a29c0bb39e?tenantId=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Jira",
                    text="Browse to access Jira",
                    display_text="Browse to access Jira",
                    value="http://10.58.144.45/pm/login.jsp",
                ),
            ],
        )

            return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))

    async def __send_intro_card(self, turn_context: TurnContext):
            card = HeroCard(
                title="ADC INTRODUCTION",
                text="BOT IS THE NEW FUTURE",
                images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
                buttons=[
                    CardAction(
                        type=ActionTypes.open_url,
                        title="ADC",
                        text="Ask a question",
                        display_text="Ask a question",
                        value="http://cisadc.capgemini.com/",
                    ),
                    CardAction(
                        type=ActionTypes.open_url,
                        title="Bot Catalog",
                        text="Browse to view bot catalog",
                        display_text="Get an overview",
                        value="http://cisadc.capgemini.com/bots_catalog/",
                    )
                ],
            )


            return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))
