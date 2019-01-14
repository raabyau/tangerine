#from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from chatbot.chat import QuestionSet
from chatbot.models import Question, Questionnaire
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept a new websocket connection
        await self.accept()

        # Load the demo questions and questionnaire
        p = Question.objects.get(name="demo_questions").data
        q = Questionnaire.objects.get(name="demo_questionnaire").data

        # Create a new QuestionSet instance, get the first question and send it to the client
        self.questions = QuestionSet(p, q)
        question = self.questions.next()

        await self.send(text_data=json.dumps({
            'action': "chat",
            'message': question
        }))

    async def disconnect(self, close_code):
        pass     

    async def receive(self, text_data):
        # Parse the JSON received from the client
        text_data_json = json.loads(text_data)
        action = text_data_json['action'].strip()

        if action == "chat":
            response = text_data_json['message'].strip()

            # Check that the rclient esponse is valid.
            r = self.questions.check(response)
      
            if r["result"]:
                # If the response was valid get the next question and send it.
                if self.questions.remaining:
                    question = self.questions.next()

                    await self.send(text_data=json.dumps({
                        'action': "chat",
                        'message': question
                    }))
                else:
                    await self.send(text_data=json.dumps({
                        'action': "complete",
                        'message': "Thank you!"
                    }))  
            else:
                # If the response was invalid, send an error message.
                await self.send(text_data=json.dumps({
                    'action': "chat",
                    'message': r["message"]
                }))

        elif action == "results":
            await self.send(text_data=json.dumps({
                'action': "results",
                'results': self.questions.responses
            }))  
