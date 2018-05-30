def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    intent = ''
    response = ''

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

    intent = '{}'.format(response.query_result.intent.display_name)
    response = '{}'.format(response.query_result.fulfillment_text)

    return intent, response