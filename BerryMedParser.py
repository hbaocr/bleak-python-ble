from construct import BitStruct, BitsInteger, Flag, Bit, ConstructError
import datetime
# Bit number to its structure
# This is the schema of the actual protocol, but we actually don't need all that stuff.

PARSING_SCHEMA = {
    0: BitStruct(sync_bit=Flag, pulse_beep=Flag, probe_unplugged=Flag, has_signal=Flag, signal_strength=BitsInteger(4)),
    1: BitStruct(sync_bit=Flag, pleth=BitsInteger(7)),
    2: BitStruct(sync_bit=Flag, pr_last_bit=Bit, pulse_research=Flag, no_finger=Flag, bargraph=BitsInteger(4)),
    3: BitStruct(sync_bit=Flag, pr_bits=BitsInteger(7)),
    4: BitStruct(sync_bit=Flag, spo2=BitsInteger(7))
}


packet_dict = {}



def parse(packet:bytearray):
    offset = 0
    data_step=5
    packet_len=len(packet)
    while offset< packet_len:
        packet_dict = {}
        byte_1_data_container = PARSING_SCHEMA[0].parse(packet[offset+0].to_bytes(1, 'big'))
        byte_3_data_container = PARSING_SCHEMA[2].parse(packet[offset+2].to_bytes(1, 'big'))
        packet_dict['signal_strength'] = byte_1_data_container['signal_strength']
        packet_dict['has_signal'] = byte_1_data_container['has_signal']
        packet_dict['bargraph'] = byte_3_data_container['bargraph']
        packet_dict['no_finger'] = byte_3_data_container['no_finger']
        packet_dict['spo2'] = packet[offset+4]
        packet_dict['pleth'] = packet[offset+1]
        packet_dict['pulse_rate'] = packet[offset+3] | ((packet[offset+2] & 0x40) << 1)
        offset=offset+data_step
        print(packet_dict['pleth']) #100Hz PPG

