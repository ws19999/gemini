import google.ai.generativelanguage as glm
from datetime import datetime
import pytz

def now(tz:str="Asia/Seoul"):
  """Get the current date and time.
  """
  return {
    "timezone": tz,
    "time": datetime.now(pytz.timezone(tz)).strftime("%Y-%m-%d %H:%M:%S"),
  }

_now_tool = glm.Tool(
  function_declarations=[
    glm.FunctionDeclaration(
      name='now',
      description="Returns the current date and time.",
      parameters=glm.Schema(
        type=glm.Type.OBJECT,
        properties={
          'tz': glm.Schema(type=glm.Type.STRING, description="Timezone, e.g. Asia/Seoul"),
        },
        required=[]
      )
    )
  ]
)