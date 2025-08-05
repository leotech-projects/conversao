#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para coletar informações do sistema (somente leitura)
e integrar com Claude via API - Versão Windows Compatible
"""

import os
import sys
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# Importações condicionais
try:
    import psutil
except ImportError:
    print("ERRO: psutil nao instalado. Execute: pip install psutil")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERRO: requests nao instalado. Execute: pip install requests")
    sys.exit(1)

# winreg só existe no Windows
if platform.system() == 'Windows':
    try:
        import winreg
    except ImportError:
        print("AVISO: winreg nao disponivel (executando em ambiente nao-Windows)")
        winreg = None
else:
    winreg = None

class SystemInfoReader:
    def __init__(self):
        self.info = {}
        
    def get_system_info(self):
        """Coleta informações básicas do sistema"""
        self.info['system'] = {
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            'timestamp': datetime.now().isoformat()
        }
        
    def get_hardware_info(self):
        """Coleta informações de hardware"""
        self.info['hardware'] = {
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'disk_usage': []
        }
        
        # Informações de disco
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.info['hardware']['disk_usage'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': (usage.used / usage.total) * 100
                })
            except PermissionError:
                continue
                
    def get_installed_programs_windows(self):
        """Coleta programas instalados no Windows (via Registry)"""
        if platform.system() != 'Windows' or winreg is None:
            return []
            
        programs = []
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for path in registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    version = ""
                                    publisher = ""
                                    
                                    try:
                                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    except FileNotFoundError:
                                        pass
                                        
                                    try:
                                        publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    except FileNotFoundError:
                                        pass
                                    
                                    programs.append({
                                        'name': name,
                                        'version': version,
                                        'publisher': publisher
                                    })
                                except FileNotFoundError:
                                    continue
                        except Exception:
                            continue
            except Exception as e:
                print(f"AVISO: Erro ao acessar registry {path}: {e}")
                continue
                
        return programs
    
    def get_installed_programs_linux(self):
        """Coleta programas instalados no Linux"""
        programs = []
        
        # Tentar diferentes gerenciadores de pacotes
        package_managers = [
            ('dpkg', ['dpkg', '-l']),
            ('rpm', ['rpm', '-qa']),
            ('pacman', ['pacman', '-Q']),
            ('snap', ['snap', 'list']),
            ('flatpak', ['flatpak', 'list'])
        ]
        
        for manager, cmd in package_managers:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    programs.append({
                        'manager': manager,
                        'output': result.stdout[:5000]  # Limitar tamanho
                    })
            except:
                continue
                
        return programs
    
    def get_installed_programs_mac(self):
        """Coleta programas instalados no macOS"""
        programs = []
        
        # Aplicações na pasta Applications
        apps_path = Path("/Applications")
        if apps_path.exists():
            for app in apps_path.glob("*.app"):
                programs.append({
                    'name': app.name,
                    'path': str(app)
                })
        
        # Homebrew
        try:
            result = subprocess.run(['brew', 'list'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                programs.append({
                    'manager': 'homebrew',
                    'packages': result.stdout.split('\n')[:100]  # Limitar
                })
        except:
            pass
            
        return programs
    
    def get_installed_programs(self):
        """Coleta programas instalados baseado no SO"""
        os_name = platform.system()
        
        if os_name == 'Windows':
            self.info['programs'] = self.get_installed_programs_windows()
        elif os_name == 'Linux':
            self.info['programs'] = self.get_installed_programs_linux()
        elif os_name == 'Darwin':  # macOS
            self.info['programs'] = self.get_installed_programs_mac()
        else:
            self.info['programs'] = []
    
    def get_network_info(self):
        """Coleta informações de rede (sem dados sensíveis)"""
        self.info['network'] = {
            'interfaces': []
        }
        
        for interface, addrs in psutil.net_if_addrs().items():
            interface_info = {
                'name': interface,
                'addresses': []
            }
            
            for addr in addrs:
                # Não incluir IPs específicos por segurança
                interface_info['addresses'].append({
                    'family': str(addr.family),
                    'has_address': bool(addr.address)
                })
            
            self.info['network']['interfaces'].append(interface_info)
    
    def get_running_processes(self):
        """Coleta processos em execução (apenas nomes, sem detalhes)"""
        processes = []
        
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                processes.append({
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Ordenar por uso de CPU e pegar apenas os top 20
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        self.info['processes'] = processes[:20]
    
    def collect_all_info(self):
        """Coleta todas as informações do sistema"""
        print("Coletando informacoes do sistema...")
        
        self.get_system_info()
        print("OK Informacoes do sistema")
        
        self.get_hardware_info()
        print("OK Informacoes de hardware")
        
        self.get_installed_programs()
        print("OK Programas instalados")
        
        self.get_network_info()
        print("OK Informacoes de rede")
        
        self.get_running_processes()
        print("OK Processos em execucao")
        
        return self.info
    
    def save_to_file(self, filename="system_info.json"):
        """Salva informações em arquivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.info, f, indent=2, ensure_ascii=False)
        print(f"OK Informacoes salvas em {filename}")
    
    def send_to_claude(self, api_key, query="Analise as informações do meu sistema"):
        """Envia informações para Claude via API"""
        url = "https://api.anthropic.com/v1/messages"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        
        # Limitar tamanho dos dados para não exceder limite da API
        info_str = json.dumps(self.info, indent=2)
        if len(info_str) > 50000:  # Limitar a ~50KB
            # Resumir informações se muito grandes
            summary = {
                'system': self.info.get('system', {}),
                'hardware': self.info.get('hardware', {}),
                'programs_count': len(self.info.get('programs', [])),
                'processes_count': len(self.info.get('processes', [])),
                'note': 'Dados resumidos devido ao tamanho. Use save_to_file() para dados completos.'
            }
            info_str = json.dumps(summary, indent=2)
        
        data = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": f"{query}\n\nInformações do sistema:\n{info_str}"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            claude_response = result['content'][0]['text']
            
            print("\n" + "="*50)
            print("RESPOSTA DO CLAUDE:")
            print("="*50)
            print(claude_response)
            
            return claude_response
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com Claude: {e}")
            return None

def main():
    """Função principal"""
    print("=== COLETOR DE INFORMACOES DO SISTEMA ===")
    print("Este script coleta informacoes do sistema (somente leitura)")
    print(f"Sistema detectado: {platform.system()}")
    print()
    
    reader = SystemInfoReader()
    
    # Coletar informações
    try:
        info = reader.collect_all_info()
        print(f"\nOK Coleta concluida! {len(json.dumps(info))} caracteres de dados")
    except Exception as e:
        print(f"ERRO durante coleta: {e}")
        return
    
    # Opções do usuário
    while True:
        print("\nO que deseja fazer?")
        print("1. Salvar em arquivo JSON")
        print("2. Enviar para Claude (requer API key)")
        print("3. Mostrar resumo")
        print("4. Sair")
        
        choice = input("\nEscolha (1-4): ").strip()
        
        if choice == '1':
            filename = input("Nome do arquivo (enter para 'system_info.json'): ").strip()
            if not filename:
                filename = "system_info.json"
            try:
                reader.save_to_file(filename)
            except Exception as e:
                print(f"ERRO ao salvar: {e}")
            
        elif choice == '2':
            api_key = input("Insira sua API key da Anthropic: ").strip()
            if api_key:
                query = input("Pergunta para Claude (enter para analise padrao): ").strip()
                if not query:
                    query = "Analise as informacoes do meu sistema e me de insights uteis"
                try:
                    reader.send_to_claude(api_key, query)
                except Exception as e:
                    print(f"ERRO ao comunicar com Claude: {e}")
            
        elif choice == '3':
            try:
                print("\n=== RESUMO DO SISTEMA ===")
                print(f"OS: {info['system']['os']} {info['system']['os_version']}")
                print(f"Arquitetura: {info['system']['architecture'][0]}")
                print(f"CPU: {info['hardware']['cpu_count']} cores")
                print(f"RAM: {info['hardware']['memory']['total'] / (1024**3):.1f} GB")
                print(f"Programas instalados: {len(info.get('programs', []))}")
                print(f"Processos em execucao: {len(info.get('processes', []))}")
            except Exception as e:
                print(f"ERRO ao mostrar resumo: {e}")
            
        elif choice == '4':
            print("Saindo...")
            break
            
        else:
            print("ERRO Opcao invalida!")

if __name__ == "__main__":
    main()