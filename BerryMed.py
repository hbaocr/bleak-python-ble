'''
https://devzone.nordicsemi.com/nordic/short-range-guides/b/bluetooth-low-energy/posts/ble-characteristics-a-beginners-tutorial

http://www.blesstags.eu/2018/08/services-characteristics-descriptors.html

[Service] Unknown: 49535343-fe7d-4ae5-8fa9-9fafd205e455
---->[Char] Unknown: 49535343-1e4d-4bd9-ba61-23c647249616 | properties:['notify']
-------->[Descriptor] Handle 15: 00002902-0000-1000-8000-00805f9b34fb | Value: b'\x00\x00' 
---->[Char] Unknown: 49535343-8841-43f4-a8d4-ecbe34729bb3 | properties:['write-without-response', 'write']
---->[Char] Vendor specific: 00005343-0000-1000-8000-00805f9b34fb | properties:['write-without-response', 'write']
---->[Char] Vendor specific: 00005344-0000-1000-8000-00805f9b34fb | properties:['read']

[Service] Device Information: 0000180a-0000-1000-8000-00805f9b34fb
---->[Char] Manufacturer Name String: 00002a29-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] Model Number String: 00002a24-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] Serial Number String: 00002a25-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] Hardware Revision String: 00002a27-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] Firmware Revision String: 00002a26-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] Software Revision String: 00002a28-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] System ID: 00002a23-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] IEEE 11073-20601 Regulatory Cert. Data List: 00002a2a-0000-1000-8000-00805f9b34fb | properties:['read']
---->[Char] PnP ID: 00002a50-0000-1000-8000-00805f9b34fb | properties:['read']
'''

import BerryMedParser
import binascii
import asyncio
import logging
#from logging import error
from bleak import BleakScanner,BleakClient
import time
start = time.time_ns()

deviceName ="BerryMed"
notify_char_uuid="49535343-1e4d-4bd9-ba61-23c647249616"


async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

async def connectDeviceByName(bleName):
    devices = await BleakScanner.discover()
    error=-1
    bleClient=0
    for d in devices:
        print("found device  %s:%s at %d"%(d.name,d.address,d.rssi))
        if (d.name==bleName):
            bleClient =  BleakClient(d.address)
            error=0
            try:
                await bleClient.connect()
            except Exception as e:
                print(e)
                error=-2
            #finally:
            #    bleClient.disconnect()
            #    error=-3
            #    print("device disconnected")
            return (error,bleClient)
    
    return (error,bleClient)



def charUUIDNotifyCallBack(sender:int,data:bytearray):
    BerryMedParser.parse(data)
    #tmp = time.time_ns()
    #print(f"{(tmp)//1000} ms | Notify data size:{len(data)} | data info: {binascii.hexlify(data)}")
    #start = tmp

async def main():
    (error,client) = await connectDeviceByName(deviceName)
    if error<0:
        print("Device %s is not found. error %d"%(deviceName,error))  
        return

    '''
    print("error %d: device is connected"%(error))  
    
    print('Dicsover service- Optional')
    for service in client.services:
        print("")
        print("[Service] {0}: {1}".format(service.description,service.uuid))
        for char in service.characteristics:
            print("---->[Char] {0}: {1} | properties:{2}".format(char.description,char.uuid,char.properties))
            for descriptor in char.descriptors:
                value = await client.read_gatt_descriptor(descriptor.handle)
                print("-------->[Descriptor] Handle {0}: {1} | Value: {2} ".format(descriptor.handle,descriptor.uuid, bytes(value)))
    
    
    print('Enable device notify by changing the config change descriptor of characteristic given by UUID and subcrible on this notify the callback')
    '''
    await client.start_notify(notify_char_uuid, charUUIDNotifyCallBack)
    #await client.is_connected()
    while True:
       await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
