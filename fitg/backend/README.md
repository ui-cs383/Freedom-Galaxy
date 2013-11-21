# Backend Team Todo

- We need to have a single command for a given action:
   - move_environ() needs a move()
   - mil_combat and char_combat need a combat()
   - We can either merge the functions (if possible) or we can have a single command that determines if 
     military combat is taking place or character combat. Same with move.
- merge_stack() parameters need to be swapped. Probably going to change this in the API so Jeff/Ben you don't need to change yours.
- Detection is currently in a combat class by itself. Looks like there is three options here:
   - A Combat class which MilitaryCombat and CharacterCombat extend.
   - No class (all combat is a bunch of methods)
   - A MilitaryCombat class and a CharacterCombat class (no parent)
      - I'm leaning towards the first. Combat class that handles detection/search. THen the API does a quick check to see if it's character or military combat. If it's military then we do military.combat() if it's character we do character.combat(). Thoughts?
