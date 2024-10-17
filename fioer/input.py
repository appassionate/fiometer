from .utils import ini2dict, dict2ini, generate_fio_input_file

class Input():
    
    content:dict = {}

    def from_input_file(self, filename):
        
        with open(filename, 'r') as f:
            self.content = ini2dict(f.read())
                    
    
    def render_dict(self):
        
        return dict2ini(self.content)