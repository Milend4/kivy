from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.garden.mapview import MapMarker
from tinydb import TinyDB, Query

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyACLqaj5emBwWFtBOQiNnXwKwJDDIC60-c",
  authDomain: "reciclatech-e91ee.firebaseapp.com",
  projectId: "reciclatech-e91ee",
  storageBucket: "reciclatech-e91ee.appspot.com",
  messagingSenderId: "396519552913",
  appId: "1:396519552913:web:14604b8ccbbb34c2fccc30",
  measurementId: "G-B4YGM4SSCS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

Builder.load_file('ReciclatechApp.kv')
    
Window.size = (430, 600)
#passo 1: criar um caminho para cadastro ou login para o coletor
#passo 2: fazer o login do coletor
class Login_coletor(Screen):

    def __init__(self, **kwargs):
        super(Login_coletor, self).__init__(**kwargs)
        self.app = App.get_running_app()

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
        self.app = App.get_running_app()

    def cadastrar_usuario(self):
        self.manager.current = 'cadastro_usuario'

    def realizar_login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text

        if email and senha:
            usuario = self.app.login_coletor_bd(email, senha)
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
        self.app = App.get_running_app()

    def cadastrar_coletor(self):
        nome = self.ids.nome.text
        genero = self.ids.genero.text
        cpf = self.ids.cpf.text
        tel = self.ids.tel.text
        empresa = self.ids.nome_empresa.text
        cnpj = self.ids.cnpj.text
        logadouro = self.ids.logadouro.text
        numero = self.ids.numero.text
        estado = self.ids.estado.text
        bairro = self.ids.bairro.text
        email = self.ids.email_cadastro.text
        senha = self.ids.senha_cadastro.text
        if nome and email and senha and cpf and cnpj and empresa and genero and logadouro and bairro and estado and numero and tel:
            if self.app.cadastrar_coletor(nome, genero, cpf, cnpj, empresa, tel, logadouro, numero, estado, bairro, email, senha):
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
        self.app = App.get_running_app()

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
        

        if nome and email and senha and cpf_cnpj and genero and logadouro and bairro and estado and numero and tel:
            if self.app.cadastrar_usuario(nome, genero, cpf_cnpj, tel, logadouro, numero, estado, bairro, email, senha):
                # Limpar os campos após o cadastro
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
    def __init__(self, **kwargs):
        super(Entrar_usuario, self).__init__(**kwargs)
        self.nome_usuario = ""

    def tela_usuario(self):
        super(Entrar_usuario, self).on_enter()
        self.mapa_recife()
        self.boas_vindas_usu(self.nome_usuario)

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
    def salvar_atualizacao(self):
        empresa = self.ids.nome_empresa.text
        cnpj = self.ids.CNPJ.text
        logadouro = self.ids.logadouro.text
        numero = self.ids.numero.text
        estado = self.ids.estado.text
        bairro = self.ids.bairro.text
        print(f"Perfil atualizado: Empresa={empresa}, CNPJ={cnpj}, Logadouro={logadouro}, numero={numero}, Estado= {estado}, Bairro={bairro}")

class Menu_coletor(Screen):
    pass

class Menu_usuario(Screen):
    pass

class Central_ajuda(Screen):
    pass

class Beneficios(Screen):
    pass

class promocoes(Screen):
    pass

class Endereco (Screen):
    pass

class Central_ajuda_coletor(Screen):
    pass

class Solicitacoes(Screen):
    def escolha_usuario(self):
        self.manager.current = 'escolher_solicitacao'

class Escolher_solicitacao(Screen):
    pass

class Editar_conta_coletor(Screen):
    def salvar_perfil(self):
        bio = self.ids.bio.text
        nome = self.ids.nome.text
        genero = self.ids.genero.text
        link = self.ids.link.text

        print(f"Perfil atualizado: Nome={nome}, Bio={bio}, Gênero={genero}, Link={link}")

class Editar_conta(Screen):
    def endereco(self):
        self.manager.current = 'endereco'

    def salvar_perfil(self):
        bio = self.ids.bio.text
        nome = self.ids.nome.text
        genero = self.ids.genero.text
        link = self.ids.link.text

        print(f"Perfil atualizado: Nome={nome}, Bio={bio}, Gênero={genero}, Link={link}")

class Rastrear_descarte(Screen):
    pass

class Area_descarte(Screen):
    def coletores(self):
        self.manager.current = 'area_coletores'

class Area_coletores(Screen):
    def coletores_selecao(self):
        self.manager.current = 'selecionar_coletores'

class Perfil_do_coletor(Screen):
    def coletores_selecao(self):
        self.manager.current = 'chat_usuario'


class Perfil_do_usuario(Screen):
    pass

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

class Gerenciador(ScreenManager):
    pass

class ReciclatechApp(App):
    def build(self):
        tabela = 'bancodedados.json'
        self.db = TinyDB(tabela)

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
        gerenciador.add_widget(Escolher_solicitacao(name='escolher_solicitacao'))
        gerenciador.add_widget(Cadastro_usuario(name='registrar_usuario'))
  
        return gerenciador
    
    def cadastrar_usuario(self, nome, genero, cpf_cnpj, tel, logadouro, numero, estado, bairro, email, senha):
        if not self.email_verificacao_usu(email):
            self.db.insert({
                'nome': nome,
                'genero': genero,
                'cpf_cnpj': cpf_cnpj,
                'tel': tel,
                'logadouro': logadouro,
                'numero': numero,
                'estado': estado,
                'bairro': bairro,
                'email': email,
                'senha': senha
                })
            return True
        else:
            return False
        
    def cadastrar_coletor(self, nome, genero, cpf, cnpj, empresa, tel, logadouro, numero, estado, bairro, email, senha):
        if not self.email_verificacao_col(email):
            self.db.insert({
                'nome': nome,
                'genero': genero,
                'cpf': cpf,
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
            return True
        else:
            return False
        
    def login_coletor_bd(self, email, senha):
        Coletor = Query()
        coletor_cadastrado = self.db.get((Coletor.email == email) & (Coletor.senha == senha))
        return coletor_cadastrado
    
    def email_verificacao_col(self, email):
        Coletor = Query()
        return bool(self.db.get(Coletor.email == email))
    
    def login_usuario_bd(self, email, senha):
        Usuario = Query()
        usuario_cadastrado = self.db.get((Usuario.email == email) & (Usuario.senha == senha))
        return usuario_cadastrado

    def email_verificacao_usu(self, email):
        Usuario = Query()
        return bool(self.db.get(Usuario.email == email))
        
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
                pass
        else:
            pass
      
if __name__ == '__main__':
    ReciclatechApp().run()