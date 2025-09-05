# MolE antimicrobial potential

A publicly available dataset accounting for the effect of 1,197 marketed drugs against 40 bacterial strains was used to train an XGBoost model, termed MolE-XGBoost, that predicts growth inhibition using MolE pre-trained representations. The model enabled a concise assessment of the antimicrobial potential of chemical compounds, including the re-discovery of de novo structurally distinct antibiotic candidates and the identification of broad-spectrum activity in other compounds that would have been missed by standard models.

This model was incorporated on 2025-08-21.Last packaged on 2025-09-05.

## Information
### Identifiers
- **Ersilia Identifier:** `eos6m2k`
- **Slug:** `mole-antimicrobial`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Activity prediction`
- **Biomedical Area:** `Antimicrobial resistance`
- **Target Organism:** `Akkermansia muciniphila`, `Bacteroides caccae`, `Bacteroides fragilis`, `Bacteroides ovatus`, `Bacteroides thetaiotaomicron`, `Bacteroides uniformis`, `Bacteroides vulgatus`, `Bacteroides xylanisolvens`, `Bifidobacterium adolescentis`, `Bifidobacterium longum`, `Bilophila wadsworthia`, `Blautia obeum`, `Clostridium bolteae`, `Clostridium difficile`, `Clostridium perfringens`, `Clostridium ramosum`, `Clostridium saccharolyticum`, `Collinsella aerofaciens`, `Coprococcus comes`, `Dorea formicigenerans`, `Eggerthella lenta`, `Escherichia coli`, `Eubacterium eligens`, `Eubacterium rectale`, `Fusobacterium nucleatum`, `Lactobacillus paracasei`, `Odoribacter splanchnicus`, `Parabacteroides distasonis`, `Parabacteroides merdae`, `Prevotella copri`, `Roseburia hominis`, `Roseburia intestinalis`, `Ruminococcus bromii`, `Ruminococcus gnavus`, `Ruminococcus torques`, `Streptococcus parasanguinis`, `Streptococcus salivarius`, `Veillonella parvula`
- **Tags:** `Antimicrobial activity`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `40`
- **Output Consistency:** `Fixed`
- **Interpretation:** Growth inhibition probability prediction of 40 bacterial strains.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| apscore_total | float | high | Global Antimicrobial Potential score |
| apscore_gpositive | float | high | Antimicrobial Potential score for gram-positive microbes |
| apscore_gnegative | float | high | Antimicrobial Potential score for gram-negative microbes |
| akkermansia_muciniphila_nt5021 | float | high | Probability to inhibit the growth of Akkermansia muciniphila (NT5021) |
| bacteroides_caccae_nt5050 | float | high | Probability to inhibit the growth of Bacteroides caccae (NT5050) |
| bacteroides_fragilis_et_nt5033 | float | high | Probability to inhibit the growth of Bacteroides fragilis (ET) (NT5033) |
| bacteroides_fragilis_nt_nt5003 | float | high | Probability to inhibit the growth of Bacteroides fragilis (NT) (NT5003) |
| bacteroides_ovatus_nt5054 | float | high | Probability to inhibit the growth of Bacteroides ovatus (NT5054) |
| bacteroides_thetaiotaomicron_nt5004 | float | high | Probability to inhibit the growth of Bacteroides thetaiotaomicron (NT5004) |
| bacteroides_uniformis_nt5002 | float | high | Probability to inhibit the growth of Bacteroides uniformis (NT5002) |

_10 of 43 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos6m2k](https://hub.docker.com/r/ersiliaos/eos6m2k)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos6m2k.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos6m2k.zip)

### Resource Consumption
- **Model Size (Mb):** `777`
- **Environment Size (Mb):** `6382`
- **Image Size (Mb):** `8656.27`

**Computational Performance (seconds):**
- 10 inputs: `32.37`
- 100 inputs: `22.48`
- 10000 inputs: `317.06`

### References
- **Source Code**: [https://github.com/rolayoalarcon/mole_antimicrobial_potential](https://github.com/rolayoalarcon/mole_antimicrobial_potential)
- **Publication**: [https://www.nature.com/articles/s41467-025-58804-4](https://www.nature.com/articles/s41467-025-58804-4)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2025`
- **Ersilia Contributor:** [arnaucoma24](https://github.com/arnaucoma24)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos6m2k
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos6m2k
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
