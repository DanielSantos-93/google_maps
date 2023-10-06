from google_maps import Maps

if __name__ == '__main__':
    pesquisa = input('Digite a pesquisa: ')
    quantidade = int(input('Quantos resultados gostaria de pesquisar (0 para todos): '))
    google_map = Maps()

    google_map.main(pesquisa, quantidade)
