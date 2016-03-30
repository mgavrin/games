Setup:
    This code requires python 2.7 and a compatible version of pygame.
    You can download python 2.7 here:
    https://www.python.org/downloads/release/python-2710/
    Pygame is available here:
    http://www.pygame.org/download.shtml
    The main interface is in mirror_machine_analyzer.py.
    Sample test cases collected from actual gameplay are included in test_cases.py.
    A set of screenshots of impossible scenarios are included in the "Mirror machine example images" folder. 

Images:
    Zoombini feature images are taken from screenshots from the game Zoombinis. I make no claim to these images and
    am using them only for commentary on the game.

Interface:
    To bring up the analyzer interface, run the main file mirror_machine_analyzer.py. The boxes on the upper left of the GUI represent the
    zoombinis to be sent across (top pair) and the filters you have to match them to (bottom pair, below the
    corresponding zoombinis). The boxes on the upper right represent the filters that can be moved around. To set up a problem
    instance, left-click part of any box to advance through the possible features, and right-click to see the previous feature.
    A blank space indicates the absence of a feature on the filter in question. The word "rotator" indicates a rotating filter
    whose value is determined by the filter behind it.
    Once the problem instance is entered, click the "analyze" button. If a solution exists, it will be displayed at the bottom
    of the window and printed in the shell as a series of filter numbers. Filters are numbered left to right and top to bottom.
    If no solution exists, the boxes on the bottom will remain blank and the shell will announce that the instance is unsolvable.
    Clicking the reset button will reset all zoombinis and filters.
    
    The file test_cases.py includes some sample instances we found during gameplay and used for testing the code.
    Running this file will indicate whether the test cases are solvable or unsolvable, but will not bring up the GUI.

