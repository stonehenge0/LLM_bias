### Documentation of prompts
**tldr:** : This file contains all the LLM prompts used throughout the project. 

For each usecase, it details what model was used, how it was accessed and with
which settings.


You will find the prompts for: 
* generating paraphrased texts targeted at:
  * men
  * women
  * all genders (neutral)
* classifying the gender targetedness of current program descriptions

----
### 1. Paraphrase Texts

**script**: generate_paraphrases_GPT.py

**model**: GPT 4 o 

**accessed over**: OpenAI API (commercial)

a) male-targeted prompt
```
You are the coordinator and responsible for writing academic program descriptions for
 a university. You need to rewrite the current program description provided below for
the university website. This description was written by a previous program coordinator
 in order to attract male candidates to the program, but the percentage of men did
 not change after that. Rewrite the text to make more men want to apply to this program.
Use a vocabulary that speaks and correlates to men according to your understanding.
 Please also incorporate the values that are important to men in the text to help
improve the program description. The resulting text should be cohesive and follow
an academic style of writing. Please think and organize your tasks step-by-step.
The text is the following:  {program description}
```

b) female targeted prompt
```
You are the coordinator and responsible for writing academic program descriptions
for a university. You need to rewrite the current program description provided
below for the university website. This description was written by a previous
program coordinator in order to attract female candidates to the program, but
the percentage of women did not change after that. Rewrite the text to make
more women want to apply to this program. Use a vocabulary that speaks and
correlates to women according to your understanding. Please also incorporate
the values that are important to women in the text to help improve the
program description. The resulting text should be cohesive and follow an
academic style of writing. Please think and organize your tasks step-by-step.
The text is the following:   {program description}


```

c) neutral prompt
```
You are the coordinator and responsible for writing academic program descriptions for a university.
 You need to rewrite the current program description provided below for the university website.
This description was written by a previous program coordinator in order to attract candidates of both
genders equally to the program, but the percentage of candidates did not get more even between genders.
 Rewrite the text to make more people of both genders want to apply to this program. Use a vocabulary
that speaks and correlates to both genders according to your understanding. Please also incorporate
the values that are important to both genders in the text to help improve the program description.
The resulting text should be cohesive and follow an academic style of writing. Please think and
organize your tasks step-by-step.
The text is the following:  {program description}


```

> The prompts for 1 were written by Marina Tiuleneva a student in a previous lab rotation.


----- 
### 2. Classify Gender Targetedness

**script**: none, prompts were plugged in manually

**model**: LLAMA3 70B instruct

**accessed over**: HuggingChat

prompt:
```
Imagine you are a program coordinator, aiming to make university program descriptions more
appealing to all genders.
You are especially concerned with language that might subtly disencourage specific
genders to apply, using
whatever measures you seem fit for this task.
Classify the following text into one of these categories: strongly male oriented,
moderately male oriented,
neutral,  moderately female oriented, strongly female oriented. 
Give strong weight to even small factors in this categorization. 

Provide your answer in a json object like the one provided below. It should make
clear which metrics you based
 your decision on. Include your step by step reasoning in the json as well.  The
confidence rating should either be low, medium, or high.


{
"classification" : "...", 
"reasoning" : "....",
"confidence rating" : "..."
}

Text: {program description text}
```
