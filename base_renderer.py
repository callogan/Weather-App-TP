from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    def __init__(self, weather_service=None):
        self.weather_service = weather_service
        self.rotation = 0.0
        self.vertices = (
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        )
        self.edges = (
            (0, 1), (0, 3), (0, 4),
            (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7),
            (5, 1), (5, 4), (5, 7)
        )
        self.weather_data = None
        self.update_weather()

    def update_weather(self):
        """Get weather updates"""
        self.weather_data = self.weather_service.get_weather("Moscow")
        if self.weather_data:
            print(f"Temperature: {self.weather_data['temperature']['celsius']}°C")
            print(f"Weather: {self.weather_data['description']}")

    @abstractmethod
    def init_gl(self):
        """OpenGL initialization"""
        pass

    @abstractmethod
    def draw(self):
        """Scene drawing"""
        pass

    @abstractmethod
    def resize(self, width: int, height: int):
        """Handling changes of window size"""
        pass

    def get_vertices(self) -> tuple[tuple[float, float, float], ...]:
        """Returns cube peaks"""
        return self.vertices

    def get_edges(self) -> tuple[tuple[int, int], ...]:
        """Returns cube edges"""
        return self.edges

    def get_rotation(self) -> float:
        """Returns current rotation angle"""
        return self.rotation

    def increment_rotation(self, amount: float = 1.0):
        """Increases rotation angle"""
        self.rotation += amount
