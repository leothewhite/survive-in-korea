# X, Y 값이 필요한 변수를 위한 클래스
class VariableXY:
    def __init__(self, x, y, img=None, sprite=None) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.sprite = sprite
        pass


# left, right 값이 필요한 변수를 위한 클래스
class VariableLR:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
        pass
