# APP: Autorun Detector
# Import Libraries
from psutil import disk_partitions
from time import sleep
import os
import glob
import shutil
import stat

class DiskMonitor:
    def __init__(self):
        print("Verificando partições...")
        self.previous_disks = self.get_current_disks()

    def get_current_disks(self):
        # Retorna a lista atual de dispositivos conectados.
        partitions = disk_partitions()
        return [item.device for item in partitions]

    def verificar_disk(self):
        # Monitora e verifica se há novos dispositivos ou se algum foi removido.
        while True:
            sleep(1)
            actual_devices = self.get_current_disks()

            # Verificar se um novo dispositivo foi adicionado
            if len(self.previous_disks) < len(actual_devices):
                print("Foi adicionado um novo dispositivo")
                self.previous_disks = actual_devices  # Atualiza a lista de dispositivos anteriores
                self.get_in_actual_disk(actual_devices[-1])

            # Verificar se um dispositivo foi removido
            elif len(self.previous_disks) > len(actual_devices):
                print("Um dispositivo foi removido")
                self.previous_disks = actual_devices  # Atualiza a lista de dispositivos anteriores

    def get_in_actual_disk(self, disk):
        # Navega até o disco atual e procura arquivos autorun
        os.chdir(disk)
        current_disk = os.getcwd()
        print(f"Analyzing disk: {current_disk}")
        arquivos_inf = self.find_autorun(current_disk)

        if arquivos_inf:
            for arquivo in arquivos_inf:
                print(f"File found: {arquivo}")
                n = input("Do you want to delete? [y/n] ")
                if n.lower() == "y":
                    confirm = input(f"{arquivo}, Are you sure (Y/N)? ")
                    if confirm.lower() == "y":
                        if os.path.isfile(arquivo):
                            try:
                                # Tenta remover o arquivo
                                os.remove(arquivo)
                                print("File deleted successfully.")
                            except PermissionError:
                                print("Permission denied. Attempting to change permissions...")
                                try:
                                    os.chmod(arquivo, stat.S_IWRITE)  # Mudar permissões para permitir escrita
                                    os.remove(arquivo)
                                    print("File deleted successfully.")
                                except Exception as e:
                                    print(f"Failed to delete file: {e}")
                        elif os.path.isdir(arquivo):
                            try:
                                # Tenta remover o diretório e todo o seu conteúdo
                                shutil.rmtree(arquivo)
                                print("Directory deleted successfully.")
                            except PermissionError:
                                print("Permission denied. Attempting to change permissions...")
                                try:
                                    os.chmod(arquivo, stat.S_IWRITE)  # Mudar permissões para permitir escrita
                                    shutil.rmtree(arquivo)
                                    print("Directory deleted successfully.")
                                except Exception as e:
                                    print(f"Failed to delete directory: {e}")
                    else:
                        print("The file/directory will not be deleted.")
                elif n.lower() == "n":
                    print("The file/directory will not be deleted.")
                else:
                    print("Invalid choice.")
        else:
            print("Nenhum arquivo .inf encontrado.")

    def find_autorun(self, directory="."):
        # Procura arquivos .inf no diretório especificado
        pattern = "*.inf"  # Padrão para arquivos .inf
        search_path = os.path.join(directory, pattern)  # Caminho completo do padrão
        return glob.glob(search_path)  # Retorna a lista de arquivos encontrados

# Criando uma instância da classe DiskMonitor e executando o método verificar_disk
monitor = DiskMonitor()
monitor.verificar_disk()
