import asyncio
import datetime
import json
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message


class MachineIoTClient:
    def __init__(self, connection_string: str, machine_id: str):
        """
        Initialize Azure IoT Hub client for a machine.

        Args:
            connection_string: Azure IoT Hub connection string
            machine_id: Unique identifier for the machine
        """
        self.device_client = None
        self.connection_string = connection_string
        self.machine_id = machine_id
        self.is_connected = False

    async def connect(self):
        """Initialize the IoT Hub client connection."""
        if not self.is_connected:
            self.device_client = IoTHubDeviceClient.create_from_connection_string(
                self.connection_string
            )
            await self.device_client.connect()
            self.is_connected = True

    async def disconnect(self):
        """Disconnect from IoT Hub."""
        if self.is_connected and self.device_client:
            await self.device_client.disconnect()
            self.is_connected = False

    async def send_telemetry(self, total_output_unit_count: int, machine_speed: float):
        """
        Send telemetry data to IoT Hub.

        Args:
            total_output_unit_count: Total units produced
            machine_speed: Current machine speed
        """
        if not self.is_connected:
            await self.connect()

        telemetry_data = {
            "telemetry": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "datasource": "172.17.2.1:80",
                "machineid": self.machine_id,
                "totaloutputunitcount": total_output_unit_count,
                "machineSpeed": machine_speed,
            }
        }

        message = Message(json.dumps(telemetry_data))
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties["messageType"] = "Telemetry"

        await self.device_client.send_message(message)

    async def send_machine_event(
            self,
            event_type: str,
            job_id: str,
            total_output_unit_count: int,
            machine_speed: float
    ):
        """
        Send machine event to IoT Hub.

        Args:
            event_type: Type of machine event
            job_id: Identifier for the current job
            total_output_unit_count: Total units produced
            machine_speed: Current machine speed
        """
        if not self.is_connected:
            await self.connect()

        message = {
            "type": event_type,
            "equipmentId": self.machine_id,
            "jobId": job_id,
            "totalOutputUnitCount": total_output_unit_count,
            "machineSpeed": machine_speed,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        msg = Message(json.dumps([message]))
        msg.content_type = "application/json"
        msg.content_encoding = "utf-8"
        msg.custom_properties["messageType"] = "MachineEvent"

        await self.device_client.send_message(msg)


async def main():
    # Replace with your IoT Hub connection string
    connection_string = "HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI6;SharedAccessKey=Lk8/pNBXRT7jFKvD2kWMDZy11Z82rETIQAIoTNEZCq4="
    client = MachineIoTClient(connection_string, "lauzhack-pi6")

    try:
        # Connect to IoT Hub
        await client.connect()

        # Send telemetry
        await client.send_telemetry(140, 5.0)

        # Send machine event
        await client.send_machine_event(
            event_type="ProductionStart",
            job_id="JOB123",
            total_output_unit_count=140,
            machine_speed=5.0
        )

        print("Sent info succesfully")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Always disconnect properly
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())