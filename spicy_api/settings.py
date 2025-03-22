# Retry settings
RETRY_TIMEOUT = 5
RETRY_MAX_COUNT = 5

# URLS
SPICY_USER_AUTH_URL = 'https://gamma.kinde.com/oauth2/token'
SPICY_USER_DETAILS_URL = 'https://4mpanjbsf6.execute-api.us-east-1.amazonaws.com/v2/users'
SPICY_SEARCH_KEY_URL = 'https://4mpanjbsf6.execute-api.us-east-1.amazonaws.com/v2/applications/spicychat'

SPICY_GET_CONVERSATIONS_URL = 'https://4mpanjbsf6.execute-api.us-east-1.amazonaws.com/v2/characters/{char_id}/conversations'
SPICY_DELETE_CONVERSATION_URL = 'https://4mpanjbsf6.execute-api.us-east-1.amazonaws.com/conversations/{conv_id}'
SPICY_SEND_MESSAGE_URL = 'https://chat.nd-api.com/chat'

SPICY_GET_BOT_PROFILE_URL = 'https://4mpanjbsf6.execute-api.us-east-1.amazonaws.com/v2/characters/{char_id}'
SPICY_SEARCH_BOTS_URL = 'https://etmzpxgvnid370fyp.a1.typesense.net/multi_search'
SPICY_AVATAR_URL = 'https://ndsc.b-cdn.net/{avatar_slug}'

def genereate_search_data(bot_name: str = None, page: int = 1, count: int = 1):

    if not bot_name: bot_name = '*'

    return {
    "searches": [
        {
            "query_by":"name,title,tags,creator_username,character_id",
            "exclude_fields":"application_ids,greeting,moderation_flags,moderation_keywords,moderation_status,reportsType",
            "use_cache":True,
            "sort_by":"num_messages_24h:desc",
            "highlight_full_fields":"name,title,tags,creator_username,character_id",
            "collection":"characters",
            "q": bot_name,
            "facet_by":"tags",
            "filter_by":"application_ids:spicychat && tags:!Step-Family && is_nsfw:false",
            "max_facet_values":100,
            "page": page,
            "per_page": count
        }
    ]
}