from tenacity import retry, stop_after_attempt, wait_random_exponential

class Stream2Msgs:
  def __init__(self, n=1, role="assistant"):
    self.msgs = [
      {
        "role": role,
        "content": "",
        "function_call": {
          "name": "",
          "arguments": "",
        },
      } for _ in range(n)
    ]
  
  def input(self, res):
    i = res.choices[0].index
    delta = res.choices[0].delta
    if content:=delta.content:
      self.msgs[i]["content"] += content
    if f_call := delta.function_call:
      if name:=f_call.name:
        self.msgs[i]["function_call"]["name"] += name
      if args:=f_call.arguments:
        self.msgs[i]["function_call"]["arguments"] += args
    return i

  def __call__(self, res):
    i = self.input(res)
    return i, self.msgs[i]

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_response(cl, messages, **kwargs):
  return cl.chat.completions.create(
    messages=messages,
    **kwargs
  )