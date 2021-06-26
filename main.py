'''
https://devzone.nordicsemi.com/nordic/short-range-guides/b/bluetooth-low-energy/posts/ble-characteristics-a-beginners-tutorial

http://www.blesstags.eu/2018/08/services-characteristics-descriptors.html

[Service] Heart Rate: 0000180d-0000-1000-8000-00805f9b34fb
---->[Char] Heart Rate Measurement: 00002a37-0000-1000-8000-00805f9b34fb | properties:['notify']
-------->[Descriptor] Handle 17: 00002902-0000-1000-8000-00805f9b34fb | Value: b'\x00\x00' 
---->[Char] Body Sensor Location: 00002a38-0000-1000-8000-00805f9b34fb | properties:['read']

[Service] Battery Service: 0000180f-0000-1000-8000-00805f9b34fb
---->[Char] Battery Level: 00002a19-0000-1000-8000-00805f9b34fb | properties:['read', 'notify']
-------->[Descriptor] Handle 23: 00002902-0000-1000-8000-00805f9b34fb | Value: b'\x00\x00' 

[Service] Device Information: 0000180a-0000-1000-8000-00805f9b34fb
---->[Char] Manufacturer Name String: 00002a29-0000-1000-8000-00805f9b34fb | properties:['read']
'''


import asyncio
import logging
#from logging import error
from bleak import BleakScanner,BleakClient

deviceName ="Nordic_HRM"
notify_char_uuid="00002a37-0000-1000-8000-00805f9b34fb"

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
    print(f"Notify data size:{len(data)} | data info: {data}")

async def main():
    (error,client) = await connectDeviceByName(deviceName)
    if error<0:
        print("Device %s is not found. error %d"%(deviceName,error))  
        return

    

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

    await client.start_notify(notify_char_uuid, charUUIDNotifyCallBack)
    await client.is_connected()
    while await client.is_connected():
       await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
