# ======================================================================
# example.py
# IpAddressCalculatorの使用例
# IPアドレスとサブネットマスクを入力すると、
# 以下3種類のアドレスを計算し、導出過程と共に結果を示す
#   ・ネットワークアドレス
#   ・ブロードキャストアドレス
#   ・ホストアドレス
#
# Created on 2024/10/26, author: L3onSW
# ======================================================================

import ip_address_calculator as ipac

calculator = ipac.IpAddressCalculator()
# ネットワークアドレスの導出
calculator.get_network_address()
# ブロードキャストアドレスの導出
calculator.get_broadcast_address()
# ホストアドレスの導出
calculator.get_host_address()
