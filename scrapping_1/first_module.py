import pandas as pd

states = ['California', 'Texas', 'Florida', 'New York']
population = [65151311, 6253151, 6373251, 1224625]
dict_states = {
    'States': states,
    'population': population
}
df_states = pd.DataFrame(dict_states)
print(df_states)
df_states.to_csv('states.csv', index=False)
# for state in states:
#     if state=='Florida':
#         print(state)

with open('test.txt', 'w') as file:
    file.write('Data succesfully scraped')
    k=0
print(k)