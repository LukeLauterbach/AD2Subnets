## Description 
Uses [dirkjanm's adidnsdump](https://github.com/dirkjanm/adidnsdump) to get DNS records from Active Directory, and then returns a list of /24 subnets.

Only requires low-level AD privileges. 

### Installation 
> pipx install git+https://github.com/LukeLauterbach/AD2Subnets

### Usage
> ad2subnets {DOMAIN}/{USERNAME}:{PASSWORD}@{DC IP OR HOSTNAME}
#### Optional Arguments
| Argument | Description               |
|----------|---------------------------|
| `-o`     | File to output results to |
