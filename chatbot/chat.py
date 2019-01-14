"""
QuestionSet
"""

import re

class QuestionSet:
  """QuestionSet. Class for iterating through a set of questions.
  """

  def __init__(self, prompts, questions):
    """The QuestionSet constructor

    Creates a new QuestionSet object with prompts and questions.

    Parameters
    ----------
    prompts : dict
    The prompts that contains the sentences that make up questions and the rules that govern the validity of the responses.

    questions: dict
    The structure that defines the order in which the questions are asked. Each question or the response to it, points to the next question in the QuestionSet.
    
    Examples
    --------
    # 2 prompts, one that asks for a name and the other for a date of birth.
    p = {
      "name": {
        "text": "What is your name?",
        "response": {
          "type": "str",
          "conditions": {
              "min": {
                "val":10,
                "errmsg": "Enter a name that is greater than {} characters",
              }
          }
        }
      },
      "dob": {
        "text": "When were you born?",
        "response": {
          "type": "date",
          "errmsg": "Please enter the date in the format dd-mm-yyyy"
        }
      },
    }

    # Questions. "first" key marks "name" as the first prompt. "last" value marks "dob" as the last prompt.
    q = {
      "first": "name",
      "name":  "dob",
      "dob":   "last"
    }

    qs = QuestionSet(p, q)
    question = qs.next()
    res = qs.check("Fred")

    str = "response accepted" if res["result"] else "response invalid"
    print(str)

    question = qs.next()
    res = qs.check("01-01-2010")

    str = "response accepted" if res["result"] else "response invalid"
    print(str)

    print(qs.responses)

    """
    self.__prompts = prompts
    self.__questions = questions
    self.reset()

  def reset(self):
    """Reset the QuestionSet.

    Resets the internal state of the QuestionSet object, by clearing responses and moving back to the first question in the set.
    """
    self.remaining = True
    self.responses = {}
    self.__current_pos = self.__questions["first"]

  def next(self):
    """Get the next question in the Question set.

    Returns
    -------
    question : string
    """
    return self.__prompts[self.__current_pos]["text"]

  def __validateStr(self, resp):
    """Validate a string response to a question

    Checks that the response adheres to the validation rules associated with the question.
    Strings responses can be constrained to a minimum (min) or maximum (max) length.

    Parameters
    ----------
    resp : string.
    The response string to validate

    Returns
    -------
    result : dict
    The "result" key stores a boolean value that indicate if the response is valid or not.
    The "message" key stores validation error messages in the case that the "result" is False.
    The "value" key stores the validated string in the case that the "result" is True.
  """
    prompt = self.__prompts[self.__current_pos]

    if "conditions" in prompt["response"]:
      conditions = prompt["response"]["conditions"]

      # Check minimum condition.
      if "min" in conditions:
        minimum = conditions["min"]
        if len(resp) < minimum["val"]:
          return {"result": False, "message": minimum["errmsg"].format(minimum["val"]) }

      # Check maximum condition.
      if "max" in conditions:
        maximum = conditions["max"]
        if len(resp) > maximum["val"]:
          return {"result": False, "message": maximum["errmsg"].format(maximum["val"]) }

      # Valid string
      return {"result": True, "value": resp}

  def __validateDate(self, resp):
    """Validate a date response to a question.

    Checks that the response adheres to the validation rules associated with the question.
    Date responses must take the form "dd-mm-yyyy".

    Parameters
    ----------
    resp : string.
    The date to validate

    Returns
    -------
    result : dict
    The "result" key stores a boolean value that indicate if the response is valid or not.
    The "message" key stores validation error messages in the case that the "result" is False.
    The "value" key stores the validated string in the case that the "result" is True.
  """
    prompt = self.__prompts[self.__current_pos]

    if not re.match(r'^\d{2}-\d{2}-\d{4}$', resp):
      return {"result": False, "message": prompt["response"]["errmsg"]}
    return {"result": True, "value": resp}

  def __validateInt(self, resp):
    """Validate an integer response to a question.

    Integer responses can be constrained to a minimum (min) value.

    Parameters
    ----------
    resp : string.
    The integer to validate (in the form of a string)

    Returns
    -------
    result : dict
    The "result" key stores a boolean value that indicate if the response is valid or not.
    The "message" key stores validation error messages in the case that the "result" is False.
    The "value" key stores the validated string in the case that the "result" is True.
  """
    prompt = self.__prompts[self.__current_pos]

    if not re.match(r'^\d{1,}$', resp):
      return { "result": False, "message": prompt["response"]["errmsg"] }

    value = int(resp)

    if "conditions" in prompt["response"]:
      conditions = prompt["response"]["conditions"]

      if "min" in conditions:
        minimum = conditions["min"]
        if value < minimum["val"]:
          return {"result": False, "message": minimum["errmsg"].format(minimum["val"]) }

    return { "result": True, "value": value }

  def __validateSet(self, resp):
    """Validate a response that takes the form of a set selection.

    Checks that the response is contained within a known set of response options.

    Parameters
    ----------
    resp : string.
    The integer to validate (in the form of a string)

    Returns
    -------
    result : dict
    The "result" key stores a boolean value that indicate if the response is valid or not.
    The "message" key stores validation error messages in the case that the "result" is False.
    The "value" key stores the validated string in the case that the "result" is True.
  """
    prompt = self.__prompts[self.__current_pos]
    valid_set = frozenset(prompt["response"]["options"])
    response = resp.lower()

    if response not in valid_set:
      return {"result": False, "message": prompt["response"]["errmsg"]}
    return {"result": True, "value": response}

  __validators = {
      "str":  __validateStr,
      "int":  __validateInt,
      "date": __validateDate,
      "set":  __validateSet,
  }

  def check(self, response):
    """Check the response to the current questions.

    Checks the validity of the response by applying the appropriate validation rule. If the response is
    found to be valid, then it is accepted as an answer and the next question is set. Otherwise, an error
    message is provided and the current question remains set.

    Parameters
    ----------
    response : string.
    The response to check/validate.

    Returns
    -------
    result : dict
    The "result" key stores a boolean value that indicate if the response is valid or not.
    The "message" key stores validation error messages in the case that the "result" is False.
    The "value" key stores the validated string in the case that the "result" is True.

    """
    prompt = self.__prompts[self.__current_pos]

    # Some prompts do require a response so validation is not necessary in these cases.
    if "response" not in prompt:
      return {"result": True}

    # Run a validator that matches the response type.
    response_type = prompt["response"]["type"]
    res = self.__validators[response_type](self, response)

    # Save the response and move to the next question if validation was successful
    if res["result"]:
      self.responses[self.__current_pos] = res["value"]

      if self.__current_pos in self.__questions:
        new_pos = self.__questions[self.__current_pos]
        self.__current_pos = new_pos if type(new_pos) is str else new_pos[response.lower()]
      if self.__current_pos == "last":
        self.remaining = False

    return res
