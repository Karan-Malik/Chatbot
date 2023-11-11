from src.service import ModelService

# Self learning
# print('Ajude-me a aprender?')
# tag = input('Por favor insira a categoria geral da sua pergunta ')
# flag = -1
# for i in range(len(intents['intents'])):
#     if tag.lower() in intents['intents'][i]['tag']:
#         intents['intents'][i]['patterns'].append(input('Digite sua mensagem: '))
#         intents['intents'][i]['responses'].append(input('Insira a resposta esperada: '))
#         flag = 1
# if flag == -1:
#     intents['intents'].append(
#         {'tag': tag,
#          'patterns': [input('Por favor insira a sua mensagem')],
#          'responses': [input('Insira a resposta esperada')]})
# with open('intents.json', 'w') as outfile:
#     outfile.write(json.dumps(intents, indent=4))
# TODO: Rodar treino para incluir informacoes add

model_service = ModelService()
model_service.training()
