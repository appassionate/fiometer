from pydantic import BaseModel, Field
from .utils import ini2dict, dict2ini



class FioInput(BaseModel):

    
    # avoid dict pointer problem BUG
    content: dict = Field(default_factory=dict)


    def from_input_file(self, filename):

        with open(filename, 'r',) as f:
            self.content = ini2dict(f.read())

    def render_dict(self):

        return dict2ini(self.content)
    