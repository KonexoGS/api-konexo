from app.enums import ProjectsCategoryCode
from random import randint, choice
from traceback import format_exc

class GenerateFriendlyCode:

    def __init__(self):
        self.project_alias = 'PRJ'
        self.stack_alias = 'STK'
        self.badges_alias = 'BDG'
        self.alphabetic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def generate_project_code(self, category: ProjectsCategoryCode):
        try:
            category_name = category[0].value.upper() # get the first instance, because its the main category of the project
            category_id = ProjectsCategoryCode[category_name].value
            unique_code = '' 
            for i in range(4):
                if i % 2 == 0:
                    unique_code += str(randint(0, 9))
                else:
                    unique_code += choice(self.alphabetic)
            
            friendly_code = f'{self.project_alias}-{category_id}-{unique_code}'
            return friendly_code
        except KeyError as e:
            print(format_exc)
            raise KeyError("Categoria inexistente no sistema.")
