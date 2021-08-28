from plugin import plugin

HELP_TEXTS = {
    'newsapi_org': 'https://newsapi.org/',
    'google': 'https://console.developers.google.com/apis',
    'openwathermap': 'https://openweathermap.org/appid'
}


HELP_TEXTS_LONG = {
    'google': """\
Please create an API key here: https://console.developers.google.com/apis/credentials
then copy the value to 'key' in jarviscli/data/Google_api_key.json
To create an api key you must select a project (creating one if you do not have one yet)
, then you must select 'create credentials' > 'API key'.

More detailed instructions can be found here: "
https://developers.google.com/civic-information/docs/using_api
"""
}


@ plugin("apikey add")
def apikey_add(jarvis, s):
    valid_api_keys = jarvis.key_vault.get_valid_api_key_names()
    options = []
    for api_key in valid_api_keys:
        if jarvis.get_user_pass(api_key)[1] is None:
            options.append(api_key)
            if api_key in HELP_TEXTS:
                jarvis.say('{}) {} ({})'.format(len(options), api_key, HELP_TEXTS[api_key]))
            else:
                jarvis.say('{}) {}'.format(len(options), api_key))
    if len(options) == 0:
        jarvis.say("There is no API key in the world, I would like to know")
        return
    choosen_option = jarvis.input_number("Which api key to add?", rtype=int,
                                         rmin=1, rmax=len(options)) - 1
    key = jarvis.input("New API key:")
    jarvis.update_user_pass(options[choosen_option], '##APIKEY', key)
    jarvis.say("Thanks!")


@ plugin("apikey update")
def apikey_update(jarvis, s):
    valid_api_keys = jarvis.key_vault.get_valid_api_key_names()
    for i, api_key in enumerate(valid_api_keys):
        if api_key in HELP_TEXTS:
            jarvis.say('{}) {} ({})'.format(i + 1, api_key, HELP_TEXTS[api_key]))
        else:
            jarvis.say('{}) {}'.format(i + 1, api_key))
    if len(valid_api_keys) == 0:
        jarvis.say("No API KEY")
        return
    choosen_option = jarvis.input_number("Which api key to update? ", rtype=int,
                                         rmin=1, rmax=len(valid_api_keys)) - 1
    key = jarvis.input("New API key: ")
    jarvis.update_user_pass(valid_api_keys[choosen_option], '##APIKEY', key)
    jarvis.say("Thanks!")
