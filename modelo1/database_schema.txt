Modelo da base de dados (sqlite)

tabela imlist:
	rowid 		--> id
	filename 	--> nome do ficheiro da imagem

tabela imwords:
	imid		--> id da imagem	
	wordid		--> id da palavra visual
	vocname		--> o nome da palavra visual

tabela imhistogram:
	imid		--> id da imagem
	histigram	--> histograma
	vocname		--> nome da palavra visual
