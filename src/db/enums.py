from enum import Enum


class SessionMode(Enum):
    """
    Enumeration of supported conversation modes for the assistant.

    Attributes:
        GPT (str): Chat mode for general-purpose GPT assistant.
        TALK (str): Reserved for future conversational mode.
        QUIZ (str): Reserved for future quiz-based interaction.
        RANDOM (str): Sends random technical trivia facts.
    """
    GPT = "gpt"
    TALK = "talk"
    QUIZ = "quiz"
    RANDOM = "random"