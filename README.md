# SDP Group 22 Repo
This is the repository for the softare component of the inflatable mannequin leg developed by Group 22 (Yanjin, Alice, Adarsh, Aiden, Bhavya, Eric, Enes, Stone = YaaaBees) as part of the the System Design course at the University of Edinburgh. 

Our mannequin leg was built of silicone sleeves/pouches which could inflate and deflate to specific sizes using pumps and a network of tubing splitters and solenoid valves. The sizes were achieved by inflating each sleeves for a certain amount of time at a specific power from its resting state and we also integrated a pressure sensor into one of the silicone pouches so that the sizes could be achieved by monitoring the pouches/sleeves' internal air pressure.

## How to use:
See Setup_overview.txt for how the valves and the motors should be connected to the motorboard and the (Cube)Main.py files which run our demo for the leg and for the cube.

To change the hardcoded timing/pressure thresholds for inflating and deflating the silicone pouches, look in the init functions of Safe_Controller and Cube_Controller.

If an error occurs and the pumps or valves do not turn off correctly, run emergency.py.

Air.py has all the hardware-control functionality.

See https://docs.google.com/drawings/d/1iiNrprrmitW4A5fImg711Zits6A8UIad0X0ZcEftsuo/edit?usp=sharing for valve connections (may need to double-check that this is correct).
