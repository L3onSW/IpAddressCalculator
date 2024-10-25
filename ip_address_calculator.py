# ======================================================================
# ip_address_calculator.py
#
# IPアドレスとサブネットマスクを入力すると、
# 以下3種類のアドレスを計算し、導出過程と共に結果を示す
#   ・ネットワークアドレス
#   ・ブロードキャストアドレス
#   ・ホストアドレス
#
# Created on 2024/10/26, author: L3onSW
# ======================================================================

import re


class IpAddressCalculator:
    def __init__(self):
        self.ip_address = None
        self.subnet_mask = None
        self.input_start_statement()
        self.input_ip_address()
        self.input_subnet_mask()

    def input_start_statement(self):
        print("=============================================================")
        print("[IPアドレス(10進数)とサブネットマスク(10進数)の入力]")
        print()

    def input_ip_address(self):
        while True:
            ip_address = input(" IPアドレス(10進数)を入力してください: ")
            if self.is_valid_ip(ip_address):
                while True:
                    print(f"    入力されたIPアドレスは {ip_address} です。")
                    confirmation = input("    このIPアドレスでよろしいですか？ (Y/N): ")
                    if confirmation.lower() in ['y', 'yes']:
                        self.ip_address = ip_address
                        return
                    elif confirmation.lower() in ['n', 'no']:
                        print("    IPアドレスを再入力してください。")
                        break
                    else:
                        print("    無効な入力です。YまたはNを入力してください。")
            else:
                print("    無効なIPアドレスです。再入力してください。")

    def input_subnet_mask(self):
        while True:
            subnet_mask = input(" サブネットマスク(10進数)を入力してください: ")
            if self.is_valid_ip(subnet_mask):
                while True:
                    print(f"    入力されたサブネットマスクは {subnet_mask} です。")
                    confirmation = input("    このサブネットマスクでよろしいですか？ (Y/N): ")
                    if confirmation.lower() in ['y', 'yes']:
                        self.subnet_mask = subnet_mask
                        return
                    elif confirmation.lower() in ['n', 'no']:
                        print("    サブネットマスクを再入力してください。")
                        break
                    else:
                        print("    無効な入力です。YまたはNを入力してください。")
            else:
                print("    無効なサブネットマスクです。再入力してください。")

    @staticmethod
    def is_valid_ip(ip):
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            parts = ip.split(".")
            for part in parts:
                if int(part) < 0 or int(part) > 255:
                    return False
            return True
        return False

    @staticmethod
    def ip_to_binary(ip):
        return '.'.join([
            format(int(octet), '08b')
            for octet in ip.split('.')
        ])

    @staticmethod
    def binary_or_operation(binary_str1, binary_str2):
        octets1 = binary_str1.split('.')
        octets2 = binary_str2.split('.')
        return '.'.join([
            format(int(o1, 2) | int(o2, 2), '08b')
            for o1, o2 in zip(octets1, octets2)
        ])

    @staticmethod
    def binary_and_operation(binary_str1, binary_str2):
        octets1 = binary_str1.split('.')
        octets2 = binary_str2.split('.')
        return '.'.join([
            format(int(o1, 2) & int(o2, 2), '08b')
            for o1, o2 in zip(octets1, octets2)
        ])

    @staticmethod
    def binary_xor_operation(binary_str1, binary_str2):
        octets1 = binary_str1.split('.')
        octets2 = binary_str2.split('.')
        return '.'.join([
            format(int(o1, 2) ^ int(o2, 2), '08b')
            for o1, o2 in zip(octets1, octets2)
        ])

    @staticmethod
    def complement_subnet_mask(self, binary_mask):
        complement_binary = \
            '.'.join([
                format(~int(octet, 2) & 0xFF, '08b')
                for octet in binary_mask.split('.')
            ])
        complement_decimal = self.binary_to_decimal(complement_binary)
        return complement_binary, complement_decimal

    @staticmethod
    def binary_to_decimal(binary_str):
        return '.'.join([
            str(int(octet, 2))
            for octet in binary_str.split('.')
        ])

    @staticmethod
    def add_cidr_suffix(decimal_str, binary_mask):
        cidr_suffix = \
            sum(
                bin(int(octet, 2)).count('1')
                for octet in binary_mask.split('.')
            )
        return f"{decimal_str}/{cidr_suffix}"

    def get_network_address(self):
        binary_ip = self.ip_to_binary(self.ip_address)
        binary_subnet_mask = self.ip_to_binary(self.subnet_mask)
        binary_network_address = \
            self.binary_and_operation(binary_ip, binary_subnet_mask)
        network_address = \
            self.binary_to_decimal(binary_network_address)
        network_address_with_cidr = \
            self.add_cidr_suffix(network_address, binary_subnet_mask)
        print()
        print("=============================================================")
        print("[ネットワークアドレスの導出]")
        print()
        print(f"IPアドレス{self.ip_address}、サブネットマスク{self.subnet_mask}に対して、")
        print("ネットワークアドレスを求めると、以下のようになります。")
        print()
        print(f"     {binary_ip} = {self.ip_address}")
        print(f"AND) {binary_subnet_mask} = {self.subnet_mask}")
        print("     ----------------------------------------------------")
        print(f"     {binary_network_address} = {network_address_with_cidr}")

    def get_broadcast_address(self):
        binary_ip = \
            self.ip_to_binary(self.ip_address)
        binary_subnet_mask = \
            self.ip_to_binary(self.subnet_mask)
        binary_subnet_mask_complement, subnet_mask_complement = \
            self.complement_subnet_mask(self, binary_subnet_mask)
        binary_broadcast_address = \
            self.binary_or_operation(binary_ip, binary_subnet_mask_complement)
        broadcast_address = \
            self.binary_to_decimal(binary_broadcast_address)
        print()
        print("=============================================================")
        print("[ブロードキャストアドレスの導出]")
        print()
        print(f"IPアドレス{self.ip_address}、サブネットマスク{self.subnet_mask}に対して、")
        print("ブロードキャストアドレスを求めると、以下のようになります。")
        print()
        print(f"     {binary_ip} = {self.ip_address}")
        print((
            f"OR)  {binary_subnet_mask_complement} = "
            f"{subnet_mask_complement} = サブネットマスクの補数"
        ))
        print("     ----------------------------------------------------")
        print(f"     {binary_broadcast_address} = {broadcast_address}")
        return broadcast_address

    def get_host_address(self):
        binary_ip = \
            self.ip_to_binary(self.ip_address)
        binary_subnet_mask = \
            self.ip_to_binary(self.subnet_mask)
        binary_subnet_mask_complement, subnet_mask_complement = \
            self.complement_subnet_mask(self, binary_subnet_mask)
        binary_host_address = \
            self.binary_and_operation(binary_ip, binary_subnet_mask_complement)
        host_address = \
            self.binary_to_decimal(binary_host_address)
        print()
        print("=============================================================")
        print("[ホストアドレスの導出]")
        print()
        print(f"IPアドレス{self.ip_address}、サブネットマスク{self.subnet_mask}に対して、")
        print("ホストアドレスを求めると、以下のようになります。")
        print()
        print(f"     {binary_ip} = {self.ip_address}")
        print((
            f"AND) {binary_subnet_mask_complement} = "
            f"{subnet_mask_complement} = サブネットマスクの補数"
        ))
        print("     ----------------------------------------------------")
        print(f"     {binary_host_address} = {host_address}")
        return host_address
