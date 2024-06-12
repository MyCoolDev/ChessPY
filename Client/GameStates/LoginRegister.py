from Client.GameStates.GlobalStateImport import *


class LoginRegisterState(BaseState):
    def __init__(self, state_manager: StateManager, screen: pygame.Surface, client_socket: ClientSocket):
        BaseState.__init__(self, state_manager)

        self.client_socket = client_socket
        self.__init_vars(screen)

    def __init_vars(self, screen: pygame.Surface = None):
        self.title = Text("Login To Your Account", "Open Sans", 40, True, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 - 150), (226, 226, 226))
        self.username_textbox = TextBox(pygame.Vector2(608, 50), pygame.Vector2(screen.get_width() / 2 - 304, screen.get_height() / 2 - 53), (29, 29, 29), "Enter Username", "Open Sans", 22, (255, 255, 255), (20, 0, 0, 0), border_radius=5)
        self.password_textbox = TextBox(pygame.Vector2(608, 50), pygame.Vector2(screen.get_width() / 2 - 304, screen.get_height() / 2 + 53), (29, 29, 29), "Enter Password", "Open Sans", 22, (255, 255, 255), (20, 0, 0, 0), border_radius=5)
        self.login_button = Button(pygame.Vector2(198, 50), pygame.Vector2(screen.get_width() / 2 - 150, screen.get_height() / 2 + 200), (74, 114, 255), "Login", "Open Sans", 24, (255, 255, 255), border_radius=5)
        self.register_button = Button(pygame.Vector2(280, 50), pygame.Vector2(screen.get_width() / 2 + 110, screen.get_height() / 2 + 200), (122, 122, 122), "Create an account", "Open Sans", 24, (255, 255, 255), border_radius=5)
        self.login_status = False

    def update(self, dt: float, events: list):
        self.username_textbox.update(dt, events)
        self.password_textbox.update(dt, events)

        if self.login_button.update(dt, events):
            self.client_socket.send_request({'event': "login", 'data': {'username': self.username_textbox.text.txt, 'password': self.password_textbox.text.txt}})

        if self.register_button.update(dt, events):
            self.client_socket.send_request({'event': "register", 'data': {'username': self.username_textbox.text.txt, 'password': self.password_textbox.text.txt}})

        for i, error in enumerate(self.client_socket.error_box):
            if error.update(dt, events):
                self.client_socket.error_box.pop(i)

    def render(self, screen: pygame.Surface):
        self.title.render(screen)
        self.username_textbox.render(screen)
        self.password_textbox.render(screen)
        self.login_button.render(screen)
        self.register_button.render(screen)

        for i, error in enumerate(self.client_socket.error_box):
            error.create_error_box(screen.get_height() - 30 - ((30 + 160) * i), screen).render(screen)
