#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import serial
import struct
from typing import List, Optional, Sequence

class DynPick:
    # LPFとゼロ点の設定は未実装，他は実装済み
    ver: str = '25.10.31'  # 最終更新日
    # 変数変換（型の明確化と初期値の整合性）
    # - is_started: int -> bool
    # - force: 3要素 -> 6要素（Fx, Fy, Fz, Mx, My, Mz）
    is_started: bool = False
    force: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # 校正パラメータ（クラス全体で共有）
    sensitivity: List[float] = [65.470, 65.440, 65.080, 1638.500, 1639.250, 1640.750]
    zero_output: List[int] = [0x2000, 0x2000, 0x2000, 0x2000, 0x2000, 0x2000]
    def __init__(self, port):
        self.ser = serial.Serial(
            port,
            baudrate = 921600,
            # parity = serial.PARITY_NONE,
            # bytesize = serial.EIGHTBITS,
            # stopbits = serial.STOPBITS_ONE,
            # timeout = None,
            # xonxoff = 0,
            # rtscts = 0,
            )
        self.stop_continuous_read()
    def __del__(self):
        self.close()
    def close(self):
        if self.ser.is_open:
            self.stop_continuous_read()
            self.ser.close()
    def show_firmware_version(self):
        time.sleep(0.100)
        self.ser.flush()
        self.ser.write(b'V')
        time.sleep(0.100)
        in_waiting = self.ser.in_waiting
        if in_waiting > 0:
            print(self.ser.read(in_waiting).decode())
    def show_sensitivity(self):
        time.sleep(0.100)
        self.ser.flush()
        self.ser.write(b'p')
        time.sleep(0.100)
        in_waiting = self.ser.in_waiting
        if in_waiting > 0:
            print(self.ser.read(in_waiting).decode())

    def set_sensitivity(self) -> bool:
        """センサから感度（sensitivity）を読み取り、クラス属性に保存する。
        
        センサに 'p' コマンドを送信して受信した6軸の感度データを解析し、
        クラス全体の `sensitivity` 属性に設定します。
        
        戻り値:
            成功時 True、失敗時 False
        
        使用例:
            dpick = DynPick('COM4')
            if dpick.set_sensitivity():
                print('感度の取得に成功しました')
                print(DynPick.sensitivity)
        """
        time.sleep(0.100)
        self.ser.flush()
        self.ser.write(b'p')
        time.sleep(0.100)
        in_waiting = self.ser.in_waiting
        if in_waiting > 0:
            recv = self.ser.read(in_waiting).decode()
            # 応答形式の例: "Sens X:65.470 Y:65.440 Z:65.080 Mx:1638.500 My:1639.250 Mz:1640.750\r\n"
            # 数値を抽出してクラス属性に格納
            try:
                import re
                # 浮動小数点数を抽出（小数点を含む数値）
                numbers = re.findall(r'\d+\.\d+', recv)
                if len(numbers) == 6:
                    # クラス属性に保存
                    DynPick.sensitivity = [float(n) for n in numbers]
                    return True
                else:
                    print(f'Expected 6 sensitivity values, but got {len(numbers)}: {numbers}')
                    return False
            except Exception as e:
                print(f'Failed to parse sensitivity data: {e}')
                print(f'Received data: {recv}')
                return False
        else:
            print('No data received from sensor.')
            return False

    def read_temperature(self) -> Optional[float]:
        time.sleep(0.100)
        self.ser.flush()
        self.ser.write(b'T')
        time.sleep(0.100)
        in_waiting = self.ser.in_waiting
        if in_waiting > 0:
            recv = self.ser.read(in_waiting)
            data = struct.unpack('=4s2B', recv)
            return float(int(data[0].decode(), 16)) / 16.0
        else:
            return None

    def read_once(self) -> List[float]:
        self.ser.write(b'R')
        time.sleep(0.020)
        in_waiting = self.ser.in_waiting
        if in_waiting == 27:
            recv = self.ser.read(in_waiting)
            data = struct.unpack('=B4s4s4s4s4s4s2B', recv)[1:7]
            return self.bytesToDouble(list(data))
        else:
            print('No available data.')
            return [float('nan')] * 6

    def start_continuous_read(self):
        self.ser.flush()
        self.ser.write(b'S')
        while self.ser.in_waiting < 27*2:
            time.sleep(1e-3)
        self.is_started = True
        self.force = self.read_continuous()
    def stop_continuous_read(self):
        self.ser.write(b'E')
        time.sleep(0.020)
        self.ser.flush()
        self.is_started = False
    def read_continuous(self) -> List[float]:
        # 13	0D	CR
        # 10	0A	LF
        if self.is_started:
            in_waiting = self.ser.in_waiting
            if in_waiting >= 27*2:
                recv = self.ser.read(in_waiting)
                if 0x0A in recv:
                    ii = recv.rfind(0x0A)
                    recv = recv[ii-27+1:ii+1]
                    if recv[25] == 0x0D:
                        data = struct.unpack('=B4s4s4s4s4s4s2B', recv)[1:7]
                        self.force = self.bytesToDouble(list(data))
                    # self.ser.flush()
                return self.force
            else:
                return self.force
        else:
            print('Data send is NOT started.')
            return self.force

    @classmethod
    def bytesToDouble(cls, argBytes6: Sequence[bytes]) -> List[float]:
        """受信した6軸データ（各4文字の16進ASCII）をSI単位へ変換する。

        引数:
            argBytes6: 長さ6の配列。各要素は b"xxxx" 形式の16進ASCIIバイト列。

        戻り値:
            [Fx, Fy, Fz, Mx, My, Mz] の6要素（float）。
        """
        # 16進ASCII文字列 -> int
        hex_strs = [b.decode() if isinstance(b, (bytes, bytearray)) else str(b) for b in argBytes6]
        retInt6 = [int(s, 16) for s in hex_strs]

        # ゼロ点補正および感度によるスケーリング
        retDouble6 = [
            float(retInt6[i] - cls.zero_output[i]) / cls.sensitivity[i]
            for i in range(6)
        ]
        return retDouble6

    @classmethod
    def set_calibration(cls, sensitivity: Optional[List[float]] = None, zero_output: Optional[List[int]] = None) -> None:
        """クラス全体の校正値を設定する。

        引数:
            sensitivity: 6要素の感度リスト（例: [Fx, Fy, Fz, Mx, My, Mz]）
            zero_output: 6要素のゼロ点リスト（整数、例: 0x2000 等）
        """
        if sensitivity is not None:
            if len(sensitivity) != 6:
                raise ValueError('sensitivity must be a list of 6 elements.')
            cls.sensitivity = sensitivity
        if zero_output is not None:
            if len(zero_output) != 6:
                raise ValueError('zero_output must be a list of 6 elements.')
            cls.zero_output = zero_output

if __name__ == '__main__':
    # ls -l /dev/tty.* # for macOS
    # dpick = DynPick('/dev/tty.usbserial-AU02EQ8G')
    # dpick = DynPick('/dev/tty.usbserial-AU05U761')    
    # See device manager for windows OS
    dpick = DynPick('COM4')

    dpick.show_firmware_version()
    dpick.show_sensitivity()
    print(str(dpick.read_temperature())+'(deg C)')

    data = dpick.read_once()
    print(data)
    print("[N], [Nm]")