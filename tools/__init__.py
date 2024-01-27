import google.ai.generativelanguage as glm
from .now import now, _now_tool

tools = {
  'now': _now_tool
}

functions = {
  'now': now,
}

def handle_function_call(parts):
  try:
    fc = parts[0].function_call
    assert fc.name in functions.keys()
    return glm.Content(
      parts=[glm.Part(
        function_response=glm.FunctionResponse(
          name=fc.name,
          response=functions[fc.name](**fc.args)
        )
      )]
    )
  except:
    pass
  return None