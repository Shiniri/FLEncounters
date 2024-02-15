# FLEncounters

This is a simple tool which can be used to create Encounter files
for the game Freelancer. It's advantage as opposed to simple .ini
editing is that created encounters are validated and your Freelancer
directory is parsed, so that no buggy encounters (should) be possible
to create.


## Installation

You should be able to simple run the .exe provided in the repo.
If you want, you can also run main.py (if you have the right
dependencies) and build yourself using:

```
pyinstaller -F --noconsole FLEncounters.py
```


## Usage

Workflow to create a complete encounter file is as such:
1. Open the program, to the right you will see a (now empty) listbox of permutations.
2. Add as many or as few permutations as needed. You can also rename or delete them.
3. Set each permutation using the entry fields and dropdowns on the left.
NOTE: Most widgets are validated only when you _leave_ the widget, meaning you should
just click into some other widget (not just empty space between them) so your progress
is saved. (I know it sucks but Tkinter is bugging around for me.)
4. Once you are done simply press the create encounter button and provide the app
with an .ini file in which the encounter should be saved.
5. The created .ini file will contain some commented-out lines, which __do not__ go
into the encounters directory, but should be copied to the appropriate solar file
in which the encounter will appear. (I will expand this in some future version.)

Please keep an eye out for the changelog, in case anything related to the workflow
is updated.