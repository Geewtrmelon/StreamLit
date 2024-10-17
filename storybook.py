import os
import streamlit as st
from openai import OpenAI


# client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
# use streamlit Secrets management

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
client_secret = st.secrets("OPENAI_API_KEY")

#story
def story_gen(prompt):
  system_prompt = """
  You are a world renowned suthor for young adults fiction short stories.
  Given a concept, generate a short story relevant to the themes of concept with a twist ending.
  the total length of story should be within 100 words
  """

  # system_prompt is now defined before being used in the response variable assignment
  response = client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [
        {'role':'system','content':system_prompt},
        {'role':'user','content':prompt}
    ],
    temperature = 1.3,
    max_tokens=2000
  )
  return response.choices[0].message.content

#cover art
def art_gen(prompt):
  response = client.images.generate(
      model = 'dall-e-2',
      prompt = prompt,
      size = '1024x1024',
      n = 1
  )
  return response.data[0].url

#cover prompt design
def design_gen(prompt):
  system_prompt = """
  You will be given a short story. Generate a prompt for a cover art that
  is suitable for story. The prompt is for dall-e-2.
  """
  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {'role':'system','content':system_prompt},
          {'role':'user','content':prompt}
      ],
      temperature = 1.3,
      max_tokens=2000
  )

  # Add a return statement to return the generated prompt
  return response.choices[0].message.content

prompt = "cat drinking cupuccino"
print(story_gen(prompt))



prompt = st.text_input('Enter a prompt')
if st.button('Generate'):
  story = story_gen(prompt)
  design = design_gen(story)
  art = art_gen(design)
  
  st.caption(design)
  st.divider()
  st.write(story)
  st.divider()
  st.image(art)


