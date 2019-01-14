import re

class QuestionSet:
  def __init__(self, prompts, questions):
    self.__prompts = prompts
    self.__questions = questions
    self.reset()

  def reset(self):
    self.remaining = True
    self.responses = {}
    self.__current_pos = self.__questions["first"]

  def next(self):
    return self.__prompts[self.__current_pos]["text"]

  def __validateStr(self, resp):
    prompt = self.__prompts[self.__current_pos]

    if "conditions" in prompt["response"]:
      conditions = prompt["response"]["conditions"]

      if "min" in conditions:
        minimum = conditions["min"]
        if len(resp) < minimum["val"]:
          return {"result": False, "message": minimum["errmsg"].format(minimum["val"]) }

      if "max" in conditions:
        maximum = conditions["max"]
        if len(resp) > maximum["val"]:
          return {"result": False, "message": maximum["errmsg"].format(maximum["val"]) }

      return {"result": True, "value": resp}

  def __validateDate(self, resp):
    prompt = self.__prompts[self.__current_pos]

    if not re.match(r'^\d{2}-\d{2}-\d{4}$', resp):
      return {"result": False, "message": prompt["response"]["errmsg"]}
    return {"result": True, "value": resp}

  def __validateInt(self, resp):
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
