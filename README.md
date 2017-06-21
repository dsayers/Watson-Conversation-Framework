# Watson Conversation Demo Framework (an orchestration engine Watson Developer Cloud services and exeternal services)

## Create demos with automated conversation
This demo framework leverages the **Conversation**, **Retrieve and Rank**, ""Text to Speech**, **Speech to Text** and **Predictive Analytics** services. Powered by Watson, these services allow for a personalized experience in which users can engage in natural, human-like conversations with the chat engine.

## Running and Delpoying
In order to run this application, you will need to update watson.py with your watson service credentials and other id's. (These are the values in the brackets, eg. <'CONVERSATION_USERNAME'>) You will need to set at a minimum the values for the Conversation Service. If you want to do a voice demo, also populate the TTS and STT values.

To run locally, you'll need a python 2.7.12 runtime on your local machine. You'll also have to use PIP to install the libraries referenced in requirements.txt. To start the service, execute welcome.py. You can access the UI from a browser by opening http://localhost:5000

Once you can run this locally, you can of course push your application to Bluemix.

## My Deployed instance
You can use my instance of this framework here: http://service-orchestration-engine.mybluemix.net/
Ask questions like:
-- How many people work for your company?
-- Tell me about Node.js
-- I want to update my address
-- What's the earliest you can deliver a laptop to Athens GA?
-- I've decided to discontinue my service
