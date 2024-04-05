import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request received:", self.path)
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Obter o diretório do script
            script_dir = os.path.dirname(os.path.realpath(__file__))
            # Construir o caminho completo para index.html
            index_file_path = os.path.join(script_dir, 'index.html')
            # Abrir o arquivo index.html
            with open(index_file_path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/imgs/'):
            try:
                # Extrai o nome do arquivo de imagem da solicitação
                image_name = self.path.split('/')[-1]
                # Define o tipo de conteúdo apropriado para a imagem
                content_type = 'image/jpeg' if image_name.endswith('.jpg') else 'image/png'
                # Envia uma resposta de sucesso com o tipo de conteúdo apropriado
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                # Obter o diretório do script
                script_dir = os.path.dirname(os.path.realpath(__file__))
                # Construir o caminho completo para a imagem
                image_path = os.path.join(script_dir, 'imgs', image_name)
                # Abre e envia a imagem solicitada
                with open(image_path, 'rb') as file:
                    self.wfile.write(file.read())
            except IOError:
                # Se houver erro ao abrir a imagem, envia uma resposta 404
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

def main():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server running at http://localhost:8080')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
