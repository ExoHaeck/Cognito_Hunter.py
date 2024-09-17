import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import init, Fore

# Inicializa colorama para sistemas Windows
init(autoreset=True)

# ASCII art para "HUNTERCOGNITO" en color púrpura
ascii_art = f"""
{Fore.MAGENTA}
 ██████╗ ██████╗  ██████╗ ███╗   ██╗██╗████████╗ ██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
██╔════╝██╔═══██╗██╔════╝ ████╗  ██║██║╚══██╔══╝██╔═══██╗    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║██║  ███╗██╔██╗ ██║██║   ██║   ██║   ██║    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██║     ██║   ██║██║   ██║██║╚██╗██║██║   ██║   ██║   ██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║██║   ██║   ╚██████╔╝    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

"""

def buscar_cognito_en_url(url):
    try:
        response = requests.get(url, timeout=10)  # Timeout de 10 segundos para la solicitud
        response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta HTTP

        # Solo mostrar las URLs que devuelvan código 200
        if response.status_code == 200:
            # Analiza el HTML de la página para buscar referencias a cognito
            soup = BeautifulSoup(response.content, 'html.parser')
            if 'cognito' in soup.prettify().lower():
                return True
            else:
                return False
        else:
            return False

    except requests.exceptions.HTTPError as http_err:
        # Comentado para evitar impresión de errores no deseados
        # print(f"Error HTTP al hacer la solicitud a {url}: {http_err}")
        return False
    except requests.exceptions.Timeout as timeout_err:
        # Comentado para evitar impresión de errores no deseados
        # print(f"Timeout al hacer la solicitud a {url}: {timeout_err}")
        return False
    except requests.exceptions.RequestException as req_err:
        # Comentado para evitar impresión de errores no deseados
        # print(f"Error al hacer la solicitud a {url}: {req_err}")
        return False

def buscar_en_urls(urls):
    cognito_urls = []
    for url in urls:
        try:
            if buscar_cognito_en_url(url):
                cognito_urls.append(url)
                print(f"{Fore.GREEN}Se encontró AWS Cognito en: {url}{Fore.RESET}")
        except Exception as e:
            # Comentado para evitar impresión de errores no deseados
            # print(f"Error al procesar la URL {url}: {str(e)}")
            pass

    return cognito_urls

def main():
    # Imprime el ASCII art al inicio del programa
    print(ascii_art)

    parser = argparse.ArgumentParser(description='Herramienta para buscar AWS Cognito en URLs')
    parser.add_argument('-u', '--url', type=str, help='URL individual a verificar')
    parser.add_argument('-f', '--file', type=str, help='Archivo que contiene URLs (una por línea)')

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, 'r') as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    else:
        parser.print_help()
        return

    if not urls:
        print("No se proporcionaron URLs válidas.")
        return

    # Busca AWS Cognito en cada URL de la lista
    urls_con_cognito = buscar_en_urls(urls)

    # Muestra los resultados encontrados
    if urls_con_cognito:
        print("\nURLs con AWS Cognito encontradas:")
        for idx, url in enumerate(urls_con_cognito, start=1):
            print(f"{idx}. {url}")
    else:
        print("\nNo se encontraron URLs con AWS Cognito.")

    # Imprime el mensaje de derechos reservados al final
    print(f"\n{Fore.RED}Derechos reservados a Agrawain.{Fore.RESET}")
    print(f"{Fore.RED}Blog: https://www.hacksyndicate.tech/{Fore.RESET}")

if __name__ == "__main__":
    main()
