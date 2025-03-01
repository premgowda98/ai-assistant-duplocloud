import constants.llms as llm_const

GOOGLE_2_FLASH = "models/gemini-2.0-flash"
GOOGLE_2_FLASH_LITE = "models/gemini-2.0-flash-lite"
GOOGLE_15_FLASH = "models/gemini-1.5-flash"
GOOGLE_15_PRO = "models/gemini-1.5-pro"

OPENAI_GPT_40 = "gpt-4o"
OPENAI_GPT_40_MINI = "gpt-4o-mini"
OPENAI_GPT_01_MINI = "o1-mini"
OPENAI_GPT_03_MINI = "o3-mini"

GOOGLE_MODELS = [GOOGLE_2_FLASH, GOOGLE_2_FLASH_LITE, GOOGLE_15_FLASH, GOOGLE_15_PRO]
OPENAI_MODELS = [
    OPENAI_GPT_40,
    OPENAI_GPT_40_MINI,
    OPENAI_GPT_01_MINI,
    OPENAI_GPT_03_MINI,
]

LLM_MODELS = {llm_const.GOOGLE: GOOGLE_MODELS, llm_const.OPENAI: OPENAI_MODELS}
