from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.mapview import MapMarker
import pyrebase
from kivy.uix.label import Label
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.properties import StringProperty


firebaseConfig = {
  'apiKey': "AIzaSyACLqaj5emBwWFtBOQiNnXwKwJDDIC60-c",
  'authDomain': "reciclatech-e91ee.firebaseapp.com",
  'projectId': "reciclatech-e91ee",
  'storageBucket': "reciclatech-e91ee.appspot.com",
  'messagingSenderId': "396519552913",
  'appId': "1:396519552913:web:14604b8ccbbb34c2fccc30",
  'measurementId': "G-B4YGM4SSCS",
  'databaseURL': "https://reciclatech-e91ee-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
mAuth = firebase.auth()
db = firebase.database()

Builder.load_file('ReciclatechApp.kv')
    
Window.size = (430, 600)
#passo 1: criar um caminho para cadastro ou login para o coletor
#passo 2: fazer o login do coletor
class Login_coletor(Screen):

    def __init__(self, **kwargs):
        super(Login_coletor, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def cadastrar_coletor(self):
        self.manager.current = 'cadastro_coletor'


    def realizar_login_col(self):
        email = self.ids.email_input.text
        senha = self.ids.senha_input.text

        if email and senha:
            usuario = self.app.login_coletor_bd(email, senha)
            if usuario:
                self.manager.current = 'entrar_coletor'
            else:
                print('Erro: Email ou senha incorretos.')
        else:
            print('Erro: Preencha todos os campos.')


class Login_usuario(Screen):

    def __init__(self, **kwargs):
        super(Login_usuario, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def cadastrar_usuario(self):
        self.manager.current = 'cadastro_usuario'

    def realizar_login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text

        if email and senha:
            usuario = self.app.login_usuario_bd(email, senha)
            if usuario:
                self.manager.current = 'entrar_usuario'
                
            else:
                print('Erro: Email ou senha incorretos.')
        else:
            print('Erro: Preencha todos os campos.')

#passo 3: fazer o cadastro do coletor 
class Cadastro_coletor(Screen):
    def __init__(self, **kwargs):
        super(Cadastro_coletor, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def cadastrar_coletor(self):
        nome = self.ids.nome.text
        genero = self.ids.genero.text
        usuario = self.ids.usuario.text
        tel = self.ids.tel.text
        empresa = self.ids.nome_empresa.text
        cnpj = self.ids.cnpj.text
        logadouro = self.ids.logadouro.text
        numero = self.ids.numero.text
        estado = self.ids.estado.text
        bairro = self.ids.bairro.text
        email = self.ids.email_cadastro.text
        senha = self.ids.senha_cadastro.text
        if nome and email and senha and usuario and cnpj and empresa and genero and logadouro and bairro and estado and numero and tel:
            if self.app.cadastrar_coletor(nome, genero, usuario, cnpj, empresa, tel, logadouro, numero, estado, bairro, email, senha):
                self.ids.nome.text = ''
                self.ids.genero.text = ''
                self.manager.current = 'resistrar_coletor'
            else:
                print('Erro: Email já cadastrado.')
        else:
            print('Erro: Preencha todos os campos.')

class Cadastro_usuario(Screen):
    def __init__(self, **kwargs):
        super(Cadastro_usuario, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def cadastrar_usuario(self):
        nome = self.ids.nome.text
        genero = self.ids.genero.text
        cpf_cnpj = self.ids.cpf_cnpj.text
        tel = self.ids.tel.text
        logadouro = self.ids.logadouro.text
        numero = self.ids.numero.text
        estado = self.ids.estado.text
        bairro = self.ids.bairro.text
        email = self.ids.email_cadastro.text
        senha = self.ids.senha_cadastro.text
        usuario = self.ids.usuario.text
        
        if nome and email and senha and cpf_cnpj and genero and logadouro and bairro and estado and numero and tel and usuario :
            if self.app.cadastrar_usuario(nome, genero, cpf_cnpj, tel, logadouro, numero, estado, bairro, email, senha, usuario):
                self.ids.nome.text = ''
                self.ids.genero.text = ''
                self.manager.current = 'resistrar_usuario'
            else:
                print('Erro: Email já cadastrado.')
        else:
            print( 'Erro: Preencha todos os campos.')

class Registro_coletor(Screen):
    def voltar_coletor(self):
        self.manager.current = 'login_coletor'

class Registro_usuario(Screen):
    def voltar_usuario(self):
        self.manager.current = 'login_usuario'

#passo 4 fazer a tela inicial do coletor
class Entrar_coletor(Screen):
    mensagem = StringProperty("")

    def on_enter(self, *args):
        super(Entrar_coletor, self).on_enter(*args)
        email = self.manager.get_screen('login_coletor').ids.email_input.text
        try:
            coletores = db.child("schedule").get().val()  
            if coletores:
                coletor_encontrado = None
                for key, value in coletores.items():
                    if value.get("email") == email:
                        coletor_encontrado = value
                        print("Coletor encontrado com o e-mail", email)
                        break
                if coletor_encontrado:
                    self.mensagem = f"[b]Bem-vindo, {coletor_encontrado['usuario']}[/b]!"
                    boas_vindas_label = Label(text=self.mensagem, markup=True, color=(0, 0, 0, 1), font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.24})
                    self.ids.layout.add_widget(boas_vindas_label)
                else:
                    print("Nenhum coletor encontrado com o e-mail", email)
            else:
                print("Nenhum coletor encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)


    def tela_coletor(self):
        super(Entrar_coletor, self).on_enter()
        self.adicionar_mapa()

    def adicionar_mapa(self):
        mapview = self.ids.mapview

    def menu(self):
        self.manager.current = 'menu_coletor'

    def solicitar(self):
        self.manager.current = 'solicitacoes'

    def mensagens(self):
        self.manager.current = 'mensagens'
   
class Entrar_usuario(Screen):
    mensagem = StringProperty("")

    def on_enter(self):
        super(Entrar_usuario, self).on_enter()
        email = self.manager.get_screen('login_usuario').ids.email.text
        try:
            usuarios = db.child("schedule").get().val()  
            if usuarios:
                usuario_encontrado = None
                for key, value in usuarios.items():
                    if value.get("email") == email:
                        usuario_encontrado = value
                        print("Usuário encontrado com o e-mail", email)
                        break
                if usuario_encontrado:
                    self.mensagem = f"[b]Bem-vindo, {usuario_encontrado['usuario']}[/b]!"
                    boas_vindas_label = Label(text=self.mensagem, markup=True, color=(0, 0, 0, 1), font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.24})
                    self.ids.layout.add_widget(boas_vindas_label)
                else:
                    print("Nenhum usuário encontrado com o e-mail", email)
            else:
                print("Nenhum usuário encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)

    
    def tela_usuario(self):
        super(Entrar_usuario, self).on_enter()
        self.mapa_recife()
        

    def mapa_recife(self):
        mapview = self.ids.mapview

        mapview.add_marker('Coleta 1')
        mapview.add_marker('Coleta 2')
        mapview.add_marker('Coleta 3')
        mapview.add_marker('Coleta 4')
        mapview.add_marker('Coleta 5')
        mapview.add_marker('Coleta 6')
        mapview.add_marker('Coleta 7')
        mapview.add_marker('Coleta 8')
        mapview.add_marker('Coleta 9')
        mapview.add_marker('Coleta 10')
        

    def menu(self):
        self.manager.current = 'menu_usuario'

class ColetaMarker(MapMarker):
    pass

class Empresa(Screen):
    def empresa_atualizacoao(self):
        empresa_novo = self.ids.empresa_novo.text
        cnpj_novo = self.ids.CNPJ_novo.text
        logadouro_novo = self.ids.logadouro_novo.text
        numero_novo = self.ids.numero_novo.text
        estado_novo = self.ids.estado_novo.text
        bairro_novo = self.ids.bairro_novo.text
        
        if logadouro_novo and numero_novo and estado_novo and bairro_novo and empresa_novo and cnpj_novo:
            email = self.manager.get_screen('login_coletor').ids.email.text
            if self.app.atualizar_coletor(email, logadouro_novo, numero_novo, estado_novo, bairro_novo,empresa_novo,cnpj_novo):
                self.manager.current = 'menu_coletor'
            else:
                toast('Erro: Não foi possível atualizar o perfil.')
                
        else:
            toast('Erro: Preencha todos os campos.')
    
class Menu_coletor(Screen):
    mensagem = StringProperty("")

    def on_enter(self, *args):
        super(Menu_coletor, self).on_enter(*args)
        email = self.manager.get_screen('login_coletor').ids.email_input.text
        try:
            coletores = db.child("schedule").get().val()  
            if coletores:
                coletor_encontrado = None
                for key, value in coletores.items():
                    if value.get("email") == email:
                        coletor_encontrado = value
                        print("Coletor encontrado com o e-mail", email)
                        break
                if coletor_encontrado:
                    self.mensagem = f"[b]{coletor_encontrado['nome']}[b]"
                    label = Label(text=self.mensagem, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint={'center_x': 0.5, 'center_y': 0.7})
                    self.ids.layout.add_widget(label)
                else:
                    print("Nenhum coletor encontrado com o e-mail", email)
            else:
                print("Nenhum coletor encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)
    
    def coletor(self):
        super(Menu_coletor, self).on_enter()

class Menu_usuario(Screen):
    mensagem = StringProperty("")

    def on_enter(self, *args):
        super(Menu_usuario, self).on_enter(*args)
        email = self.manager.get_screen('login_usuario').ids.email.text
        try:
            usuarios = db.child("schedule").get().val()  
            if usuarios:
                usuario_encontrado = None
                for key, value in usuarios.items():
                    if value.get("email") == email:
                        usuario_encontrado = value
                        print("Coletor encontrado com o e-mail", email)
                        break
                if usuario_encontrado:
                    self.mensagem = f"[b]{usuario_encontrado['nome']}[b]"
                    label = Label(text=self.mensagem, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint={'center_x': 0.5, 'center_y': 0.7})
                    self.ids.layout.add_widget(label)
                else:
                    print("Nenhum coletor encontrado com o e-mail", email)
            else:
                print("Nenhum coletor encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)
    
    def usuario(self):
        super(Menu_usuario, self).on_enter()

class Central_ajuda(Screen):
    pass

class Beneficios(Screen):
    pass

class promocoes(Screen):
    pass

class Endereco (Screen):
    def salvar_endereco(self):
        logadouro_novo = self.ids.logadouro_novo.text
        numero_novo = self.ids.numero_novo.text
        estado_novo = self.ids.estado_novo.text
        bairro_novo = self.ids.bairro_novo.text
        
        if logadouro_novo and numero_novo and estado_novo and bairro_novo:
            email = self.manager.get_screen('login_usuario').ids.email.text
            if self.app.atualizar_usuario(email, logadouro_novo, numero_novo, estado_novo, bairro_novo):
                self.manager.current = 'editar_conta'
            else:
                toast('Erro: Não foi possível atualizar o perfil.')
                
        else:
            toast('Erro: Preencha todos os campos.')


class Central_ajuda_coletor(Screen):
    pass

class Solicitacoes(Screen):
    def escolha_usuario(self):
        self.manager.current = 'perfil_do_usuario'


class Editar_conta_coletor(Screen):
    def salvar_perfil(self):
        novo_nome = self.ids.nome.text
        novo_genero = self.ids.genero.text
        novo_tel = self.ids.tel.text
        
        if novo_nome and novo_genero and novo_tel:
            email = self.manager.get_screen('login_coletor').ids.email.text
            if self.app.atualizar_coletor(email, novo_nome, novo_genero, novo_tel):
                self.manager.current = 'perfil_do_coletor'
            else:
                toast('Erro: Não foi possível atualizar o perfil.')
                
        else:
            toast('Erro: Preencha todos os campos.')

class Editar_conta(Screen):

    def __init__(self, **kwargs):
        super(Editar_conta, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def salvar_perfil(self):
        novo_nome = self.ids.nome_novo.text
        novo_genero = self.ids.genero_novo.text
        novo_tel = self.ids.tel_novo.text
        
        if novo_nome and novo_genero and novo_tel:
            email = self.manager.get_screen('login_usuario').ids.email.text
            if self.app.atualizar_usuario(email, novo_nome, novo_genero, novo_tel):
                self.manager.current = 'perfil_do_usuario'
            else:
                toast('Erro: Não foi possível atualizar o perfil.')
                
        else:
            toast('Erro: Preencha todos os campos.')

    def endereco(self):
        self.manager.current = 'endereco'

class Rastrear_descarte(Screen):
    pass

class Area_descarte(Screen):
    def coletores(self):
        self.manager.current = 'area_coletores'

class Area_coletores(Screen):
    def coletores_selecao(self):
        self.manager.current = 'selecionar_coletores'

class Perfil_do_coletor(Screen):
    nome = StringProperty("")
    empresa = StringProperty("")
    logadouro = StringProperty("")
    numero = StringProperty("")

    def on_enter(self, *args):
        super(Perfil_do_coletor, self).on_enter(*args)

        email_coletor = "apollo.santana@gmail.com"
        try:
            coletor_info = db.child("schedule").get().val()  
            if coletor_info:
                coletor_encontrado = None
                for key, value in coletor_info.items():
                    if value.get("email") == email_coletor:
                        coletor_encontrado = value
                        print("Coletor encontrado com o e-mail", email_coletor)
                        break
                if coletor_encontrado:
                    self.nome = f"[b]{coletor_encontrado['nome']}[b]"
                    label = Label(text=self.nome, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.5, 'center_y': 0.57})
                    self.ids.layout.add_widget(label)
                    self.empresa = f"[b]{coletor_encontrado['empresa']}[b]"
                    label_empresa = Label(text=self.empresa, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.5, 'center_y': 0.5})
                    self.ids.layout.add_widget(label_empresa)
                    self.logadouro = f"[b]{coletor_encontrado['logadouro']},[b]"
                    label_logadouro = Label(text=self.logadouro, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.4, 'center_y': 0.3})
                    self.ids.layout.add_widget(label_logadouro)
                    self.numero = f"[b]{coletor_encontrado['numero']}[b]"
                    label_numero = Label(text=self.numero, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.8, 'center_y': 0.3})
                    self.ids.layout.add_widget(label_numero)
                    self.bairro = f"[b]{coletor_encontrado['bairro']}[b]"
                    label_bairro = Label(text=self.bairro, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.5, 'center_y': 0.25})
                    self.ids.layout.add_widget(label_bairro)
                else:
                    print("Nenhum coletor encontrado com o e-mail", email_coletor)
            else:
                print("Nenhum coletor encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)

    def coletores_selecao(self):
        self.manager.current = 'chat_usuario'


class Perfil_do_usuario(Screen):
    nome = StringProperty("")
    logadouro = StringProperty("")
    numero = StringProperty("")
    bairro = StringProperty("")

    def on_enter(self, *args):
        super(Perfil_do_usuario, self).on_enter(*args)

        email_usuario = "giovana890@gmail.com"
        try:
            usuario_info = db.child("schedule").get().val()  
            if usuario_info:
                usuario_encontrado = None
                for key, value in usuario_info.items():
                    if value.get("email") == email_usuario:
                        usuario_encontrado = value
                        print("Usuário encontrado com o e-mail", email_usuario)
                        break
                if usuario_encontrado:
                    self.nome = f"[b]{usuario_encontrado['nome']}[b]"
                    label = Label(text=self.nome, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.5, 'center_y': 0.57})
                    self.ids.layout.add_widget(label)
                    self.logadouro = f"[b]{usuario_encontrado['logadouro']},[b]"
                    label_logadouro = Label(text=self.logadouro, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.4, 'center_y': 0.3})
                    self.ids.layout.add_widget(label_logadouro)
                    self.numero = f"[b]{usuario_encontrado['numero']}[b]"
                    label_numero = Label(text=self.numero, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.75, 'center_y': 0.3})
                    self.ids.layout.add_widget(label_numero)
                    self.bairro = f"[b]{usuario_encontrado['bairro']}[b]"
                    label_bairro = Label(text=self.bairro, markup=True, color=(0, 0, 0, 1), font_size=28, pos_hint= {'center_x': 0.5, 'center_y': 0.25})
                    self.ids.layout.add_widget(label_bairro)
                else:
                    print("Nenhum usuário encontrado com o e-mail", email_usuario)
            else:
                print("Nenhum usuário encontrado")
        except Exception as e:
            print("Ocorreu um erro durante a consulta:", e)


#passo 5: fazer o chat

class Chat_usuario(Screen):
    pass

class Chat_coletor(Screen):
    pass

#passo 1: criar um caminho para cadastro ou login para o coletor
class Inicial(Screen):
    def entrar_como_coletor(self):
        self.manager.current = 'login_coletor'
    def entrar_como_usuario(self):
        self.manager.current = 'login_usuario'
    def mapa(self):
        mapview = self.ids.mapview
        marker = MapMarker(lat=37.7749, lon=-122.4194)
        mapview.add_marker(marker)

    def realizar_login_coletor(self):
        self.manager.get_screen('login_coletor').realizar_login_col(self.manager)

    def realizar_login_usuario(self):
        self.manager.get_screen('login_usuario').realizar_login(self.manager)

class Gerenciador(ScreenManager):
    pass

class ReciclatechApp(MDApp):
    db = firebase.database()
    def build(self):
        gerenciador = Gerenciador()
        gerenciador.add_widget(Inicial(name='inicial'))
        gerenciador.add_widget(Login_coletor(name='login_coletor'))
        gerenciador.add_widget(Login_usuario(name='login_usuario'))
        gerenciador.add_widget(Cadastro_coletor(name='cadastro_coletor'))
        gerenciador.add_widget(Cadastro_usuario(name='cadastro_usuario'))
        gerenciador.add_widget(Registro_coletor(name='resistrar_coletor'))
        gerenciador.add_widget(Registro_usuario(name='resistrar_usuario'))
        gerenciador.add_widget(Entrar_coletor(name='entrar_coletor'))
        gerenciador.add_widget(Entrar_usuario(name='entrar_usuario'))
        gerenciador.add_widget(Menu_coletor(name='menu_coletor'))
        gerenciador.add_widget(Menu_usuario(name='menu_usuario'))
        gerenciador.add_widget(Area_descarte(name='area_descarte'))
        gerenciador.add_widget(Solicitacoes(name='solicitacoes'))
        gerenciador.add_widget(Empresa(name='empresa'))
        gerenciador.add_widget(Area_coletores(name='area_coletores'))
        gerenciador.add_widget(Perfil_do_coletor(name='selecionar_coletores'))
        gerenciador.add_widget(Perfil_do_usuario(name='perfil_do_usuario'))
        gerenciador.add_widget(Chat_usuario(name='chat_usuario'))
        gerenciador.add_widget(Chat_coletor(name='chat_coletor'))
        gerenciador.add_widget(Editar_conta(name='editar_conta'))
        gerenciador.add_widget(Beneficios(name='beneficios'))
        gerenciador.add_widget(Rastrear_descarte(name='rastrear_descarte'))
        gerenciador.add_widget(Central_ajuda(name='central_ajuda'))
        gerenciador.add_widget(Endereco(name='endereco'))
        gerenciador.add_widget(Editar_conta_coletor(name='editar_conta_coletor'))
        gerenciador.add_widget(Cadastro_usuario(name='registrar_usuario'))
        gerenciador.add_widget(Cadastro_coletor(name='registrar_coletor'))
  
        return gerenciador
    
    def cadastrar_usuario(self, nome, genero, cpf_cnpj, tel, logadouro, numero, estado, bairro, email, senha, usuario):
        if not self.email_verificacao_usu(email):
            db.child("/schedule/").push({
                'nome': nome,
                'genero': genero,
                'cpf_cnpj': cpf_cnpj,
                'tel': tel,
                'logadouro': logadouro,
                'numero': numero,
                'estado': estado,
                'bairro': bairro,
                'email': email,
                'senha': senha,
                'usuario': usuario
                })
            return True
        else:
            return False
        
    def cadastrar_coletor(self, nome, genero, usuario, cnpj, empresa, tel, logadouro, numero,estado, bairro, email, senha):
        if not self.email_verificacao_col(email):
            db.child("/schedule/").push({
                'nome': nome,
                'genero': genero,
                'usuario': usuario,
                'tel': tel,
                'empresa': empresa,
                'cnpj': cnpj,
                'logadouro': logadouro,
                'numero': numero,
                'estado': estado,
                'bairro': bairro,
                'email': email,
                'senha': senha
                })
        else:
            return False
        
    def login_usuario_bd(self, email, senha):
        usuarios = db.child("/schedule/").get().val()
        if usuarios:
            for usuario in usuarios.values():
                if usuario['email'] == email and usuario['senha'] == senha:
                    toast('Login usuário bem-sucedido')
                    return True
        else:
            toast(f'Erro ao fazer login usuário')
            return False
    
    def email_verificacao_col(self, email):
        coletores = db.child("/schedule/").get().val()
        if coletores:
            for coletor in coletores.values():
                if coletor['email'] == email:
                    return True
  
        return False
    
    def login_coletor_bd(self, email, senha):
        usuarios = db.child("/schedule/").get().val()
        if usuarios:
            for usuario in usuarios.values():
                if usuario['email'] == email and usuario['senha'] == senha:
                    toast('Login coletor bem-sucedido')
                    return True
        else:
            toast(f'Erro ao fazer login coletor')
            return False

    def email_verificacao_usu(self, email):
        usuarios = db.child("/schedule/").get().val()
        if usuarios:
            for usuario in usuarios.values():
                if usuario['email'] == email:
                    return True
        return False
        
    def realizar_login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text
        
        if email and senha:
            usuario = self.app.login_usuario_bd(email, senha)
            coletor = self.app.login_coletor_bd(email, senha)
            if usuario:
                self.manager.current = 'entrar_usuario'
            elif coletor:
                self.manager.current = 'entrar_coletor'
            else:
                toast('Erro: Email ou senha incorretos.')
        else:
            toast('Erro: Preencha todos os campos.')

    def atualizar_usuario(self, email, novo_nome, novo_genero, novo_tel, logadouro_novo, numero_novo, estado_novo, bairro_novo):
        # Primeiro, obtenha a chave do usuário com base no e-mail
        usuarios = self.db.child("schedule").get().val()
        if usuarios:
            for chave, usuario in usuarios.items():
                if usuario['email'] == email:
                    # Atualize os dados do usuário com os novos valores
                    self.db.child("schedule").child(chave).update({
                        'nome': novo_nome,
                        'genero': novo_genero,
                        'tel': novo_tel,
                        'logadouro': logadouro_novo,
                        'numero': numero_novo,
                        'estado': estado_novo,
                        'bairro': bairro_novo
                    })
                    return True
        return False
    
    def atualizar_coletor(self, email, novo_nome, novo_genero, novo_tel, CNPJ_novo, logadouro_novo, numero_novo, estado_novo, bairro_novo):
        coletores = self.db.child("schedule").get().val()
        if coletores:
            for chave, coletor in coletores.items():
                if coletor['email'] == email:
                    self.db.child("schedule").child(chave).update({
                        'nome': novo_nome,
                        'genero': novo_genero,
                        'tel': novo_tel,
                        'cnpj': CNPJ_novo,
                        'logadouro': logadouro_novo,
                        'numero': numero_novo,
                        'estado': estado_novo,
                        'bairro': bairro_novo,
                    })
                    return True
        return False
      
if __name__ == '__main__':
    ReciclatechApp().run()