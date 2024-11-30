from gpiozero import DigitalOutputDevice
from time import sleep


def test_multiple_gpios(gpio_pins):
    # Dictionary to store output objects
    outputs = {}

    try:
        # Create output objects
        print("Initializing GPIO pins...")
        for pin in gpio_pins:
            try:
                outputs[pin] = DigitalOutputDevice(pin)
                print(f"Successfully initialized GPIO {pin}")
            except Exception as e:
                print(f"Failed to initialize GPIO {pin}: {str(e)}")
                continue

        # Test each output
        for pin, output in outputs.items():
            print(f"\nTesting GPIO {pin}")
            for i in range(1):  # Test 3 times
                print(f"Cycle {i + 1}: GPIO {pin} HIGH")
                output.on()
                sleep(1.5)  # Shorter delay for stepper testing
                print(f"Cycle {i + 1}: GPIO {pin} LOW")
                output.off()
                # sleep(1.5)
            print(f"GPIO {pin} test complete")

    except KeyboardInterrupt:
        print("\nTest stopped by user")

    finally:
        # Clean up
        print("\nCleaning up...")
        for output in outputs.values():
            output.off()  # Ensure all pins are off
            output.close()
        print("Cleanup complete")


if __name__ == "__main__":
    # List of GPIO pins to test
    gpio_list = [i for i in range(20, 30)]
    # gpio_list = [18, 23, 24, 25]

    print(f"Starting test for GPIO pins: {gpio_list}")
    test_multiple_gpios(gpio_list)