<br>

<center>
<div style="width:100%;text-align:center;">
<img src='data/image_readme.png' width="400" height="300">  
</div>
</center>

---

### Investigating Gender Bias with LLms
This repository documents the code and data for the research project Investigating Gender Bias with LLMs. It investigates how we can encourage women to apply to male dominated fields (and the reverse for men) by way of changing the wording of program descriptions using LLMs. 

We also test how LLMs think about gendered language and gender bias in text. If you want to have an in depth look at the research itself and what we found, have a look at the final presentation in `final_presentation.pptx`


### How to navigate this repository
There are three main folders:  
**code**: all code used for this project. This includes seeds and hyperparameters for the LLM prompts, code for the statistical analysis as well as the scripts for implementing the traditional metrics we use as our baseline.   
**data**: Mainly the program descriptions and statistics about them. A  "p_" prefix as in`p_results_agentic.csv` indicates that the file contains data about the paraphrased program descriptions, files without the prefix are for the original descriptions.   
**results**: Final statistics, cleaned data for presentation. 

If you are just looking to have an idea what this project is and what it did, you can find the presentation in `final_presentation.pptx`


## Installation
See `requirements.txt` for a full list of requirements.
The fastest way to install the requirements is using [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing) and a [virtual environment](https://docs.python.org/3/tutorial/venv.html) (like [venv](https://docs.python.org/3/library/venv.html)).
> Make sure to substitute <name_of_vev> with an actual name for your environment.

```sh
python3 -m venv <name_of_venv>
source <name_of_venv>/bin/activate
pip install -r requirements.txt
```

If you want to run the LLM scripts, you will need an API key for KISSKI. API keys are free of charge if you are a student or researcher at a German university. You can request them [here](https://kisski.gwdg.de/leistungen/2-02-llm-service/). 

```python

from openai import OpenAI
import pandas as pd

# API configuration
api_key = "YOUR_API_KEY"  # Replace with your own API key

```


## Data Sources/ Acknowledgements
- Marc Brysbaert, Amy Beth Warriner, and Victor Ku-
perman. 2014. Concreteness ratings for 40 thousand
generally known English word lemmas. Behavior
Research Methods, 46(3):904–911.  
- Danielle Gaucher, Justin Friesen, and Aaron C. Kay 2011. Evidence that gendered wording in job advertisements exists and sustains gender inequality. Journal of Personality and Social Psychology, 101(1):109–128.      
- https://github.com/lovedaybrooke/gender-decoder


## Project Details

**Author**: Emma Stein  
**Supervisors**: [Dr. Terry Ruas](https://terryruas.com/), [Jan Philip Wahle](https://jpwahle.com/)  
**Project Module**: B.DH.21, Summer Semester 2024  

> For more projects related to AI Safety and Natural Language Processing you can have a look at the other projects at the [GippLab](https://gipplab.org/)

## Contact
emma.stein@stud.uni-goettingen.de  


