import logging

# Configuracoes basicas de logging para nao ser necessario inserir em todos os arquivos

file_name = "log.log"

logging.basicConfig(
    filename=file_name,
    level=logging.DEBUG,
    filemode="w+",
    format="%(asctime)s - %(levelname)s:%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)


def log(begin_message: str, end_message: str, exception_message: str):
    """
    Insercao de logs basicos de inicio, fim e exception.

    Parameters:
    begin_message (str): Mensagem do inicio da execucao.
    end_message (str): Mensagem do fim da execucao.
    exception_message (str): Mensagem de erro.
    """

    def decorator(func):
        def wrapper_func(*args, **kwargs):
            logging.info(begin_message)
            try:
                result = func(*args, **kwargs)
                logging.info(end_message)
                return result
            except Exception as exception:
                logging.info(f"{exception_message}. Erro: {exception}")
                raise exception

        return wrapper_func

    return decorator
