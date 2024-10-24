# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
# from tesing import insert_data   # for database
# from ema import send_email
from rasa_sdk.events import EventType
from rasa_sdk import Action, Tracker
# import string

# for first action  it is not used in project
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!, Develoer ")

        return []

# for second action it is not used in our project , using only learning purpose
class ActionImage(Action):

    def name(self) -> Text:
        return "action_image"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Here is something to cheer you up 😉", image="https://i.imgur.com/nGF1K8f.jpg")

        return []

# function for remove unwaterd character from name        
def clean_name(name):
    return "".join([c for c in name if c.isalpha()])
form_data = []  # store data in list

# this function contain user data 

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        form_data.append(name)   # store data first name
        
        if len(name) == 0:
            dispatcher.utter_message(text="Pleas Enter valid First Name.")
            return {"first_name": None}
        return {"first_name": name}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        name = clean_name(slot_value)
        form_data.append(name)  # store data in second name
        if len(name) == 0:
            dispatcher.utter_message(text="Pleas Enter valid Last Name.")
            return {"last_name": None}
        
        first_name = tracker.get_slot("first_name")
        if len(first_name) + len(name) < 3:
            dispatcher.utter_message(text="That's a very short name. We fear a typo. Restarting!")
            return {"first_name": None, "last_name": None}
        return {"last_name": name}
    

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone_number` value."""

        phone_number = slot_value.strip()
        form_data.append(phone_number)  #store phone number 
        if not phone_number.isdigit() and 7 <= len(phone_number) <= 15:
            dispatcher.utter_message(text="Please provide a valid phone number.")
            return {"phone_number": None}
        return {"phone_number": phone_number}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""

        email = slot_value.strip()
        form_data.append(email) # store email 
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            dispatcher.utter_message(text="Please provide a valid email address.")
            return {"email": None}
        return {"email": email}


    def validate_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `city` value."""

        # Check if the city name is provided.
        city = slot_value.strip()
        form_data.append(city) # store  city
        if not city:
            dispatcher.utter_message(text="Please enter a valid city name.")
            return {"city": None}
        return {"city": city}

    def validate_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `age` value."""

        # Check if the age is provided and within a valid range.
        # age = slot_value.strip()
        age = slot_value
        form_data.append(age) # store  age
        if age.isdigit():
            age = int(age)
        if 0 < age < 120:
            return {"age": age}
        else:
            dispatcher.utter_message(text="Please enter a valid age between 0 and 120.")
        return {"age": None}
    
 

class ActionProvideVeganDetails(Action):
    def name(self) -> Text:
        return "action_provide_vegan_details"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")

        # Mapping intents to categories and corresponding responses
        category_map = {
            "select_family": ("Family", "utter_family_selected"),
            "select_corporate": ("Corporate", "utter_corporate_selected"),
            "select_personal": ("Personal", "utter_personal_selected")
        }

        # Default category and response for unknown intents
        default_category = "Personal"
        default_response = "utter_personal_selected"

        # Get category and response based on intent
        category, response = category_map.get(intent, (default_category, default_response))

        # Log the selected category
        tracker.slots["selected_category"] = category

        # Dispatch the appropriate response
        dispatcher.utter_message(response=response)

        return []

class ActionProvideVeganSubCategories(Action):
    def name(self) -> Text:
        return "action_provide_vegan_sub_details"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")

        # Mapping intents to sub-categories and corresponding responses
        sub_category_map = {
            "two_member": ("2 Member", "product_list"),
            "four_member": ("4 Member", "product_list"),
            "six_member": ("6 Member", "product_list")
        }

        # Default sub-category and response for unknown intents
        default_sub_category = "6+ Member"
        default_response = "product_list"

        # Get sub-category and response based on intent
        sub_category, response = sub_category_map.get(intent, (default_sub_category, default_response))

        # Log the selected sub-category
        tracker.slots["selected_sub_category"] = sub_category

        # Dispatch the appropriate response
        dispatcher.utter_message(response=response)

        return []
    
class ActionProvideVeganSubCategories(Action):
    def name(self) -> Text:
        return "action_provide_vegan_subcorporate_details"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[EventType]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        print(intent)   # only for checking print value 
        if intent == "employee_one_to_ten":
            # form_data.append("Employees Size 1-10")
            dispatcher.utter_message(response="product_list")

        elif intent == "employee_one_to_twentyfive":
            # form_data.append("Employees Size 1-25")
            dispatcher.utter_message(response="product_list")
        elif intent == "employee_one_to_fifty":
            # form_data.append("Employees Size 1-50")
            dispatcher.utter_message(response="product_list")
        else:
            form_data.append("Employees Size 50-above")
        # insert_data(form_data[0],form_data[1],form_data[2],form_data[3],form_data[4],form_data[5],form_data[6],form_data[7])
        return []





# for handling out scope question 
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        # Respond with a message asking to rephrase the question
        dispatcher.utter_message(text="I'm sorry, I didn't understand that. Could you please rephrase your question? "
                                      "Feel free to ask about vegan-related topics!")
        return []
    
#  for video
class ActionYoutubeVideos(Action):

    def name(self) -> Text:
        return "action_show_video"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text="Hello World!")
        dispatcher.utter_message(attachment={
            "type": "video",
            "payload": {
                "title": "Watch Below Video For More Information",
                "src": "how_to_use_chatbot.mp4"
            }
        })

        return []   


class ActionIntoShowCarousel(Action):

     def name(self) -> Text:
         return "actions_list"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         new_carousel = {
             "type": "template",
             "payload":{
                 "template_type":"generic",
                 "elements":[
                     {
                         "title": "Weight Loss",
                         "subtitle": "Shed Pounds, Gain Confidence",
                        #  "image_url": "https://qph.cf2.quoracdn.net/main-qimg-f7b477c863d72cfc16624b231ed16763-lq",
                         "image_url": "Chatbot image\Weight losss.jpg",
                         "buttons":[
                             {
                               "title": "Buy Plans",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                             {
                               "title": "Details",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"   
                             },
                            {
                               "title": "Contact",
                               "type": "postback",
                               "payload": "/contact_details"   
                             }
                         ]
                     },
                     {
                         "title": "Weight Gain",
                         "subtitle": "Build Mass, Transform Body",
                        # "image_url": "https://risingmatters.com/wp-content/uploads/2020/08/How-Gain-Weight-Fast-Safe.jpg",
                         "image_url": "Chatbot image\weight gain.jpg",
                         "buttons":[
                             {
                               "title": "Buy Plans",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                             {
                               "title": "Details",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                            {
                               "title": "Contact",
                               "type": "postback",
                               "payload": "/contact_details"   
                             }
                         ]
                     },
                    {
                         "title": "Immunity Boost",
                         "subtitle": "Feel Energized, Conquer Day",
                        #  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTr6Nwf-U9Xok-kEhHGLIPSHkh1UE4NQ0NqlQ&s",
                        "image_url": "Chatbot image\energy boosting.jpg",
                         "buttons":[
                             {
                               "title": "Buy Plans",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                             {
                               "title": "Details",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"   
                             },
                            {
                               "title": "Contact",
                               "type": "postback",
                               "payload": "/contact_details"   
                             }
                         ]
                     },
                    {
                         "title": "Disease Prevention",
                         "subtitle": "Stay Healthy, Live Longer",
                         "image_url": "https://cdn.dribbble.com/users/1006465/screenshots/15003513/frame_1__1_.png",
                         "buttons":[
                             {
                               "title": "Buy Plans",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                             {
                               "title": "Details",
                               "url": "https://vegan-dietitian.com/",
                               "type": "web_url"  
                             },
                            {
                               "title": "Contact",
                               "type": "postback",
                               "payload": "/contact_details"   
                             }
                         ]
                     }
                 ]
             } 
         }
         dispatcher.utter_message(text="Select Plans",attachment=new_carousel)
        #  insert_data(form_data[0],form_data[1],form_data[2],form_data[3],form_data[4],form_data[5],form_data[6],form_data[7])
         return[]
    
