
class token_sequence:
    def __init__(self,ts:list) -> None:
        self.__ts = ts
        self.__idx = 0

    def peek(self)->str:
        return self.__ts[self.__idx]

    def advance(self)->None:
        self.__idx =  self.__idx + 1

    def match(self,token:str)->None:
        actual_token = self.peek()
        if self.peek() == token:
            self.advance()
        else:
            print(
                f'Syntax error: esperado "{token}", mas encontrado "{actual_token}"'
            )
            print('')
            print('Geracao do arquivo SAM cancelada.')
            exit(0)
