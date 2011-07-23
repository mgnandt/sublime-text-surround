Surround (Sublime Text Plugin)
==============================

This plugin implements the basic functionality of [surround.vim](https://github.com/tpope/vim-surround) as a Sublime Text plugin.

Installation
------------

Place surround.py in the User packages directory of Sublime Text.
Merge any desired keyboard shortcuts in surround.sublime-keymap with your Sublime Text user key bindings.

Commands
--------

When any of the surround commands are executed, Sublime Text will request a character (or two characters, for the replace_surround command) from the user via the input panel. Entering any half of a commonly used surrounding pair (parenthesis, brackets, braces, or angle brackets) will correctly add, remove, or replace the proper pair.

### add\_surround

- The add\_surround command surrounds a selection or the word around the cursor with the user's desired character.  
- The add\_surround command requires a single character as input from the user - the character that will surround the text.

Given the cursor position: This is a test of the emerg|ency broadcasting system.  
Given the input character: "  
The resulting text is: This is a test of the "emerg|ency" broadcasting system.  

Given the cursor position: This is a test of the emerg|ency broadcasting system.  
Given the input character: )  
The resulting text is: This is a test of the (emerg|ency) broadcasting system.  

Given the text selection: This is a test of the eme|rge|ncy broadcasting system.  
Given the input character: [  
The resulting text is: This is a test of the eme[|rge|]ncy broadcasting system.  

### delete\_surround

- The delete\_surround command removes the surrounding character desired by the user from around a selection or the word around the cursor.  
- The delete\_surround command requires a single character as input from the user - the surrounding character to remove from the text.

Given the cursor position: This is a test of the "emerg|ency" broadcasting system.  
Given the input character: "  
The resulting text is: This is a test of the emerg|ency broadcasting system.  

Given the cursor position: This is a test of (the (emerg|ency) broadcasting) system.  
Given the input character: )  
The resulting text is: This is a test of (the emerg|ency broadcasting) system.  

### replace\_surround

- The replace\_surround command replaces one set of surrounding characters with another.  
- The replace\_surround command requires two characters as input from the user - the first is the existing surround character, the second is the character to exchange.

Given the cursor position: This is a test of the "emerg|ency" broadcasting system.  
Given the input characters: ")  
The resulting text is: This is a test of the (emerg|ency) broadcasting system.  

Shortcuts
---------

- **\[ctrl+shift+a\]** executes the add\_surround command
- **\[ctrl+shift+d\]** executes the delete\_surround command
- **\[ctrl+shift+r\]** executes the replace\_surround command
