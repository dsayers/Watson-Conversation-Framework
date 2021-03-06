# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, sys
from os.path import join, dirname
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import TextToSpeechV1 as TextToSpeech
import xmltodict
# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
#####
# Hardcoded env variables defaults for testing
#####
PREDICTIVE_ANALYTICS_ACCESS_KEY = '<PREDICTIVE_ANALYTICS_ACCESS_KEY>'
PREDICTIVE_ANALYTICS_CONTEXT_ID = '<PREDICTIVE_ANALYTICS_CONTEXT_ID>'
ALCHEMY_API_APIKEY = '<ALCHEMY_API_APIKEY>'
TONE_ANALYZER_VERSION = '2016-05-19'
TONE_ANALYZER_USERNAME = '<TONE_ANALYZER_USERNAME>'
TONE_ANALYZER_PASSWORD = '<TONE_ANALYZER_PASSWORD>'
CONVERSATION_WORKSPACE_ID = '<CONVERSATION_WORKSPACE_ID>'
CONVERSATION_VERSION = '2016-07-11'
CONVERSATION_USERNAME = '<CONVERSATION_USERNAME>'
CONVERSATION_PASSWORD = '<CONVERSATION_PASSWORD>'
DIALOG_ID = '<DIALOG_ID>'
DIALOG_USERNAME = '<DIALOG_USER_NAME>'
DIALOG_PASSWORD = '<DIALOG_PASSWORD>'
CLASSIFIER_ID = '<CLASSIFIER_ID>'
CLASSIFIER_USERNAME = '<CLASSIFIER_USERNAME>'
CLASSIFIER_PASSWORD = '<CLASSIFIER_PASSWORD>'
TTS_USERNAME = '<TTS_USERNAME>'
TTS_PASSWORD = '<TTS_PASSWORD>'
STT_USERNAME = '<SST_USERNAME>'
STT_PASSWORD = '<STT_PASSWORD>'
SOLR_CLUSTER_ID = '<SOLR_CLUSTER_ID>'
SOLR_COLLECTION_NAME = '<SOLR_COLLECTION_NAME>'
RANKER_ID = '<RANKER_ID>'
RETRIEVE_AND_RANK_USERNAME = '<RETRIEVE_AND_RANK_USERNAME>'
RETRIEVE_AND_RANK_PASSWORD = '<RETRIEVE_AND_RANK_PASSWORD>'
RANDR_SEARCH_ARGS = '<RANDR_SEARCH_ARGS>'
WEX_URL = '<WEX_URL>'
CASTIRON_USERNAME = ''
CASTIRON_PASSWORD = ''
CIRON_URL_GET_ASSET_ACTIVATION_CODE = '<CIRON_URL_GET_ASSET_ACTIVATION_CODE>'
CIRON_URL_CREATE_CASE = '<CIRON_URL_CREATE_CASE>'
CIRON_URL_ACTIVATION = '<CIRON_URL_ACTIVATION>'
CIRON_URL_GET_SERIAL = '<CIRON_URL_GET_SERIAL>'

#####
# Overwrites by env variables
#####
if 'CASTIRON_USERNAME' in os.environ:
	CASTIRON_USERNAME = os.environ['CASTIRON_USERNAME']
if 'CASTIRON_PASSWORD' in os.environ:
	CASTIRON_PASSWORD = os.environ['CASTIRON_PASSWORD']
if 'PREDICTIVE_ANALYTICS_CONTEXT_ID' in os.environ:
	PREDICTIVE_ANALYTICS_CONTEXT_ID = os.environ['PREDICTIVE_ANALYTICS_CONTEXT_ID']
if 'TONE_ANALYZER_VERSION' in os.environ:
	TONE_ANALYZER_VERSION = os.environ['TONE_ANALYZER_VERSION']
if 'CONVERSATION_WORKSPACE_ID' in os.environ:
	CONVERSATION_WORKSPACE_ID = os.environ['CONVERSATION_WORKSPACE_ID']
if 'CONVERSATION_VERSION' in os.environ:
	CONVERSATION_VERSION = os.environ['CONVERSATION_VERSION']
if 'DIALOG_ID' in os.environ:
	DIALOG_ID = os.environ['DIALOG_ID']
if 'CLASSIFIER_ID' in os.environ:
	CLASSIFIER_ID = os.environ['CLASSIFIER_ID']
if 'SOLR_CLUSTER_ID' in os.environ:
	SOLR_CLUSTER_ID = os.environ['SOLR_CLUSTER_ID']
if 'SOLR_COLLECTION_NAME' in os.environ:
	SOLR_COLLECTION_NAME = os.environ['SOLR_COLLECTION_NAME']
if 'RANKER_ID' in os.environ:
	RANKER_ID = os.environ['RANKER_ID']
if 'RANDR_SEARCH_ARGS' in os.environ:
	RANDR_SEARCH_ARGS = os.environ['RANDR_SEARCH_ARGS']
if 'WEX_URL' in os.environ:
	WEX_URL = os.environ['WEX_URL']
if 'VCAP_SERVICES' in os.environ:
	if len('VCAP_SERVICES') > 0:
		vcap_services = json.loads(os.environ['VCAP_SERVICES'])
		if 'pm-20' in vcap_services.keys():
			pm_20 = vcap_services['pm-20'][0]
			PREDICTIVE_ANALYTICS_ACCESS_KEY = pm_20["credentials"]["access_key"]
		if 'alchemy_api' in vcap_services.keys():
			alchemy_api = vcap_services['alchemy_api'][0]
			ALCHEMY_API_APIKEY = alchemy_api["credentials"]["apikey"]
		if 'conversation' in vcap_services.keys():
			conversation = vcap_services['conversation'][0]
			CONVERSATION_USERNAME = conversation["credentials"]["username"]
			CONVERSATION_PASSWORD = conversation["credentials"]["password"]
		if 'tone_analyzer' in vcap_services.keys():
			tone_analyzer = vcap_services['tone_analyzer'][0]
			TONE_ANALYZER_USERNAME = tone_analyzer["credentials"]["username"]
			TONE_ANALYZER_PASSWORD = tone_analyzer["credentials"]["password"]
		if 'dialog' in vcap_services.keys():
			dialog = vcap_services['dialog'][0]
			DIALOG_USERNAME = dialog["credentials"]["username"]
			DIALOG_PASSWORD = dialog["credentials"]["password"]
		if 'natural_language_classifier' in vcap_services.keys():
			natural_language_classifier = vcap_services['natural_language_classifier'][0]
			CLASSIFIER_USERNAME = natural_language_classifier["credentials"]["username"]
			CLASSIFIER_PASSWORD = natural_language_classifier["credentials"]["password"]
		if 'speech_to_text' in vcap_services.keys():
			stt = vcap_services['speech_to_text'][0]
			STT_USERNAME = stt["credentials"]["username"]
			STT_PASSWORD = stt["credentials"]["password"]
		if 'text_to_speech' in vcap_services.keys():
			tts = vcap_services['text_to_speech'][0]
			TTS_USERNAME = tts["credentials"]["username"]
			TTS_PASSWORD = tts["credentials"]["password"]
		if 'retrieve_and_rank' in vcap_services.keys():
			retrieve_and_rank = vcap_services['retrieve_and_rank'][0]
			RETRIEVE_AND_RANK_USERNAME = retrieve_and_rank["credentials"]["username"]
			RETRIEVE_AND_RANK_PASSWORD = retrieve_and_rank["credentials"]["password"]
# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------
#####
# local
#####
# Encapsulate BMIX services plus helper funcs ----
def CIRON_get_asset_activation_code(data):
	global CIRON_URL_GET_ASSET_ACTIVATION_CODE, CASTIRON_USERNAME, CASTIRON_PASSWORD
	POST_SUCCESS = 200
	castiron_response = {}
	url = CIRON_URL_GET_ASSET_ACTIVATION_CODE
	r = requests.post(url, auth=(CASTIRON_USERNAME, CASTIRON_PASSWORD), data=data)
	print('---CIRON_get_asset_activation_code')
	print('---r.status_code')
	print(r.status_code)
	if r.status_code == POST_SUCCESS:
		castiron_response = r.json()
		print('--Status_Message Get Asset')
		print(castiron_response['Status_Message'])
	else:
		castiron_response['Status_Message'] = 'Cast Iron service call failed with return code: [' + str(r.status_code) + ']'
	return castiron_response

def BMIX_evaluate_predictive_model(model):
	global PREDICTIVE_ANALYTICS_ACCESS_KEY, PREDICTIVE_ANALYTICS_CONTEXT_ID
	POST_SUCCESS = 200
	response = {}
	response['flag'] = False
	response['message'] = 'r.status_code != POST_SUCCESS'
	url = 'https://palbyp.pmservice.ibmcloud.com/pm/v1/' + PREDICTIVE_ANALYTICS_CONTEXT_ID + '?accesskey=' + PREDICTIVE_ANALYTICS_ACCESS_KEY
	r = requests.post(url, headers={'content-type': 'application/json', 'accept': 'application/json'}, data=json.dumps(model))
	if r.status_code == POST_SUCCESS:
		response = r.json()
	return response
	
def BMIX_call_alchemy_api(request, parameters):
	global ALCHEMY_API_APIKEY
	POST_SUCCESS = 200
	response = {}
	parameters['apikey'] = ALCHEMY_API_APIKEY
	parameters['outputMode'] = 'json'
	url = 'https://gateway-a.watsonplatform.net/calls' + request
	r = requests.post(url, data=parameters)
	if r.status_code == POST_SUCCESS:
		response = r.json()
	return response
	
def BMIX_analyze_tone(text):
	global TONE_ANALYZER_VERSION, TONE_ANALYZER_USERNAME, TONE_ANALYZER_PASSWORD
	POST_SUCCESS = 200
	response = {}
	url = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=' + TONE_ANALYZER_VERSION
	r = requests.post(url, auth=(TONE_ANALYZER_USERNAME, TONE_ANALYZER_PASSWORD), headers={'content-type': 'text/plain', 'accept': 'application/json'}, data=text)
	if r.status_code == POST_SUCCESS:
		response = r.json()
	return response
	
def BMIX_converse(message):
	global CONVERSATION_WORKSPACE_ID, CONVERSATION_USERNAME, CONVERSATION_PASSWORD, CONVERSATION_VERSION
	POST_SUCCESS = 200
	url = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces/' + CONVERSATION_WORKSPACE_ID + '/message?version=' + CONVERSATION_VERSION
	r = requests.post(url, auth=(CONVERSATION_USERNAME, CONVERSATION_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps(message))
	if r.status_code == POST_SUCCESS:
		message = r.json()
	return message
	
def BMIX_get_first_dialog_response_json():
	global DIALOG_ID, DIALOG_USERNAME, DIALOG_PASSWORD
	POST_SUCCESS = 201
	response_json = None
	url = 'https://gateway.watsonplatform.net/dialog/api/v1/dialogs/' + DIALOG_ID + '/conversation'
	r = requests.post(url, auth=(DIALOG_USERNAME, DIALOG_PASSWORD))
	if r.status_code == POST_SUCCESS:
		response_json = r.json()
		response_json['response'] = format_dialog_response(response_json['response'])
	return response_json

def BMIX_get_next_dialog_response(client_id, conversation_id, input):
	global DIALOG_ID, DIALOG_USERNAME, DIALOG_PASSWORD
	POST_SUCCESS = 201
	response = ''
	url = 'https://gateway.watsonplatform.net/dialog/api/v1/dialogs/' + DIALOG_ID + '/conversation'
	payload = {'client_id': client_id, 'conversation_id': conversation_id, 'input': input}
	r = requests.post(url, auth=(DIALOG_USERNAME, DIALOG_PASSWORD), params=payload)
	if r.status_code == POST_SUCCESS:
		response = format_dialog_response(r.json()['response'])
	return response
	
def BMIX_classify(utterance, threshold):
	global CLASSIFIER_ID, CLASSIFIER_USERNAME, CLASSIFIER_PASSWORD
	POST_SUCCESS = 200
	
	class_name = ''
	url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/' + CLASSIFIER_ID + '/classify'
	r = requests.post(url, auth=(CLASSIFIER_USERNAME, CLASSIFIER_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps({'text': utterance}))

	if r.status_code == POST_SUCCESS:
		classes = r.json()['classes']
		if len(classes) > 0:
			confidence = classes[0]['confidence']
			if (confidence > threshold):
				class_name = classes[0]['class_name']
	return class_name

def BMIX_retrieve_and_rank(question):
	global SOLR_CLUSTER_ID, SOLR_COLLECTION_NAME, RANKER_ID, RANDR_SEARCH_ARGS, RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD
	POST_SUCCESS = 200
	docs = []
	fields_str = RANDR_SEARCH_ARGS
	question = str(question).decode('utf-8', 'ignore')
	url = 'https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/' + SOLR_CLUSTER_ID + '/solr/' + SOLR_COLLECTION_NAME + '/fcselect?ranker_id=' + RANKER_ID + '&q=' + question + '&wt=json&fl=' + fields_str
	r = requests.get(url, auth=(RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD), headers={'content-type': 'application/json; charset=utf8'})
	if r.status_code == POST_SUCCESS:
		docs = r.json()['response']['docs']
	return docs

def WEX_retrieve(question):
	global WEX_URL;
	POST_SUCCESS = 200
	docs = []
	query_str = format_WEX_query_str(question)
	url = WEX_URL.replace('[##QUERY_STR##]', query_str)
	r = requests.get(url)
	if r.status_code == POST_SUCCESS:
		WEX_response = xmltodict.parse(r.content)
		if len(WEX_response['query-results']) > 3:
			docs = WEX_response['query-results']['list']['document']
			if type(docs) == type(WEX_response):
				doc = docs
				docs = []
				docs.append(doc)
	return docs

def get_stt_token():
	global STT_USERNAME, STT_PASSWORD
	return Authorization(username=STT_USERNAME, password=STT_PASSWORD).get_token(url=SpeechToText.default_url)

def get_tts_token():
	global TTS_USERNAME, TTS_PASSWORD
	return Authorization(username=TTS_USERNAME, password=TTS_PASSWORD).get_token(url=TextToSpeech.default_url)

# Helper funcs -----------------------------------
def format_dialog_response(dialog_responses):
	dialiog_response = ''
	if dialog_responses:
		for dialiog_response_line in dialog_responses:
			if str(dialiog_response_line) != '':
				if len(dialiog_response) > 0:
					dialiog_response = dialiog_response + ' ' + dialiog_response_line
				else:
					dialiog_response = dialiog_response_line
	return dialiog_response

def format_WEX_query_str(question):
	query_str = ''
	strip_tokens = '_HOW_A_IS_WHAT_THE_WHICH_WHO_IN_THAT_THAN_THEN_OF_WITH_WITHIN_FOR_MUST_'
	question = question.replace('?','')
	question = question.replace('%','')
	tokens = question.split()
	for token in tokens:
		if strip_tokens.find('_' + token.upper() + '_') == -1:
			query_str = query_str + token + ' '
	return query_str.strip().replace(' ', '%20')
