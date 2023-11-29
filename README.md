# Welcome on Minions-Toolbox

This repository contains multiple useful tools developed for the data from SmartSolo IGU-16HR 3C series. As those geophones shares some similarities with yellowish creatures, we decide to rename the nodes as Minions. As a consequence, a new branch in seismology had appeared and called : *Minionology*.


<p align="center">
  <img src="Figures/Minions Seismology.be.jpg" width=600></img>
</p>


## Notebooks :

**Renamer_SDS.ipynb** : Notebook uses to reclassify SmartSolo .miniseed into a **S**eisComP **D**ata **S**tructure (SDS).

**approx_positioning.ipynb** : uses to extract satellite data from LogFile and reassignated an approximative location (median point).  

**response.ipynb** : uses to remove automatically the instrument response from minions' data

## Python codes (PyMod) :
 
**LogExtract.py** : Python module to extract data from SmartSolo LogFiles

To compute HVSR from SmartSolo-3C (Minions) use the repository developped by [@KoenVanNoten](https://github.com/KoenVanNoten) for [skience2023](https://github.com/heinerigel/skience2023/tree/main/02_Tuesday/Afternoon)