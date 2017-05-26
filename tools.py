import simplejson as json
from sys import argv
import re
import pandas as pd

file_out_pos = 'pos.txt'
file_out_neg = 'neg.txt'


def jason_to_txt(filename):
	
	# abre o arquivo json
	with open(filename, 'r') as in_f:

		# itera pelas linhas
		for line in in_f:
			obs = json.loads(line) # converte a linha de str para dict
			nota = int(obs['overall']) # pega a nota da observação
			texto = obs['reviewText'] # pega o texto da observação

			# pequeno processamento
			texto = re.sub(r"[^a-z0-9]+", " ", texto.lower()) + '\n' # mantem apenas char alfanuméricos

			# separa avaliações negativas
			if nota < 3:

				with open(file_out_neg, "a") as myfile:
					myfile.write(texto) # adiciona texto no arquito de obs negativas

			# separa avaliações postivas
			elif nota > 3:

				with open(file_out_pos, "a") as myfile:
					myfile.write(texto) # adiciona texto no arquito de obs positivas

def read_dataframe(neg='/media/matheus/Elements/data/nlp/neg.txt',
					pos='/media/matheus/Elements/data/nlp/pos.txt',
					n_pos = 50000,
					n_neg = 50000):
	
	neg_df = pd.read_csv(neg, nrows=n_neg, header=None, names=['text']) # le textos negativos
	neg_df['sentiment'] = 0 # classifica textos negativos com 0

	pos_df = pd.read_csv(pos, nrows=n_pos, header=None, names=['text']) # le textos positivos
	pos_df['sentiment'] = 1 # classifica textos negativos com 0

	return pos_df.append(neg_df, ignore_index=True).sample(frac=1)

if __name__ == '__main__':

	run_flags = argv[1:] # argumentos da linha de comando
	filename = run_flags[0]
	jason_to_txt(filename)

	# data = read_dataframe()
	# print(data.shape)
	# print(data.head())