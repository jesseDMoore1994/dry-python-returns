def display_hangman(tries: int) -> str:
    stages = ["""
                    --------
                    |      |
                    |      0
                    |     \\|/
                    |      |
                    |     / \\
                    -
              """,
              """
                    --------
                    |      |
                    |      0
                    |     \\|/
                    |      |
                    |     / 
                    -
              """,
              """
                    --------
                    |      |
                    |      0
                    |     \\|/
                    |      |
                    |    
                    -
              """,
              """
                    --------
                    |      |
                    |      0
                    |     \\|
                    |      |
                    |    
                    -
              """,
              """
                    --------
                    |      |
                    |      0
                    |      |
                    |      |
                    |    
                    -
              """,
              """
                    --------
                    |      |
                    |      0
                    |      
                    |      
                    |    
                    -
              """,
              """
                    --------
                    |      |
                    |      
                    |      
                    |      
                    |    
                    -
              """
              ]
    return stages[tries]
