# Mobile Network Scripting

This is a python based domain specific language (DSL) and simulator for 
prototyping and testing algorithms for mobile and dynamically networked 
multi-agent systems operating in physical environments. 

[![Open In Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/ANRGUSC/mobile_network_scripting.git)

## Installation
To get started, you can just click the "Open in Gitpod" button above.
This starts a fresh dev environment with everything pre-installed and ready to 
go with an in-browser VSCode IDE. 

Otherwise to install on your system, you just need python >= 3.6:

```bash
git clone https://github.com/ANRGUSC/mobile_network_scripting.git 

pip install ./mobile_network_scripting 
# Or in developer mode
pip install -e ./mobile_network_scripting
```

## Usage 
When you install the package, the CLI command ```mobscript``` is included.
See the [examples](./examples) for example instruction sets for different tasks.

```bash 
mobscript ./mobile_network_scripting/examples/pathfinding
mobscript ./mobile_network_scripting/examples/overview
mobscript ./mobile_network_scripting/examples/many_waypoints_in_tick
mobscript ./mobile_network_scripting/examples/delayed_instruction
```

By default, output files will save to a directory ./generated_data wherever 
you ran the ```mobscript``` command from. 
To change this behavior, simply specify a location:

```bash
mobscript ./mobile_network_scripting/examples/pathfinding -o ./outputs
```

