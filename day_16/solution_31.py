import numpy as np
import io
import argparse

def hex_to_binary(hex):
    hex_dict = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    decoded = ""
    for c in hex:
        decoded += hex_dict[c]
    return decoded

def binary_to_decimal(binary):
    if binary:
        order = len(binary)
        decmial = 0
        for i, bit in enumerate(binary):
            decmial += 2**(order - i - 1) * int(bit)
        return decmial
    else:
        return None

def parse_literal(subpacket, verbose=False):
    if verbose:
        print(f"parsing literal from {subpacket}")
    number = ""
    offset = 0
    while True:
        control = subpacket[offset]
        offset += 1
        number += subpacket[offset:offset + 4]
        offset += 4
        if control == "0":
            break
    if verbose:
        print(f"parsed {number} from {subpacket}")
    return number, offset

def parse_packet(packet, verbose=False):
    if verbose:
        print("parsing packet", packet)
    def _fail():
        return None, None, None, None
    if len(packet) < 6:
        return _fail()
    # Every packet begins with a standard header: 
    # the first three bits encode the packet version, 
    # and the next three bits encode the packet type ID.
    offset = 0
    header = packet[offset:offset + 6]
    offset += 6
    version = binary_to_decimal(header[0:3])
    type_id = binary_to_decimal(header[3:6])
    if verbose:
        print("parsed header, version, type", header, version, type_id)
    if type_id == 4:
        literal, literal_length = parse_literal(packet[offset:], verbose=verbose)
        offset += literal_length
        value = binary_to_decimal(literal)
        if verbose:
            print("parsed literal", value)
    else:
        if len(packet) < 6 + 1:
            return _fail()
        length_type_id = binary_to_decimal(packet[offset])
        offset += 1
        if length_type_id == 0:
            if len(packet) < 6 + 1 + 15:
                return _fail()
            if verbose:
                print("parsing operator packet type 0")
            # Every other type of packet (any packet with a type ID other than 4) 
            # represent an operator that performs some calculation on one or more 
            # sub-packets contained within. 
            # An operator packet contains one or more packets. To indicate which 
            # subsequent binary data represents its sub-packets, an operator packet 
            # can use one of two modes indicated by the bit immediately after the 
            # packet header; this is called the length type ID:
            # If the length type ID is 0, then the next 15 bits are a number that 
            # represents the total length in bits of the sub-packets contained by 
            # this packet.
            sub_packet_length_binary = packet[offset:offset + 15]
            sub_packet_length = binary_to_decimal(sub_packet_length_binary)
            if verbose:
                print(f"parsing {sub_packet_length_binary}, {sub_packet_length} bits for sub packets")
            offset += 15
            length_parsed = 0
            subpackets = []
            while length_parsed < sub_packet_length:
                _type_id, _version, _value, _offset = parse_packet(packet[offset:], verbose=verbose)
                offset += _offset
                if verbose:
                    print(f"parsed packet of length {_offset}, remaining packet: {packet[offset:]}")
                length_parsed += _offset
                subpackets.append({"type_id": _type_id, "version": _version, "value": _value})
            value = subpackets
        elif length_type_id == 1:
            if len(packet) < 6 + 1 + 11:
                return _fail()
            if verbose:
                print("parsing operator packet type 1")
            # If the length type ID is 1, then the next 11 bits are a number that 
            # represents the number of sub-packets immediately contained by 
            # this packet.
            number_of_sub_packets = binary_to_decimal(packet[offset:offset + 11])
            if verbose:
                print(f"parsing {number_of_sub_packets} sub packets")
            offset += 11
            num_sub_packets_parsed = 0
            subpackets = []
            while num_sub_packets_parsed < number_of_sub_packets:
                _type_id, _version, _value, _offset = parse_packet(packet[offset:], verbose=verbose)
                offset += _offset
                if verbose:
                    print(f"parsed packet of length {_offset}, remaining packet: {packet[offset:]}")
                num_sub_packets_parsed += 1
                subpackets.append({"type_id": _type_id, "version": _version, "value": _value})
            value = subpackets
        else:
            raise Exception("bad length type id")
    if verbose:
        print("parsed value", value)
    return type_id, version, value, offset

def unpackage(packet, verbose=False):
    packets = []
    offset = 0
    while offset < len(packet):
        type_id, version, value, _offset = parse_packet(packet[offset:], verbose=verbose)
        if value:
            offset += _offset
            packets.append({"type_id": type_id, "version": version, "value": value})
        else:
            break
    return packets

def version_sum(packets):
    _sum = 0
    for packet in packets:
        _sum += packet['version']
        if type(packet['value']) is list:
            _sum += version_sum(packet['value'])
    return _sum

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--test-num", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    test_num = args.test_num
    verbose = args.verbose

    if test:
        infile = f"test_input_{test_num}"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    hex = lines[0]
    packet = hex_to_binary(hex)
    packets = unpackage(packet, verbose=verbose)
    if verbose:
        print("packets:", packets)
    
    print("version sum:", version_sum(packets))

if __name__ == "__main__":
    main()
